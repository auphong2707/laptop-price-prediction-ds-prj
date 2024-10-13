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
        try:
            storage = self.get_scoped_value(response, ["Ổ cứng:"]).split(" ")
            if storage[1] == "TB":
                return int(storage[0]) * 1024
            else:
                return int(storage[0])
        except:
            return "N/A"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        try:
            return self.get_scoped_value(response, ["Ổ cứng:"]).split(" ")[2]
        except:
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            webcams = (self.get_scoped_value(response, ['Webcam'])).split("\n")
            if len(webcams) == 1:
                webcam = webcams[0].lower()
            else:
                for _ in webcams:
                    if "Camera trước:" in _:
                        webcam = _.lower()

            if any(term in webcam for term in ['qhd', '2k', '1440p', '2560x1440']):
                return 'QHD'
            elif any(term in webcam for term in ['fhd', '1080p', '1920x1080']):
                return 'FHD'
            elif any(term in webcam for term in ['hd', '720p', '1280x720']):
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
            return float(self.get_scoped_value(response, ["Màn hình:"]).replace('"', ''))
        except:
            return "N/A"
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            screen_res = self.get_scoped_value(response, ["Độ phân giải:"])
            search = re.search(r'(\d{3,4})\s*[x×]\s*(\d{3,4})', screen_res)
            if search:
                return search.group()
            else:
                return "N/A"
        except:
            return "N/A"

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        try:
            refresh_rate = self.get_scoped_value(response, ["Tần số quét:"])
            search = re.search(r'\d+\s*Hz', refresh_rate)
            if search:
                return int(search.group()[:-2])
            else:
                return "N/A"
        except:
            return "N/A"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        try:
            brightness = self.get_scoped_value(response, ["Công nghệ màn hình:"])
            search = re.findall(r'\d+\s*nits', brightness)
            if search:
                return max(int(nit.split()[0]) for nit in search)
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """ 
        try:
            battery = self.get_scoped_value(response, ["Thông tin Pin:"])
            search = re.search(r'(\d+(\.\d+)?)+\s*Wh', battery)
            if search:
                return float(search.group().replace("Wh", "").strip())
            else:
                return "N/A"
        except:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        try:
            battery = self.get_scoped_value(response, ["Thông tin Pin:"])
            search = re.search(r'(\d+)-?\s*cell', battery)
            if search:
                return int(search.group().split("-")[0].strip())
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Size
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước:"]).split(" - ")
            width = size[0].split(" ")
            if width[2] == "mm":
                return round(float(width[1]) / 10, 4)
            else:
                return float(width[1])
        except:
            return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước:"]).split(" - ")
            depth = size[1].split(" ")
            if depth[2] == "mm":
                return round(float(depth[1]) / 10, 4)
            else:
                return float(depth[1])
        except:
            return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước:"]).split(" - ")
            height = size[2].split(" ")
            if height[2] == "mm":
                return round(float(height[1]) / 10, 4)
            else:
                return float(height[1])
        except:
            return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        try:
            return float(self.get_scoped_value(response, ["Khối lượng tịnh:"]).split(" ")[0])
        except:
            return "N/A"
    
    # Connectivity
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        try:
            return self.get_scoped_value(response, ["Cổng giao tiếp:"])
        except:
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
        try:
            search = re.search(r'HDMI', self.get_scoped_value(response, ["Cổng giao tiếp:"]))
            return 1 if search else 0
        except:
            return "N/A"
    
    def parse_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        try:
            search = re.search(r'RJ-?45|Ethernet', self.get_scoped_value(response, ["Cổng giao tiếp:"]))
            return 1 if search else 0
        except:
            return "N/A"
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        try:
            search = re.search(r'Jack tai nghe', self.get_scoped_value(response, ["Cổng giao tiếp:"]))
            return 1 if search else 0
        except:
            return "N/A"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        try:
            os = self.get_scoped_value(response, ["Hệ điều hành:"]).split(" ")
            if os[0].lower() == "windows":
                return " ".join(os[:3])
            elif os[0].lower() == "macos":
                return "macOS"
            elif "linux" in os or "Linux" in os:
                return "Linux"
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        try:
            colors = response.xpath('//div[@class="box03 color group desk"]/a/text()').getall()
            return [color.strip() for color in colors]
        except:
            return "N/A"
    
    # Origin: Unavailable
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
        try:
            warranty = response.xpath('//ul[@class="policy__list"]/li[2]/p//text()').getall()
            warranty = warranty[1].split(" ")[-2:]
            if warranty[1] == "tháng":
                return int(warranty[0])
            else:
                return int(warranty[0]) * 12
        except:
            return "N/A"
    
    # Release Date
    def parse_release_date(self, response: Response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        try:
            year = self.get_scoped_value(response, ["Thời điểm ra mắt:"])
            if year == "Hãng không công bố":
                return "N/A"
            else:
                return "**/**/" + year
        except:
            return "N/A"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        try:
            prices = [
                response.xpath('//div[@class="bs_price"]/em/text()').get(), 
                response.xpath('//p[@class="box-price-present"]/text()').get()
            ]
            for price in prices:
                if price:
                    return int(price.replace(".", "").split("₫")[0])
        except:
            return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def parse(self, response: Response):
        yield {
            # 'brand': self.parse_brand(response), # Done
            'name': self.parse_name(response),    # Done
            # 'cpu': self.parse_cpu(response),    # Done
            # 'vga': self.parse_vga(response),  # Done
            # 'ram_amount': self.parse_ram_amount(response), # Done
            # 'ram_type': self.parse_ram_type(response), # Done
            # 'storage_amount': self.parse_storage_amount(response), # Done
            # 'storage_type': self.parse_storage_type(response), # Done
            # 'webcam_resolution': self.parse_webcam_resolution(response), # Done
            # 'screen_size': self.parse_screen_size(response), # Done
            # 'screen_resolution': self.parse_screen_resolution(response), # Done
            # 'screen_refresh_rate': self.parse_screen_refresh_rate(response), # Done
            # 'screen_brightness': self.parse_screen_brightness(response), # Done
            # 'battery_capacity': self.parse_battery_capacity(response), # Done
            # 'battery_cells': self.parse_battery_cells(response), # Done
            # 'width': self.parse_width(response), # Done
            # 'depth': self.parse_depth(response), # Done
            # 'height': self.parse_height(response), # Done
            # 'weight': self.parse_weight(response), # Done
            'number_usb_a_ports': self.parse_number_usb_a_ports(response),
            'number_usb_c_ports': self.parse_number_usb_c_ports(response),
            # 'number_hdmi_ports': self.parse_number_hdmi_ports(response), # Done
            # 'number_ethernet_ports': self.parse_number_ethernet_ports(response), # Done
            # 'number_audio_jacks': self.parse_number_audio_jacks(response), # Done
            # 'default_os': self.parse_default_os(response), # Done
            # 'color': self.parse_color(response),  # Done
            # 'origin': self.parse_origin(response), # Unavailable
            # 'warranty': self.parse_warranty(response), # Done
            # 'release_date': self.parse_release_date(response), # Done
            # 'price': self.parse_price(response) # Need checking
        }
        