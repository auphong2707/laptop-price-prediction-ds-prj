from .base_laptopshop_spider import BaseLaptopshopPageSpider
from scrapy.http import Response
import re

class LaptopazSpider(BaseLaptopshopPageSpider):
    name = 'laptopaz_spider'
    allowed_domains = ["laptopaz.vn"]
    start_urls = ['https://laptopaz.vn/laptop-moi.html']

    product_site_css = ".p-img a::attr(href)"
    page_css = ".page-link::attr(href)"
    #page_css = None
    source = "laptopaz"

    def yield_condition(self, response: Response):
        paths = ["//span[@class='box-text-update2021']/span[@class='show-shadow']/text()"]

        for path in paths:
            res = response.xpath(path).get()
            if res:
                return True
        return False

    def get_scoped_value(self, response, names, trash = []):
        possible_values = [
                "//td[span/strong[text() = '{}']]/following-sibling::td/span/text()".format(name)
                for name in names
            ] + [
                "//td[span/strong[text() = '{}']]/following-sibling::td//p//span/text()".format(name)
                for name in names
            ] + [
                "//td[span/strong[text() = '{}']]/following-sibling::td//span/text()".format(name)
                for name in names
            ] + [
                "//table//tr[td/strong[contains(text(), '{}')]]/td[2]//text()".format(name)
                for name in names
            ] 
        for value in possible_values:
            scope = response.xpath(value).getall()
            if len(scope) != 0:
                scope = list(set(scope))
                return ' '.join(re.sub(r'[^\x20-\x7E\u00C0-\u024F\u1E00-\u1EFF]', ' ', ' '.join(scope)).split()).encode('utf-8').decode('latin1').encode('latin1').decode('utf-8').lower()
            
        return None

    def parse_brand(self, response: Response):
        try:
            product_name = response.xpath("//h1[contains(@class, 'bk-product-name')]/text()").get().lower()
            for brand in ["dell", "asus", "lenovo", "hp", "msi", "acer", "huawei", "gigabyte", "samsung galaxy", "lg", "microsoft"]:
                if brand in product_name:
                    return brand
            if "macbook" in product_name:
                return "apple"
            for name in ["thinkpad", "ideapad"]:
                if name in product_name:
                    return "lenovo"
        except:
            return "n/a"
    
    def parse_name(self, response: Response):
        res = response.xpath("//h1[contains(@class, 'bk-product-name')]/text()").get()
        return res if res else 'n/a'
    
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['CPU', 'Bộ vi xử lý', 'Tên bộ vi xử lý'], 
                                        [("Bộ vi xử lý (CPU)", "Tên bộ vi xử lý")])
        return res if res else 'n/a'
        
        
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['VGA', 'Card đồ họa', 'Bộ xử lý', 'Card VGA'],
                                        [("Đồ Họa (VGA)", "Bộ xử lý")])
        return res if res else 'n/a'
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ['RAM', "Bộ nhớ trong", "Ram"], 
                                        [("Bộ nhớ trong (RAM Laptop)", "Dung lượng")])
        return res if res else 'n/a'
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res = self.get_scoped_value(response, ['RAM', "Bộ nhớ trong", "Ram", "Dung lượng"],
                                        [("Bộ nhớ trong (RAM Laptop)", "Dung lượng")])
        return res if res else 'n/a'
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD'])
        return res if res else 'n/a'
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD'])
        return res if res else 'n/a'
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Webcam', 'Camera'], [("tiếp mở", "Camera")])
        return ''.join(res.lower().split()) if res else 'n/a'
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
        return res if res else 'n/a'
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: 1920x1080, 2560x1600, etc.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Độ phân giải")])
        return res if res else 'n/a'
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
        return res if res else 'n/a'
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
        return res if res else 'n/a'
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
        return res if res else 'n/a'
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
        return res if res else 'n/a'
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        res = self.get_scoped_value(response, ['Kích thước (rộng x dài x cao)', 'Thiết kế (rộng x dài x cao)'], [("Thông tin khác", "Thiết kế")])
        return res if res else 'n/a'
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ['Trọng lượng', 'Cân nặng', "Khối lượng"],
                                        [("Thông tin khác", "Trọng Lượng")])
        return res if res else 'n/a'
    
    # Connectivity
    def parse_connectivity(self, response: Response):
        res = self.get_scoped_value(response, ['Cổng kết nối', 'Cổng giao tiếp', 'Cổng kết nôi', 'Kết nối'],
                                        [("Giao tiếp mở rộng", "Kết nối USB"), ("Giao tiếp mở rộng", "Kết nối HDMI/ VGA"), ("Giao tiếp mở rộng", "Jack tai nghe"), ("Kết nối", "Cổng giao tiếp")])
        return res if res else 'n/a'
       
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ['Hệ điều hành', "OS"],
                                        [("Hệ điều hành (Operating System)", "Hệ điều hành đi kèm")])
        return res if res else 'n/a'
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        res = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"], [("Thông tin khác", "Màu sắc")])
        return res if res else 'n/a'
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        res = response.xpath("//div[contains(@class, 'pd-warranty-group')]//p[contains(text(), 'Bảo hành')]/text()").get()
        if res is None:
            res = response.xpath("//strong[contains(text(), 'Bảo hành')]/following-sibling::text()").get()
        if res is None:
            res = response.xpath('//span[contains(text(), "Bảo hành")]/text()').get()
        return res if res else 'n/a'
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        paths = ["//span[@class='box-text-update2021']/span[@class='show-shadow']/text()"]

        for path in paths:
            res = response.xpath(path).get().lower()
            if res:
                res = res.replace("deal:", "").strip()
                return res
        return 'n/a'
        
    
    