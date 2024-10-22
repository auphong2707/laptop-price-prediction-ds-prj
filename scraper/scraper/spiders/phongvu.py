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
            return self.get_scoped_value(response, ['Thương hiệu'])
        except Exception:
            return "N/A"

    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            return self.get_scoped_value(response, ['CPU'])
        except Exception:
            return "N/A"

    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            return self.get_scoped_value(response, ['Chip đồ họa'])
        except Exception:
            return "N/A"

        # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            return self.get_scoped_value(response, ["RAM", "Dung lượng RAM"])
        except Exception:
            return "N/A"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        try:
            return self.get_scoped_value(response, ["RAM"])
            # if ram_type.split().includes("Onboard"):
            #     index = ram_type.split().index("Onboard")
            #     return ram_type.split()[index + 1]
            # elif ram_type.split().includes("Onbard"):
            #     index = ram_type.split().index("Onbard")
            #     return  ram_type.split()[index + 1]
            # else:
            #     index = -1
            #     for i, word in enumerate(ram_type.split()):
            #         if "GB" in word:
            #             index = i
            #         break
            #     return ram_type.split()[index + 1]
        except Exception:
            return "N/A"
    
    # Storage
    def parse_storage_amount(self, response: Response):
        """
        Extracts the amount of storage in GB from the response.
        """
        try:
            storage = self.get_scoped_value(response, ["Dung lượng SSD", "Lưu trữ"]).split(" ")
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
            return self.get_scoped_value(response, ["Dung lượng SSD", "Lưu trữ"])
        except Exception:
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            if self.get_scoped_value(response, ["Thương hiệu"]) == "APPLE":
                return self.get_scoped_value(response, ["Màn hình"]).split()[-2]
            else:
                return self.get_scoped_value(response, ["Webcam"]).strip("Webcam")
        except Exception:
            return "N/A"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        try:
            return self.get_scoped_value(response, ["Màn hình"]).split()[0]
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
        Extracts the battery capacity from the response.
        """
        try:
            return self.get_scoped_value(response, ["Công suất pin"])
        except Exception:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        try:
            return self.get_scoped_value(response, ["Pin"])
        except Exception:
            return "N/A"
    
    # Size
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước", "Kích thước, khối lượng"]).split(" | ")[-1].strip()
            size = size.split("x")
            return size[1]
        except Exception:
            return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước", "Kích thước, khối lượng"]).split(" | ")[-1].strip()
            size = size.split("x")
            return size[2]
        except Exception:
            return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop from the response.
        """
        try:
            size = self.get_scoped_value(response, ["Kích thước", "Kích thước, khối lượng"]).split(" | ")[-1].strip()
            size = size.split("x")
            return size[0]
        except Exception:
            return "N/A"
    
    # Weight
    def parse_weight(self, response: Response):
        """
        Extracts the weight of the laptop in kg from the response.
        """
        try:
            return float(self.get_scoped_value(response, ["Kích thước, khối lượng tịnh:", "Khối lượng:"]).split(" ")[0])
        except Exception:
            return "N/A"
    
    # Connectivity
    def parse_number_orts(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        try:
            return self.get_scoped_value(response, ["Cổng kết nối"])
        except Exception:
            return "N/A"
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        try:
            search = re.search(r'Jack tai nghe', self.get_scoped_value(response, ["Cổng giao tiếp:"]))
            return 1 if search else 0
        except Exception:
            return "N/A"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        try:
            return self.get_scoped_value(response, ["Hệ điều hành"])
        except Exception:
            return "N/A"
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        try:
            return self.get_scoped_value(response, ["Màu sắc"])
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
            return self.get_scoped_value(response, ["Bảo hành"])
        except Exception:
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
        except Exception:
            return "N/A"
    
    # [PARSE FEATURES SECTION: END]