import scrapy
from scrapy.http import Response
import re

class ThegioididongSpider(scrapy.Spider):
    
    name = "test_spider"
    
    start_urls = [
        'https://www.thegioididong.com/laptop/dell-inspiron-15-3520-i5-n5i5052w1',
        "https://www.thegioididong.com/laptop/apple-macbook-air-2020-mgn63saa",
        "https://www.thegioididong.com/laptop/asus-vivobook-go-15-e1504fa-r5-nj776w?utm_flashsale=1",
        "https://www.thegioididong.com/laptop/surface-pro-9-i7-512",
        "https://www.thegioididong.com/laptop/macbook-pro-14-inch-m3-2023",
        "https://www.thegioididong.com/laptop/acer-aspire-a515-58gm-53pz-i5-nxkq4sv008?utm_recommendation=1",
    ]
    
    
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//ul/li[contains(., '{}')]//aside[2]//text()".format(name)
                for name in names
            ]
        
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return "".join(scope).strip()
            
        return None
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            brand =  response.xpath('//ul[@class="breadcrumb"]/li[2]/a/text()').get().split(" ")[1]
            if brand == "Surface":
                return "Microsoft"
            return brand
        except:
            return "N/A"
    
    def parse_name(self, response: Response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            fullname = response.xpath('//div[@class="product-name"]/h1/text()').get()
            
            id = re.search(r'\(([^)]+)\)', fullname)
            if id:
                id = id.group(1)
            else:
                id = ""
            
            for _ in ["i3", "i5", "i7", "i9", "R3", "R5", "R7", "R9"]:
                if _ in fullname:
                    fullname = fullname.split(_)[0].strip()
                    break
            name = fullname.replace("Laptop", "").strip()
            name = re.sub(r'\d+(\.\d+)? inch.*', '', name).strip()
            
            return name + " " + id
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            return self.get_scoped_value(response, ["Công nghệ CPU:"]).split(" - Hãng không công bố")[0].replace(" - ", "-")
        except:
            return "N/A"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            vga = self.get_scoped_value(response, ["Card màn hình:"])
            for _ in ["Card tích hợp", "Hãng không công bố"]:
                if _ in vga:
                    return "N/A"
            return vga.split("-")[1].split(",")[0].strip()
        except:
            return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            ram = self.get_scoped_value(response, ["RAM:"])
            return int(ram.split("\n")[0].split("GB")[0].strip())
        except:
            return "N/A"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        try:
            ram_type = self.get_scoped_value(response, ["Loại RAM:"])
            if ram_type == "Hãng không công bố":
                return "N/A"
            else:
                return ram_type.split()[0].replace("LP", "")
        except:
            return "N/A"
    
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
            # 'brand': self.parse_brand(response), # Done
            # 'name': self.parse_name(response),    # Done
            # 'cpu': self.parse_cpu(response),    # Done
            # 'vga': self.parse_vga(response),  # Done
            # 'ram_amount': self.parse_ram_amount(response), # Done
            # 'ram_type': self.parse_ram_type(response), # Done
            'storage_amount': self.parse_storage_amount(response),
            'storage_type': self.parse_storage_type(response),
            # 'webcam_resolution': self.parse_webcam_resolution(response),
            # 'screen_size': self.parse_screen_size(response),
            # 'screen_resolution': self.parse_screen_resolution(response),
            # 'screen_ratio': self.parse_screen_ratio(response),
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
        