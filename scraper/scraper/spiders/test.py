import scrapy
from scrapy.http import Response
import re

class Test(scrapy.Spider):
    name = "test"
    
    start_urls = [
        "https://gearvn.com/products/laptop-gaming-acer-predator-helios-neo-16-phn16-72-78dq",
        "https://gearvn.com/products/laptop-acer-swift-x14-sfx14-72g-77f9",
        "https://gearvn.com/products/macbook-pro-14-m2-pro-10cpu-16gpu-16gb-512gb-silver-mphh3sa-a",
        "https://gearvn.com/products/laptop-acer-swift-go-14-sfg14-73-57fz",
        "https://gearvn.com/products/laptop-gaming-hp-victus-16-s0142ax-9q989pa",
        "https://gearvn.com/products/laptop-gaming-asus-rog-zephyrus-g16-ga605wi-qr090ws",
        "https://gearvn.com/products/laptop-asus-vivobook-s-14-flip-tn3402ya-lz192w",
    ]
            
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//tr/td[contains(., '{}')]/following-sibling::td//span//text()".format(name)
                for name in names
            ] + [
                "//li/div[contains(., '{}')]/following-sibling::div/text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return ''.join(scope)
            
        return None
                
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            res = response.css('.product-name h1::text').get()
            
            if "Macbook" in res or "MacBook" in res:
                return "Apple"
            
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0]
        except:
            return "N/A"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            res = response.css('.product-name h1::text').get()
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            
            if "Macbook" in res:
                res = "Apple " + ' '.join(res.split()[:2] + res.split()[-1:])
            
            return res
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['CPU'])
            
            if self.parse_brand(response) == "Apple":
                res = re.sub(r'(\d+)CPU', r'\1 cores', res)
                res = re.sub(r'\s?\d+GPU', '', res)
                res = "Apple " + res
            else:
                res = res.split(' (')[0]
                
                for removal in ['®', '™', ' processor', ' Processor', 'Mobile']:
                    res = res.replace(removal, '')
                
                if 'GHz' in res:
                    res = ' '.join(res.split(' ')[:-1])
            
            return res.strip()
        except:
            return "N/A"
        
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['VGA', 'Card đồ họa'])
            
            if res in ["Intel® ARC™ Graphics", "AMD Radeon™ Graphics", None]:
                res = "N/A"
            else:
                for spliter in [' with ', ' Laptop ']:
                    res = res.split(spliter)[0]

                for removal in ['®', '™']:
                    res = res.replace(removal, '')

                if res.startswith('GeForce RTX'):
                    res = 'NVIDIA ' + res
                    
                res = re.sub(r'\d+GB|GDDR\d+', '', res)
                
            return res.strip()
        except:
            return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            res = self.get_scoped_value(response, ['RAM'])
            
            search_value = re.search(r'\d+GB', res)
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
            res = self.get_scoped_value(response, ['RAM'])
            
            search_value = re.search(r'DDR+\d', res)
            if search_value:
                res = search_value.group()
            else:
                res = "N/A"
            
            return res.strip()
        except:
            return "N/A"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ'])
        
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
            res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ'])
        
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
            
            return res.strip()
        except:      
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            res = ''.join(self.get_scoped_value(response, ['Webcam', 'Camera']).lower().split())

            if any(term in res for term in ['qhd', '2k', '1440p', '2560x1440']):
                return 'QHD'
            elif any(term in res for term in ['fhd', '1080p', '1920x1080']):
                return 'FHD'
            elif any(term in res for term in ['hd', '720p', '1280x720']):
                return 'HD'
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
            res = self.get_scoped_value(response, ['Màn hình'])
            res = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch)', res)
            
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
        Example: 1920x1080, 2560x1600, etc.
        """
        try:
            res = self.get_scoped_value(response, ['Màn hình'])
            
            res = ''.join(res.split())
            
            search_value = re.search(r'\d+x\d+', res)
            if search_value:
                res = search_value.group()
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    def parse_screen_ratio(self, response: Response): 
        """
        Extracts the screen ratio from the response.
        Example: 16:9, 16:10, 4:3.
        """
        
        value = self.parse_screen_resolution(response)
        if value != "N/A":
            value = value.split('x')
            
            if int(value[0]) / 16 == int(value[1]) / 9:
                res = "16:9"
            elif int(value[0]) / 16 == int(value[1]) / 10:
                res = "16:10"
            elif int(value[0]) / 4 == int(value[1]) / 3:
                res = "4:3"
            else:
                res = "N/A"
            
            return res
        else:
            return "N/A"
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Màn hình'])
            
            search_value = re.search(r'\d+\s*Hz', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('Hz')[0])
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
            res = self.get_scoped_value(response, ['Màn hình'])
            
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
            res = self.get_scoped_value(response, ['Pin'])
            res = res.lower()
            
            search_value = re.search(r'\d+\s*whr', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('whr')[0])
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
            res = self.get_scoped_value(response, ['Pin'])
            res = res.lower()
            search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells', res)
            
            if search_value:
                res = int(search_value.group()[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    # Size
    def parse_length(self, response: Response):
        """
        Extracts the length of the laptop in cm from the response.
        """
        try:
            
        except:
            return "N/A"
    
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        return "N/A"
    
    # Connectivity
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return "N/A"
    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return "N/A"
    
    def parse_number_hdmi_ports(self, response: Response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return "N/A"
    
    def parse_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return "N/A"
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        return "N/A"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        return "N/A"
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        return "N/A"
    
    # Origin
    def parse_origin(self, response: Response): 
        """
        Extracts the origin of the laptop from the response.
        Example: China, Taiwan, USA, etc.
        """
        return "N/A"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        return "N/A"
    
    # Release Date
    def parse_release_date(self, response: Response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        return "N/A"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def parse(self, response: Response):
        yield {
            # 'brand': self.parse_brand(response),
            'name': self.parse_name(response),
            # 'cpu': self.parse_cpu(response),
            # 'vga': self.parse_vga(response),
            # 'ram_amount': self.parse_ram_amount(response),
            # 'ram_type': self.parse_ram_type(response),
            # 'storage_amount': self.parse_storage_amount(response),
            # 'storage_type': self.parse_storage_type(response),
            # 'webcam_resolution': self.parse_webcam_resolution(response),
            # 'screen_size': self.parse_screen_size(response),
            # 'screen_resolution': self.parse_screen_resolution(response),
            # 'screen_ratio': self.parse_screen_ratio(response),
            # 'screen_refresh_rate': self.parse_screen_refresh_rate(response),
            # 'screen_color_gamut': self.parse_screen_color_gamut(response),
            # 'screen_brightness': self.parse_screen_brightness(response),
            'battery_capacity': self.parse_battery_capacity(response),
            'battery_cells': self.parse_battery_cells(response),
            # 'length': self.parse_length(response),
            # 'width': self.parse_width(response),
            # 'height': self.parse_height(response),
            # 'weight': self.parse_weight(response),
            # 'number_usb_a_ports': self.parse_number_usb_a_ports(response),
            # 'number_usb_c_ports': self.parse_number_usb_c_ports(response),
            # 'number_hdmi_ports': self.parse_number_hdmi_ports(response),
            # 'number_ethernet_ports': self.parse_number_ethernet_ports(response),
            # 'number_audio_jacks': self.parse_number_audio_jacks(response),
            # 'default_os': self.parse_default_os(response),
            # 'color': self.parse_color(response),
            # 'origin': self.parse_origin(response),
            # 'warranty': self.parse_warranty(response),
            # 'release_date': self.parse_release_date(response),
            # 'price': self.parse_price(response)
        }