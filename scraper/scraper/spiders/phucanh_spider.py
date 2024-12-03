from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider

# create scraper
class PhucanhShopSpider(BaseLaptopshopPageSpider): 
    name = "phucanh_spider"
    start_urls = ['https://www.phucanh.vn/laptop.html']  
    product_site_css = '.p-img::attr(href)'  # Example CSS selector to extract links to products
    page_css = 'div.paging a::attr(href)'
    allowed_domains = ['phucanh.vn']
    
    source = 'phucanh'
    
    def get_scoped_value(self, response, names):
        possibile_values = [
               "//table[contains(@class, 'tb-product-spec')]//tr//td[text()='{}']/following-sibling::td//text()".format(name)
               for name in names
            ] + [
                "//div[@id='fancybox-spec']//table[contains(@class, 'tb-product-spec')]//tr//td[text()='{}']/following-sibling::td//text()".format(name)
                for name in names
            ] + [
                "//div//strong[contains(text(), '{}')]/following-sibling::text()[1]".format(name)
                for name in names
            ]

        for value in possibile_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return '\n'.join(scope)
            
        return None

    def parse_brand(self, response:Response):
        # Extract the full product title
        product_title = response.css('h1::text').get()

        # Split the title by spaces and get the first word (brand)
        if product_title:
            brand = product_title.split()[1]  # Assuming the brand is always the second word after "Laptop"
        else:
            brand = 'n/a'

        return brand
    
    def parse_name(self, response:Response):
        # Extract the full product title
        product_name = response.css('h1::text').get()
        return product_name if product_name else 'n/a'

    def parse_price(self, response:Response):
        # Extract the price with the currency symbol
        try:
            price_text = response.css('span.detail-product-old-price::text').get()
            if not price_text:
                price_text = response.css('span.detail-product-best-price::text').get()
            return price_text if price_text else 'n/a'
        except Exception as e:
            print('Error while trying to find the price:', e)
            return 'n/a'
        
        # if price_text:
        #     # Remove dots and currency unit (like "đ")
        #     price = price_text.replace('.', '').split()[0].strip()
        # else:
        #     price = 'N/A'
        
    def parse_cpu(self, response: Response):
        cpu_text = self.get_scoped_value(response, ['Bộ VXL'])
        return cpu_text if cpu_text else 'n/a'
        # if cpu_text: 
        #     if ': ' in cpu_text: 
        #         cpu_text = cpu_text.replace(': ', '').lower()
        #         cpu_text = re.sub(r"\d+(\.\d+)?\s*ghz", "", cpu_text).strip()
                
        #         # Apple
        #         if 'apple' in cpu_text: 
        #             cpu_text = cpu_text.replace(' cpu', '').strip()
                
        #         # Intel
        #         elif 'core' in cpu_text or 'ultra' in cpu_text: 
        #             cpu_text = 'intel ' + cpu_text
                
        #     return cpu_text

        # return 'N/A'
    def parse_vga(self, response):
        vga_text = self.get_scoped_value(response, ['Card màn hình'])
        return vga_text if vga_text else 'n/a'
        # if vga_text:
        #     vga_text_lower = vga_text.strip().lower() # Normalize for easier comparison
        #     if "intel" in vga_text_lower and ("graphics" in vga_text_lower or "hd graphics" in vga_text_lower): # Check for common integrated graphics patterns
        #         return "N/A"  # Onboard Intel graphics
        #     elif "amd radeon graphics" in vga_text_lower or "amd radeon" in vga_text_lower: # Check for common integrated AMD graphics patterns
        #         return "N/A" # Onboard AMD graphics
        #     elif 'onboard' in vga_text_lower.lower():
        #         return "N/A"
        #     elif not vga_text_lower: # Handles cases where the selector doesn't find anything
        #         return "N/A"
        #     else:
        #         if 'vga nvidia - ' in vga_text_lower: 
        #             vga_text = vga_text.replace('VGA Nvidia - Nvidia ', '') # Dedicated graphics card
        #         if 'vga amd - ' in vga_text_lower:
        #             vga_text = vga_text.replace('VGA AMD - AMD ', '')
        #         if ': ' in vga_text: 
        #             vga_text = vga_text.replace(': ', '')
        #         return vga_text
        # else:
        #     return "N/A" # Value not found
    def parse_ram_amount(self, response):
        ram_text = self.get_scoped_value(response, ['Dung lượng RAM'])
        return ram_text if ram_text else 'n/a'
        # if ram_text: 
        #     return ram_text.split()[1]
        # return 'N/A'
    
    def parse_ram_type(self, response):
        ram_text = self.get_scoped_value(response, ['Loại RAM'])
        return ram_text if ram_text else 'n/a'
        # if ram_text:
        #     # Capture the "ddr" followed by a digit
        #     match = re.search(r"(ddr\d+)", ram_text.lower())
        #     if match:
        #         return match.group(1)  # Return the full match
        # return 'N/A'
    
    def parse_storage_amount(self, response):
        storage_text = self.get_scoped_value(response, ['Dung lượng ổ cứng'])
        return storage_text if storage_text else 'n/a'

        # if storage_text:
        #     # Clean up the storage text by removing ' SSD', ' HDD', and ': ' if they exist
        #     storage_text = storage_text.replace(' SSD', '').replace(' HDD', '').replace(': ', '').strip()
            
        #     return storage_text

        # return 'N/A'

    def parse_storage_type(self, response): 
        storage_text = self.get_scoped_value(response, ['Loại ổ cứng'])
        return storage_text if storage_text else 'n/a' 
    
    def parse_screen_resolution(self, response):
        screen_text = self.get_scoped_value(response, ['Độ phân giải'])
        return screen_text if screen_text else 'n/a'

        # if screen_text:
        #     match = re.search(r"\((\d+x\d+)\)", screen_text)
        #     if match: 
        #         return match.group(1)
        # return 'N/A'
    
    def parse_screen_size(self, response):
        screen_text = self.get_scoped_value(response, ['Kích thước màn hình'])
        return screen_text if screen_text else 'n/a'

        # if screen_text:
        #     # Extract just the resolution part (e.g., "Full HD")
        #     screen_text = screen_text.strip() # Remove leading/trailing whitespace
        #     parts = screen_text.split() # Split into parts based on spaces
        #     if len(parts) > 1: # Check if there's a resolution part (after the size)
        #         size  = " ".join(parts[:2]) # Join the size parts back together
        #         if ': ' in size: 
        #             size = size.replace(': ', '')
        #         return size 
        # return 'N/A'

    
    
    def parse_size(self, response: Response):  
        size_text = self.get_scoped_value(response, ['Kích thước'])
        return size_text if size_text else 'n/a'
        # for dimension_text in response.css('td:contains("Kích thước") + td.spec-value::text').getall():
        #     if dimension_text:
        #         dimension_text = dimension_text.strip()
        #         return dimension_text
                
                # # Improved regex to capture potential extra text or units before and after dimensions
                # match = re.search(r"(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*(cm|mm)", dimension_text, re.IGNORECASE)
                # if match:
                #     length, _, width, _, height, _, unit = match.groups()
                #     try:
                #         length = float(length)
                #         width = float(width)
                #         height = float(height)
                        
                #         # Convert cm to mm if necessary
                #         if unit.lower() == 'cm':
                #             length *= 10
                #             width *= 10
                #             height *= 10
                            
                #         return length, width, height  # Return dimensions in millimeters
                    
                #     except ValueError:
                #         # Log or raise an error in real use case; print for now
                #         print(f"Error converting dimension to float: {dimension_text}")
                        
        # Return None if extraction fails
        # return None, None, None
    
    def parse_weight(self, response):
        weight_text = self.get_scoped_value(response, ['Trọng lượng'])
        return weight_text if weight_text else 'n/a'
    
    def parse_default_os(self, response):
        os_text = self.get_scoped_value(response, ['Hệ điều hành'])
        return os_text if os_text else 'n/a'
        # default_os_text = response.css('td:contains("Hệ điều hành") + td::text').get() 
        # if default_os_text: 
        #     return default_os_text
        #     # return default_os_text.replace(': ', '')

        # return 'N/A'
    
    def parse_color(self, response):
        color_text = self.get_scoped_value(response, ['Màu sắc'])
        return color_text if color_text else 'n/a'
        # color_text = response.css('td:contains("Màu sắc") + td::text').get() 
        # if color_text: 
        #     return color_text
        #     # return color_text.lower().replace(': ', '')
        
        # return 'N/A'
    
    def parse_connectivity(self, response):
        connectivity_text = self.get_scoped_value(response, ['Cổng giao tiếp'])
        connectivity_text = connectivity_text[:len(connectivity_text) // 2]
        return connectivity_text if connectivity_text else 'n/a'

    def parse_battery_capacity(self, response):
        """
        Extracts the battery capacity in Whr from the response.
        """
        battery_text = self.get_scoped_value(response, ['Thông số pin'])
        return battery_text if battery_text else 'n/a'
    
    def parse_battery_cells(self, response):
        battery_text = self.get_scoped_value(response, ['Thông số pin'])
        return battery_text if battery_text else 'n/a'
        # for battery_text in response.css('td:contains("Thông số pin") + td::text').getall(): 
        #     if battery_text: 
        #         battery_text = battery_text.lower().strip()
        #         match = re.search(r'(\d+\.?\d*)\s*(cell|cells)', battery_text.lower())

        #         if match:
        #             capacity = float(match.group(1))  # Extract the capacity value
        #             return f"{capacity} cell"
                    
        #     return 'N/A'
    
    def parse_warranty(self, response):
        warranty_text = self.get_scoped_value(response, ['Bảo hành'])
        return warranty_text if warranty_text else 'n/a'
        # warranty_text = response.css('td:contains("Bảo hành") + td::text').get()
        # if warranty_text:
        #     # Match one or more digits in the text (e.g., "2 Year", "12 Months")
        #     match = re.search(r"(\d+)", warranty_text)
        #     if match:
        #         return float(match.group(1))  # Return the number as a float or int
        # return 'N/A'

    def parse_screen_brightness(self, response):
        screen_text = self.get_scoped_value(response, ['Công nghệ màn hình'])
        return screen_text if screen_text else 'n/a'
    
    def parse_screen_refresh_rate(self, response):
        screen_text = self.get_scoped_value(response, ['Tần số quét', 'Công nghệ màn hình'])
        return screen_text if screen_text else 'n/a'
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ["Webcam"])
        return res if res else "n/a"