from .base_laptopshop_spider import BaseLaptopshopPageSpider
from scrapy.http import Response
import re

class LaptopworldSpider(BaseLaptopshopPageSpider):
    name = "laptopworld_spider"
    allowed_domains = ["laptopworld.vn"]
    start_urls = [
        'https://laptopworld.vn/san-pham-apple/laptop-apple.html',
        'https://laptopworld.vn/laptop-games-do-hoa.html'
    ]
    
    product_site_css = 'a.p-img::attr(href)'
    page_css = 'div.paging a::attr(href)'
    
    source = 'laptopworld'

    selenium_product_request = True

    def get_scoped_value(self, response: Response, names):
        possibile_values = [
                "//td[.//span[contains(text(),'{}')]]/following-sibling::td//span/text()".format(name)
                for name in names
            ] + [
                "//div[@class='content-text nd']//tr[td//strong[contains(text(), '{}')]]/td[2]//text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return '\n'.join(scope)
            
        return None
    
    def yield_condition(self, response):
        name = response.xpath('//h1/text()').get().lower()
        price = response.xpath('//b[@class="js-this-product"]/text()').get().lower()
        if any(_ in name for _ in ['balo', 'tai nghe', 'dock', 'máy chơi game']) \
            or price == 'liên hệ':
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
        product_name = response.xpath('//h1/text()').get().lower()
        brands = r'\b(dell|asus|lenovo|hp|msi|acer|huawei|gigabyte|samsung galaxy|lg|microsoft|macbook)\b'
        
        # Search for the brand in the product name
        match = re.search(brands, product_name)

        if match:
            # If the matched brand is "macbook", return "apple"
            if match.group(0) == 'macbook':
                return 'apple'
            else:
                # Return the matched brand
                return match.group(0)
        else:
            return "n/a"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        res = response.xpath('//h1/text()').get()
        return res if res else 'n/a'
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['CPU','Bộ Vi Xử Lý:','Bộ xử lý'])
        return res if res else "n/a"
    
    # VGA   
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['Video','Card đồ hoạ'])
        return res if res else "n/a"    
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ['Bộ Nhớ Trong:', 'Ram', 'Bộ Nhớ:', 'Ổ đĩa cứng', 'Ổ cứng'])
        return res if res else "n/a"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res = self.get_scoped_value(response, ['Bộ Nhớ Trong:', 'Ram', 'Bộ Nhớ:','Ổ đĩa cứng'])
        return res if res else "n/a"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ['Ổ đĩa cứng', 'Ổ Lưu Trữ:', 'Bộ Lưu Trữ:'])
        return res if res else "n/a"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ['Ổ đĩa cứng', 'Ổ Lưu Trữ:', 'Bộ Lưu Trữ:'])
        return res if res else "n/a"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Webcam', 'Camera:', 'Camera'])
        return res if res else "n/a"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ['Màn Hình Hiển Thị:', 'Màn hình'])
        return res if res else "n/a"
        
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Màn Hình Hiển Thị:', 'Màn hình'])
        return res if res else "n/a"

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        res = self.get_scoped_value(response, ['Hỗ trợ hiển thị', 'Màn hình'])
        return res if res else "n/a"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        res = self.get_scoped_value(response, ['Màn Hình Hiển Thị:', 'Màn hình'])
        return res if res else "n/a"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        res = self.get_scoped_value(response, ['Pin & Nguồn:', 'Pin', 'Pin & Nguồn'])
        return res if res else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ['Pin & Nguồn:', 'Pin', 'Pin & Nguồn'])
        return res if res else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop in cm from the response.
        """
        res = self.get_scoped_value(response, ['Size and Weight'])
        return res if res else "n/a"
        
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ['Trọng lượng', 'Size and Weight'])
        return res if res else "n/a"
    
    # Connectivity
    def parse_connectivity(self, response):
        """
        Extracts the connectivity features from the response.
        """
        res = self.get_scoped_value(response, ['Cổng giao tiếp', 'Cổng Kết Nối', 'Sạc và mở rộng:', 'Tích Hợp Cổng:'])
        return res if res else "n/a"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ['Hệ Điều Hành', 'Hệ điều hành'])
        return res if res else "n/a"
    
    # Warranty      
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        res = response.xpath("//p[@class='detail-bh']/span/text()").get()
        return res if res else "n/a"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        res = response.xpath('//b[@class="js-this-product"]/text()').get()
        return res.replace(' VNĐ', '').strip() if res else "n/a"
    
    # [PARSE FEATURES SECTION: END]