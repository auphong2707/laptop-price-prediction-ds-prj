import re
from requests import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider


class CellphoneSpider(BaseLaptopshopLoadmoreButtonSpider):
    name = "cellphones"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = [
        'https://cellphones.com.vn/laptop.html',
    ]
    
    product_site_css = 'div.product-info a::attr(href)'
    loadmore_button_css = '.btn-show-more'
    close_button_xpaths = ["//button[@class='cancel-button-top']"]
    show_technical_spec_button_xpath = "//button[contains(@class, 'button__show-modal-technical')]"
    selenium_product_request = True
    
    def get_scoped_value(self, response: Response, names):
        possibile_values = [
                "//li[contains(@class, 'technical-content-modal-item')]//p[text()='{}']/following-sibling::div[1]//text()".format(name)
                for name in names
            ] + [
                "//li[contains(@class, 'technical-content-modal-item')]//p[a[text()='{}']]/following-sibling::div[1]//text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return '\n'.join(scope)
            
        return None
    
    def yield_condition(self, response):
        name = response.css('.box-product-name h1::text').get().lower()
        price = response.css('.product__price--show::text').get()
        if 'cũ' in name \
            or ('mac' in name and 'macbook' not in name) \
            or 'đã kích hoạt' in name \
            or (price is not None and 'Giá Liên Hệ' in price):
            print(f"Skipped: {name}")
            return False
        return True
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            res = response.css('.box-product-name h1::text').get().lower()
            
            if "mac" in res:
                return "apple"
            
            for removal in ['laptop gaming ', 'laptop Gaming ', 'laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0].lower()
        except:
            return "N/A"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            res = response.css('.box-product-name h1::text').get().lower()
            for removal in ['laptop gaming ', 'laptop ', '- chỉ có tại cellphones', 'i chính hãng apple việt nam', ' - nhập khẩu chính hãng']:
                res = res.replace(removal, '')

            res = re.sub(r'\([^()]*\)', '', res)
            search_value = re.search('(?<!\w)(\d+)gb(?!\w)', res)
            if search_value:
                res = res.split(search_value.group())[0]
            
            return res.strip()
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Loại CPU']).lower()
            
            for removal in ['®', '™', ' processors', ' processor', 'mobile', 'with intel ai boost', '', '(tm)', '(r)', 
                            'tiger lake', 'ice lake', 'raptor lake', 'alder lake', 'comet lake', 'kabylake refresh', 'kabylake']:
                    res = res.replace(removal.lower(), '')
            
            special_sep = re.search(r'\b(\d+\.\d+\s?upto\s?\d+\.\d+ghz|\d+(\.\d+)?\s*ghz|\d+\s?gb|dgb)\b', res)
            if special_sep:
                res = res.split(special_sep.group())[0]
            
            for spliter in [',',  'up',]:
                res = res.split(spliter)[0]
            
            res = ' '.join(res.split())
            if self.parse_brand(response) == "apple":
                cpu_name = re.search(r'm\d+(\s+pro|\s+max)?', res, re.IGNORECASE)
                if cpu_name:
                    # Update the pattern to be more general for core counting and fix the encoding issue
                    pattern = re.compile(r'(\d+)\s*(lõi|nhân|core|-core)', re.IGNORECASE)
                    num_cores = pattern.search(res)
                    if num_cores:
                        num_cores = num_cores.group(1)  # The number of cores will be in the first group
                        res = f"apple {cpu_name.group(0)} {num_cores}-core"
                    else:
                        res = f"apple {cpu_name.group(0)}"
                
            else:
                res = re.sub(r'\([^()]*\)', '', res)
                
                # Intel solving
                if any(keyword in res.lower() for keyword in ['i5', 'i7', 'i9', 'i3']):
                    
                    pattern = re.compile(r'(i\d)\s*[- ]?\s*(\d{4,5})([a-z]{0,2})')
                    match = pattern.search(res)
                
                    if match:
                        # Format the matched processor name as "iX-XXXXXH"
                        res = 'intel core ' + f"{match.group(1)}-{match.group(2)}{match.group(3)}"
                elif "ultra" in res.lower():
                    pattern = re.compile(r'(?:ultra\s*)?(u?\d)\s*[- ]?\s*(\d{3})([a-z]?)')
                    match = pattern.search(res)
                    
                    if match:
                        model_number = match.group(1).replace('u', '')
                        res = 'intel core ' + f"ultra {model_number} {match.group(2)}{match.group(3)}"
                
                # AMD solving
                elif "ryzen" in res.lower():
                    pattern = re.compile(r'(?:ryzen\s*)?(\d)\s*[- ]?\s*(\d{4})([a-z]{0,2})')
                    
                    match = pattern.search(res)
                    
                    if match:
                        res = 'amd ' f"ryzen {match.group(1)} {match.group(2)}{match.group(3)}"
                        
                # Snapdragon solving
                elif "snapdragon" in res.lower():
                    pattern = r'([A-Za-z]+\s+\d+\s+\d+)'
                    
                    # Define a function to replace spaces with hyphens in the matched string
                    def replace_with_hyphens(match):
                        # Split the matched string into components and join with hyphens
                        components = match.group(0).split()
                        return '-'.join(components)
                    
                    # Substitute the pattern in the input string using re.sub
                    res = re.sub(pattern, replace_with_hyphens, res)
                    
            return res.strip()
        except:
            return "N/A"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Loại card đồ họa']).lower()
            
            res = re.sub(r'[^\x20-\x7E]|®|™|integrated|gpu', ' ', res, flags=re.IGNORECASE)              
            res = re.sub(r'\([^()]*\)', '', res)
            
            special_sep = re.search(r'\d+\s?gb|gddr\d+|\d+g', res)
            if special_sep:
                res = res.split(special_sep.group())[0]
            
            for spliter in [' with ', ' laptop ', '+', ',',  'up', 'upto', 'up to', 'rog']:
                res = res.split(spliter)[0]
            
            res = ' '.join(res.split())
    
            if self.parse_brand(response) == "apple":
                res = 'N/A'
            else:
                if any([keyword in res.lower() for keyword in ['nvidia', 'geforce', 'rtx', 'gtx']]):
                    for removal in ['amd radeon graphics', 'intel uhd graphics', 'laptop', 'nvidia', 'intel iris xe']:
                        res = res.replace(removal, '')
                        res = ' '.join(res.split())
                    
                    if res.startswith('rtx') or res.startswith('gtx'):
                        res = 'geforce ' + res
                        
                    res = re.sub(r'(\s\d{3,4})ti', r'\1 ti', res)
                    res = re.sub(r'(tx)(\d{4})', r'\1 \2', res)
                elif any([keyword in res for keyword in ['iris xe', 'intel uhd', 'intel hd', 'intel graphics', 'intel arc', 'adreno']]):
                    res = "N/A"
                elif any([keyword in res for keyword in ['amd', 'radeon']]):
                    res = res.replace('amd', '')
                    
                    if 'vega' in res:
                        res = "N/A"
                    elif not 'rx' in res:
                        res = "N/A"
                    
            return res.strip()
        except:
            return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Dung lượng RAM'])
            
            search_value = re.search(r'\d+\s?GB', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('GB')[0])
            
            return res
        except:
            return "N/A"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        try:
            res = self.get_scoped_value(response, ['Loại RAM'])
            
            search_value = re.search(r'DDR+\d', res)
            if search_value:
                res = search_value.group()
            else:
                res = "N/A"
            
            return res.strip().lower()
        except:
            return "N/A"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Ổ cứng'])
            res = ''.join(res.split())
        
            search_value = re.search(r'\d+GB|\d+TB', res)
            if search_value:
                res = search_value.group()
                if 'TB' in res:
                    res = int(res.split('TB')[0]) * 1024
                else:
                    res = int(res.split('GB')[0])
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        try:
            
            for name in ['Ổ cứng', 'Tính năng đặc biệt']:
                res = self.get_scoped_value(response, [name])
            
                if "SSD" in res and "HDD" in res:
                    if res.index("SSD") < res.index("HDD"):
                        res = "SSD"
                    else:
                        res = "HDD"
                elif "SSD" in res:
                    res = "SSD"
                elif "HDD" in res:
                    res = "HDD"
                else:
                    res = "N/A"

                if res != "N/A":
                    break
            
            return res.strip().lower()
        except:      
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            res = ''.join(self.get_scoped_value(response, ['Webcam']).lower().split())

            if any(term in res for term in ['qhd', '2k', '1440p', '2560x1440']):
                return 'qhd'
            elif any(term in res for term in ['fhd', '1080p', '1920x1080']):
                return 'fhd'
            elif any(term in res for term in ['hd', '720p', '1280x720']):
                return 'hd'
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước màn hình']).lower()
            res = res.replace(',', '.')
            res = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch|”)', res)
            
            if res:
                res = float(res.group(1))
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
        
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            res = ''.join(self.get_scoped_value(response, ['Độ phân giải màn hình']).lower().split())
            res = res.replace('*', 'x')
            
            search_value = re.search(r'(\d{3,4})x(\d{3,4})', res)
            if search_value:
                width, height = sorted(map(int, search_value.groups()), reverse=True)
                res = f"{width}x{height}"
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Tần số quét']).lower()
            
            search_value = re.search(r'\d+\s*hz', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('hz')[0])
            else:
                res = "N/A"

            return res
        except:
            return "N/A"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Công nghệ màn hình']).lower()
            
            search_value = re.search(r'\d+\s*nits', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('nits')[0])
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Pin']).lower().replace(',', '.')
            res = re.sub(r'[()]', '', res)
        
            search_value = re.search(r'(\d+(?:\.\d+)?)\s*(wh|battery)', res)
            if search_value:
                res = float(search_value.group().split('wh')[0].split('battery')[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Pin']).lower()
            
            search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells|Chân\s*(\d+)', res)
            
            if search_value:
                res = int(search_value.group()[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    # Size
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')

            numbers = re.findall(r'\d+\.?\d*', res)
            
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[0]
            res = res if res < 100 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')

            numbers = re.findall(r'\d+\.?\d*', res)
            
            # Collect the first three numbers and any number after a hyphen
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[1]
            res = res if res < 100 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')
            
            numbers = re.findall(r'\d+\.?\d*', res)
            
            # Collect the first three numbers and any number after a hyphen
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[2]
            res = res if res < 5 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Trọng lượng']).lower()
            res = res.replace(',', '.')
        
            value_kg = re.search(r'(\d+(\.\d+)?)\s*(kg)', res)
            value_g = re.search(r'(\d+(\.\d+)?)\s*(gram|g)', res)
            
            if value_kg:
                res = float(value_kg.group(1))
            elif value_g:
                res = float(value_g.group(1)) / 1000
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    # Connectivity
    def parse_number_usb(self, response: Response, pattern_a: str, pattern_c: str, get_a=True):
        try:
            res = self.get_scoped_value(response, ['Cổng giao tiếp'])
            res = res.lower()
            if re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE) != '':
                res = re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE)
            
            while '(' in res and ')' in res:
                res = re.sub(r'\([^()]*\)', '', res)
            
            res = re.split(r'[\n,]', res)
            count = 0
            for line in res:
                if get_a:
                    if re.search(pattern_a, line) and not re.search(pattern_c, line):
                        line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                        val = line.split()[0]
                        if val[-1] == 'x': val = val[:-1]
                
                        if val.isnumeric():
                            count += int(val)
                        else:
                            count += 1
                else:
                    if re.search(pattern_c, line):
                        line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                        val = line.split()[0]
                        if val[-1] == 'x': val = val[:-1]
                
                        if val.isnumeric():
                            count += int(val)
                        else:
                            count += 1
            
            return count
        except:
            return "N/A"
    
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return self.parse_number_usb(response, 
                                     r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b',  
                                     r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b',
                                     get_a=True)

    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return self.parse_number_usb(response, 
                                     r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b',  
                                     r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b',
                                     get_a=False)
    
    def parse_has_port(self, response: Response, pattern):
        try:
            res = self.get_scoped_value(response, ['Cổng giao tiếp'])
            res = res.lower()
            
            if res:
                port_search = re.search(pattern, res)
                return 1 if port_search else 0
            else:
                return "N/A"
            
        except:
            return "N/A"
    
    def parse_number_hdmi_ports(self, response: Response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return self.parse_has_port(response, r'\bhdmi\b')
    
    def parse_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return self.parse_has_port(response, r'\brj-45|ethernet\b')
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        return self.parse_has_port(response, r'\bheadphone|3.5mm\b')
    
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        try:
            res = self.get_scoped_value(response, ['Hệ điều hành']).lower()
            
            for removal in ['single language', 'sl', '64', 'bit', 'sea', 'microsoft', 'office']:
                res = res.replace(removal, '')
            res = ' '.join(res.split())
            
            res.replace('win ', 'windows ')
            
            search_value = re.search(r"windows\s+\d{1,2}(\.\d+)?(\s+\w+)?(\s+\w+)?", res)
            if search_value:
                res = search_value.group()
            elif self.parse_brand(response) == "apple":
                res = "macos"
            elif res == 'không hệ điều hành':
                res = "N/A"
            
            return res.strip()
        except:
            return "N/A"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        try:
            res = response.xpath("//a[@href='https://cellphones.com.vn/chinh-sach-bao-hanh']/\
                                 parent::div[contains(@class, 'description')]/text()[1]").get()
                
            res = ' '.join(res.split()).lower()
            search_value = re.search(r'(\d+)\s*tháng', res)
    
            if search_value:
                res = int(search_value.group(1))
            else:
                res = "N/A"
            
            return res
            
        except:
            return "N/A"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        try:
            if response.css('.tpt---sale-price::text').get():
                price = response.css('.tpt---sale-price::text').get()
            elif response.css('.product__price--show::text').get():
                price = response.css('.product__price--show::text').get()
            
            if price:
                price = price.replace('đ', '').replace('.', '').strip()
                return int(price)
            else:
                return "N/A"
        except:
            return "N/A"
    
    # [PARSE FEATURES SECTION: END]