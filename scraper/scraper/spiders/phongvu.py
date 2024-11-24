from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
import re

class PhongvuSpider(BaseLaptopshopLoadmoreButtonSpider):
    selenium_product_request = True
    
    name = "phongvu_spider"
    allowed_domains = ["phongvu.vn"]
    start_urls = [
        'https://phongvu.vn/c/laptop',
    ]

    product_site_css = "a.css-pxdb0j::attr(href)"
    loadmore_button_css = '.css-b0m1yo'
    close_button_xpaths = ["//div[@class='css-73p2ms']/span"]
    show_technical_spec_button_xpath = "//div[contains(text(), 'Xem thêm nội dung')]"
    source = 'phongvu'

    def get_scoped_value(self, response, names):
        possibile_values = [
                "//div[@class='css-9s7q9u']//div[contains(text(), '{}')]/following-sibling::div//text()".format(name)
                for name in names
            ]
            
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return " ".join(scope)
        
        return None

    
    # [PARSE FEATURES SECTION: START]
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        res = response.css('h1.css-nlaxuc::text').get()
        return res if res else 'n/a'
    
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            return response.xpath("//div[text()='Thương hiệu']/following-sibling::div/text()").get()
        except Exception:
            return "n/a"

    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['CPU'])
        return res if res else "n/a"

    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['Chip đồ họa'])
        return res if res else "n/a"

        # RAM
    def parse_ram_amount(self, response: Response):
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ["Ram", "Dung lượng RAM"])
        return res if res else "n/a"
    
    def parse_ram_type(self, response: Response):
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res =  self.get_scoped_value(response, ["Ram"])
        return res if res else "n/a"
    
    # Storage
    def parse_storage_amount(self, response: Response):
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ["Dung lượng SSD", "Lưu trữ"])
        return res if res else "n/a"
    
    def parse_storage_type(self, response: Response):
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ["Dung lượng SSD", "Lưu trữ"])
        return res if res else "n/a"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ["Webcam", "Màn hình"])
        return res if res else "n/a"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ["Màn hình"])
        return res if res else "n/a"
        
    def parse_screen_resolution(self, response: Response):
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ["Màn hình"])
        return res if res else "n/a"
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'])
        return res if res else "n/a"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'])
        return res if res else "n/a"
    
    # Battery
    def parse_battery_capacity(self, response: Response):
        """
        Extracts the battery capacity from the response.
        """
        res = self.get_scoped_value(response, ["Công suất pin", "Pin"])
        return res if res else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ["Pin"])
        return res if res else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop from the response.
        """
        res = self.get_scoped_value(response, ["Kích thước, khối lượng", "Kích thước"])
        return res if res else "n/a"
    
    # Weight
    def parse_weight(self, response: Response):
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ["Kích thước, khối lượng", "Khối lượng"])
        return res if res else "n/a"

    # Connectivity
    def parse_connectivity(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        res = self.get_scoped_value(response, ["Cổng kết nối"])
        return res if res else "n/a"
    
    # Operating System
    def parse_default_os(self, response: Response):
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ["Hệ điều hành"])
        return res if res else "n/a"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        res = self.get_scoped_value(response, ["Bảo hành"])
        return res if res else "n/a"
    
    # Price
    def parse_price(self, response: Response):
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        res = response.xpath("//div[contains(@class, 'att-product-detail-latest-price')]/text()").get()
        return res if res else "n/a"
    
    # [PARSE FEATURES SECTION: END]