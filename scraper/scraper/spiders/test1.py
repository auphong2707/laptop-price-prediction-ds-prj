import scrapy
from scrapy.http import Response
import re

class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ["laptopaz.vn"]
    start_urls = [
        'https://laptopaz.vn/new-100-hp-envy-x360-2-in-1-14-fa0023dx-2024-ryzen-7-8840hs-16gb-1tb-14quot-fhd-touch.html',
        'https://laptopaz.vn/new-100-asus-rog-flow-x13-gv302xa-x13.r9512-ryzen-9-7940hs-16gb-512gb-amd-radeon-780m-13.4-fhd-ips-120hz-touch.html',
        'https://laptopaz.vn/like-new-lenovo-geekpro-g5000-ryzen-7-7840h-16gb-512gb-rtx-4050-6gb-15.6quot-2k-165hz.html',
        'https://laptopaz.vn/dell-inspiron-14-5430-core-i5-1340p-16gb-512gb-iris-xe-graphics-14quot-fhd.html',
    ]
    
    def get_scoped_value(self, response: Response, names):
        possibile_values = [
                "//tr[td/span/strong[contains(text(), '{}')]]/td[2]/span/text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return '\n'.join(scope)
            
        return None
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            res = response.css('.box-product-name h1::text').get()
            
            if "Macbook" in res or "MacBook" in res:
                return "Apple"
            
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0]
        except Exception:
            return "N/A"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            full_text = response.css("h1.bg-white.border-bottom.mb-0.p-3.text-18.title.w-100.bk-product-name::text").get()
            return re.sub(r"\[.*?\]|\(.*?\)|\b\d{4}\b", "", full_text).strip()
        except Exception:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        return "N/A"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        return self.get_scoped_value(response, ['RAM'])
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        return response.xpath("//div[text()='Ram']/following-sibling::div/text()").get()
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        return "N/A"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        return "N/A"
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        return "N/A"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        return "N/A"
    
    # Size
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
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
            'ram_amount': self.parse_ram_amount(response),
            # 'ram_type': self.parse_ram_type(response),
            # 'storage_amount': self.parse_storage_amount(response),
            # 'storage_type': self.parse_storage_type(response),
            # 'webcam_resolution': self.parse_webcam_resolution(response),
            # 'screen_size': self.parse_screen_size(response),
            # 'screen_resolution': self.parse_screen_resolution(response),
            # 'screen_refresh_rate': self.parse_screen_refresh_rate(response),
            # 'screen_brightness': self.parse_screen_brightness(response),
            # 'battery_capacity': self.parse_battery_capacity(response),
            # 'battery_cells': self.parse_battery_cells(response),
            # 'width': self.parse_width(response),
            # 'depth': self.parse_depth(response),
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