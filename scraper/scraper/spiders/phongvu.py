from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
import re

class GearvnSpider(BaseLaptopshopLoadmoreButtonSpider):
    selenium_product_request = True
    
    name = "phongvu"
    allowed_domains = ["phongvu.vn"]
    start_urls = [
        'https://phongvu.vn/c/laptop',
    ]

    product_site_css = "a.css-pxdb0j::attr(href)"
    loadmore_button_css = '.css-b0m1yo'
    close_button_xpaths = ["//div[@class='css-73p2ms']/span"]

    def get_scoped_value(self, response, names):
        possibile_values = [
            "//div[@class='css-1lchwqw' and text()='{}']/following-sibling::div[@class='css-1lchwqw']".format(name)
            for name in names
        ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return "".join(scope).strip()
        
        return None

    
    # [PARSE FEATURES SECTION: START]
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            full_text = response.css('h1.css-nlaxuc::text').get()
            return re.sub(r'\s*\(.*?\)', '', full_text).strip()
        except Exception:
            return "N/A"

    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            return self.get_scoped_value(response, ['Thương hiệu:'])
        except Exception:
            return "N/A"

    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            full_text = self.get_scoped_value(response, ['CPU:'])
            return re.sub(r'\s*\(.*?\)', '', full_text).strip()
        except Exception:
            return "N/A"

    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            return self.get_scoped_value(response, ['Chip đồ họa:'])
        except Exception:
            return "N/A"

        # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            ram = self.get_scoped_value(response, ["RAM:", "Dung lượng RAM:"])
            index = ram.find("GB")
            return ram[:index].strip()
        except Exception:
            return "N/A"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        try:
            ram_type = self.get_scoped_value(response, ["RAM:"])
            if ram_type.split().includes("Onboard"):
                index = ram_type.split().index("Onboard")
                return ram_type.split()[index + 1]
            elif ram_type.split().includes("Onbard"):
                index = ram_type.split().index("Onbard")
                return  ram_type.split()[index + 1]
            else:
                index = -1
                for i, word in enumerate(ram_type.split()):
                    if "GB" in word:
                        index = i
                    break
                return ram_type.split()[index + 1]
        except Exception:
            return "N/A"
    
    # Storage
    def parse_storage_amount(self, response: Response):
        """
        Extracts the amount of storage in GB from the response.
        """
        try:
            storage = self.get_scoped_value(response, ["Dung lượng SSD:", "Lưu trữ"]).split(" ")
            if "TB" in storage[0]:
                return int(storage[0].strip('TB')) * 1024
            else:
                return int(storage[0].strip('GB'))
        except Exception:
            return "N/A"
    
    def parse_storage_type(self, response: Response):
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        try:
            return self.get_scoped_value(response, ["Dung lượng SSD:", "Lưu trữ"]).split(" ")[1]
        except Exception:
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            if self.get_scoped_value(response, ["Thương hiệu:"]) == "APPLE":
                return self.get_scoped_value(response, ["Màn hình:"]).split()[-2]
            else:
                return self.get_scoped_value(response, ["Webcam:"]).strip("Webcam")  
        except Exception:
            return "N/A"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        try:
            return self.get_scoped_value(response, ["Màn hình:"]).split()[0]
        except Exception:
            return "N/A"
        
    def parse_screen_resolution(self, response: Response):
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            screen_res = self.get_scoped_value(response, ["Màn hình"])
            pattern = r"\d+\s*x\s*\d+"
            match = re.search(pattern, screen_res)
            if match:
                resolution = match.group()
            return resolution
        except Exception:
            return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response: Response):
        """
        Extracts the battery capacity in Whr from the response.
        """
        try:
            battery = self.get_scoped_value(response, ["Công suất pin:", "Pin:"])
            search = re.search(r'(\d+(\.\d+)?)+\s*Wh', battery)
            if search:
                return float(search.group().replace("Wh", "").strip())
            else:
                return "N/A"
        except Exception:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        try:
            battery = self.get_scoped_value(response, ["Công suất pin:", "Pin:"])
            search = re.search(r'(\d+)-?\s*cell', battery)
            if search:
                return int(search.group().split(" ")[0].strip())
            else:
                return "N/A"
        except Exception:
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
            height = size[2]
            if '~' in height:
                return round(float(height.split("~")[1].split(" ")[1]) / 10, 4)
            else:
                return round(float(height[1]) / 10, 4)
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
            return self.parse_number_usb(response, r'\b(usb 2\.0|usb 3\.2)\b')
        except:
            return "N/A"
    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        try:
            return self.parse_number_usb(response, r'\b(usb-c|thunderbolt|usb 4|type-c)\b')
        except:
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
            elif "chrome" in os or "Chrome" in os:
                return "Chrome OS"
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
            return ", ".join([color.strip() for color in colors]) if len(colors) > 1 else "N/A"
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
            date = self.get_scoped_value(response, ["Thời điểm ra mắt:"]).split("/")
            if len(date) == 1:
                return f"**/**/{date[0]}" if len(date[0]) == 4 else "N/A"
            elif len(date) == 2:
                return f"**/{int(date[0]):02}/{date[1]}" if len(date[1]) == 4 else "N/A"
            elif len(date) == 3:
                return f"{int(date[0]):02}/{int(date[1]):02}/{date[2]}" if len(date[2]) == 4 else "N/A"
            else:
                return "N/A"
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