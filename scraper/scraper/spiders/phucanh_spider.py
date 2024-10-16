import scrapy
from scrapy.http import Response
import re
from .base_laptopshop_spider import BaseLaptopshopPageSpider

def _extract_dimensions(response: Response):  # Helper function to extract dimensions and unit
    for dimension_text in response.css('td:contains("Kích thước") + td.spec-value::text').getall():
        if dimension_text:
            dimension_text = dimension_text.strip()
            
            # Improved regex to capture potential extra text or units before and after dimensions
            match = re.search(r"(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*(cm|mm)", dimension_text, re.IGNORECASE)
            if match:
                length, _, width, _, height, _, unit = match.groups()
                try:
                    length = float(length)
                    width = float(width)
                    height = float(height)
                    
                    # Convert cm to mm if necessary
                    if unit.lower() == 'cm':
                        length *= 10
                        width *= 10
                        height *= 10
                        
                    return length, width, height  # Return dimensions in millimeters
                
                except ValueError:
                    # Log or raise an error in real use case; print for now
                    print(f"Error converting dimension to float: {dimension_text}")
                    
    # Return None if extraction fails
    return None, None, None

# create scraper
class PhucanhShopSpider(BaseLaptopshopPageSpider): 
    name = "phucanh_spider"
    start_urls = ['https://www.phucanh.vn/laptop.html']  
    product_site_css = 'div.p-container a::attr(href)'  # Example CSS selector to extract links to products
    page_css = 'div.paging a::attr(href)'
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    def get_product_sites(self, response: Response):
        """
        Extracts the product links from the current page and generates requests to follow them.
        Filters out invalid URLs like 'javascript:void(0)'.
        """
        product_urls = response.css(self.product_site_css).getall()
        
        # Filter out invalid URLs
        valid_urls = [url for url in product_urls if url.startswith("http") or url.startswith("/")]
        
        # Generate requests only for valid URLs
        return [response.follow(url=url, callback=self.parse_one_observation) for url in valid_urls]

    def parse_brand(self, response:Response):
        # Extract the full product title
        product_title = response.css('h1::text').get()

        # Split the title by spaces and get the first word (brand)
        if product_title:
            brand = product_title.split()[1]  # Assuming the brand is always the second word after "Laptop"
        else:
            brand = 'N/A'

        return brand
    
    def parse_name(self, response:Response):
        # Extract the full product title
        product_title = response.css('h1::text').get()
        
        # Split the product title by the first occurrence of '(' and get the first part
        if product_title:
            product_name = product_title.split('(')[0].strip()  # Strip removes any leading/trailing spaces
            product_name = product_name.replace('Laptop ', '').replace('gaming ', '').replace('Gaming', '')
        else:
            product_name = 'N/A'

        return product_name

    def parse_price(self, response:Response):
        # Extract the price with the currency symbol
        price_text = response.css('span.detail-product-old-price::text').get()
        
        if price_text:
            # Remove dots and currency unit (like "đ")
            price = price_text.replace('.', '').split()[0].strip()
        else:
            price = 'N/A'
        
        return price
    def parse_cpu(self, response: Response):
        cpu_text = response.css('td:contains("Bộ VXL") + td.spec-value::text').get()
        if cpu_text: 
            if ': ' in cpu_text: 
                cpu_text = cpu_text.replace(': ', '').lower()
                cpu_text = re.sub(r"\d+(\.\d+)?\s*ghz", "", cpu_text).strip()
                
                # Apple
                if 'apple' in cpu_text: 
                    cpu_text = cpu_text.replace(' cpu', '').strip()
                
                # Intel
                elif 'core' in cpu_text or 'ultra' in cpu_text: 
                    cpu_text = 'intel ' + cpu_text
                
            return cpu_text

        return 'N/A'
    def parse_vga(self, response):
        vga_text = response.css('td:contains("Card màn hình") + td.spec-value::text').get()
        if vga_text:
            vga_text_lower = vga_text.strip().lower() # Normalize for easier comparison
            if "intel" in vga_text_lower and ("graphics" in vga_text_lower or "hd graphics" in vga_text_lower): # Check for common integrated graphics patterns
                return "N/A"  # Onboard Intel graphics
            elif "amd radeon graphics" in vga_text_lower or "amd radeon" in vga_text_lower: # Check for common integrated AMD graphics patterns
                return "N/A" # Onboard AMD graphics
            elif 'onboard' in vga_text_lower.lower():
                return "N/A"
            elif not vga_text_lower: # Handles cases where the selector doesn't find anything
                return "N/A"
            else:
                if 'vga nvidia - ' in vga_text_lower: 
                    vga_text = vga_text.replace('VGA Nvidia - Nvidia ', '') # Dedicated graphics card
                if 'vga amd - ' in vga_text_lower:
                    vga_text = vga_text.replace('VGA AMD - AMD ', '')
                if ': ' in vga_text: 
                    vga_text = vga_text.replace(': ', '')
                return vga_text
        else:
            return "N/A" # Value not found
    def parse_ram_amount(self, response):
        ram_text = response.css('td:contains("Bộ nhớ RAM") + td::text').get()
        if ram_text: 
            return ram_text.split()[1]
        return 'N/A'
    
    def parse_ram_type(self, response):
        ram_text = response.css('td:contains("Bộ nhớ RAM") + td::text').get()
        if ram_text:
            # Capture the "ddr" followed by a digit
            match = re.search(r"(ddr\d+)", ram_text.lower())
            if match:
                return match.group(1)  # Return the full match
        return 'N/A'
    
    def parse_storage_amount(self, response):
        # Select all <td> elements and look for the one containing 'Ổ cứng', then get the following <td>
        storage_text = response.css('td:contains("Ổ cứng") + td::text').get()

        if storage_text:
            # Clean up the storage text by removing ' SSD', ' HDD', and ': ' if they exist
            storage_text = storage_text.replace(' SSD', '').replace(' HDD', '').replace(': ', '').strip()
            
            return storage_text

        return 'N/A'

    def parse_storage_type(self, response): 
        for storage_text in response.css('td.spec-value::text').getall(): 
            if any(storage_type in storage_text for storage_type in ['SSD', 'HDD']): 
                if 'SSD' in storage_text: 
                    return 'SSD'
                else: 
                    return 'HDD'
        return 'N/A'
    
    def parse_screen_resolution(self, response):
        screen_text = response.css('a[href*="do-phan-giai-man-hinh"]::text').get()

        if screen_text:
            match = re.search(r"\((\d+x\d+)\)", screen_text)
            if match: 
                return match.group(1)
        return 'N/A'
    
    def parse_screen_size(self, response):
        screen_text = response.css('td:contains("Kích thước màn hình") + td::text').get()

        if screen_text:
            # Extract just the resolution part (e.g., "Full HD")
            screen_text = screen_text.strip() # Remove leading/trailing whitespace
            parts = screen_text.split() # Split into parts based on spaces
            if len(parts) > 1: # Check if there's a resolution part (after the size)
                size  = " ".join(parts[:2]) # Join the size parts back together
                if ': ' in size: 
                    size = size.replace(': ', '')
                return size 
        return 'N/A'

    def parse_length(self, response):
        length, _, _ = _extract_dimensions(response)
        return length if length is not None else 'N/A'

    def parse_width(self, response):
        _, width, _ = _extract_dimensions(response)
        return width if width is not None else 'N/A'


    def parse_height(self, response):
        _, _, height = _extract_dimensions(response)
        return height if height is not None else 'N/A'
    
    def parse_weight(self, response):
        weight_text = response.css('td:contains("Trọng lượng") + td::text').get() 
        if weight_text:
            if ': ' in weight_text: 
                weight_text = weight_text.replace(': ', '') 
            return weight_text
        
        return 'N/A'
    
    def parse_default_os(self, response):
        default_os_text = response.css('td:contains("Hệ điều hành") + td::text').get() 
        if default_os_text: 
            return default_os_text.replace(': ', '')

        return 'N/A'
    
    def parse_color(self, response):
        color_text = response.css('td:contains("Màu sắc") + td::text').get() 
        if color_text: 
            return color_text.lower().replace(': ', '')
        
        return 'N/A'
    
    def parse_screen_refresh_rate(self, response):
        # Use the CSS selector to target the <a> tag containing the refresh rate, and extract its text
        refresh_rate = response.css('a[href*="tan-so-quet-cua-man-hinh"]::text').get()
        if refresh_rate:
            return refresh_rate.strip().replace(': ', '')  # Clean up any extra spaces

        return 'N/A'  # Return 'N/A' if not found
    
    def parse_number_usb_a_ports(self, response):
        ports_texts = response.css('td.spec-key:contains("Cổng giao tiếp") + td.spec-value::text').getall()
        count = 0
        for ports_text in ports_texts:
            if ports_text:
                ports_text = ports_text.replace('<br>', ' ').replace(': ', '').strip().lower()
                if 'type-a' in ports_text or 'usb-a' in ports_text:
                    match = re.search(r"(\d+)x", ports_text)
                    if match:
                        count += int(match.group(1))
                    else:
                        count += 1  # Count 1 if no explicit number
        return count


    def parse_number_usb_c_ports(self, response):
        ports_texts = response.css('td.spec-key:contains("Cổng giao tiếp") + td.spec-value::text').getall()
        count = 0
        for ports_text in ports_texts:
            if ports_text:
                ports_text = ports_text.replace('<br>', ' ').replace(': ', '').strip().lower()
                if 'type-c' in ports_text or 'usb-c' in ports_text:
                    match = re.search(r"(\d+)x", ports_text)
                    if match:
                        count += int(match.group(1))
                    else:
                        count += 1
        return count

    def parse_number_hdmi_ports(self, response):
        ports_texts = response.css('td.spec-key:contains("Cổng giao tiếp") + td.spec-value::text').getall()
        count = 0
        for ports_text in ports_texts:
            if ports_text:
                ports_text = ports_text.replace('<br>', ' ').replace(': ', '').strip().lower()
                if 'hdmi' in ports_text:
                    match = re.search(r"(\d+)x", ports_text)
                    if match:
                        count += int(match.group(1))
                    else:
                        count += 1
        return count


    def parse_number_ethernet_ports(self, response):
        ports_texts = response.css('td.spec-key:contains("Cổng giao tiếp") + td.spec-value::text').getall()
        count = 0
        for ports_text in ports_texts:
            if ports_text:
                ports_text = ports_text.replace('<br>', ' ').replace(': ', '').strip().lower()
                if 'ethernet' in ports_text or 'rj45' in ports_text:
                    match = re.search(r"(\d+)x", ports_text)
                    if match:
                        count += int(match.group(1))
                    else:
                        count += 1
        return count


    def parse_number_audio_jacks(self, response):
        ports_texts = response.css('td.spec-key:contains("Cổng giao tiếp") + td.spec-value::text').getall()
        count = 0
        for ports_text in ports_texts:
            if ports_text:
                ports_text = ports_text.replace('<br>', ' ').replace(': ', '').strip().lower()
                if 'jack' in ports_text or 'headphone' in ports_text or 'microphone' in ports_text:
                    match = re.search(r"(\d+)x", ports_text)
                    if match:
                        count += int(match.group(1))
                    else:
                        count += 1
        return count

    def parse_battery_capacity(self, response):
        """
        Extracts the battery capacity in Whr from the response.
        """
        for battery_text in response.css('td:contains("Thông số pin") + td::text').getall(): 
            if battery_text: 
                battery_text = battery_text.lower().strip()
                match = re.search(r'(\d+\.?\d*)\s*(wh|whr|whrs|watt)', battery_text.lower())

                if match:
                    capacity = float(match.group(1))  # Extract the capacity value
                    return f"{capacity} whr"
                    
            return 'N/A'
    
    def parse_battery_cells(self, response):
        for battery_text in response.css('td:contains("Thông số pin") + td::text').getall(): 
            if battery_text: 
                battery_text = battery_text.lower().strip()
                match = re.search(r'(\d+\.?\d*)\s*(cell|cells)', battery_text.lower())

                if match:
                    capacity = float(match.group(1))  # Extract the capacity value
                    return f"{capacity} cell"
                    
            return 'N/A'
    
    def parse_warranty(self, response):
        warranty_text = response.css('td:contains("Bảo hành") + td::text').get()
        if warranty_text:
            # Match one or more digits in the text (e.g., "2 Year", "12 Months")
            match = re.search(r"(\d+)", warranty_text)
            if match:
                return float(match.group(1))  # Return the number as a float or int
        return 'N/A'

