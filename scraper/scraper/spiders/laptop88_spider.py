import re
from requests import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider

class Laptop88Spider(BaseLaptopshopPageSpider):
    name = "laptop88"
    allowed_domains = ["laptop88.vn"]
    start_urls = [
        "https://laptop88.vn/laptop-moi.html",
        ] + [
        f"https://laptop88.vn/laptop-moi.html?page={i}" for i in range(2, 15)
        ]
    
    product_site_css = 'h2.product-title a::attr(href)'
    source = 'laptop88'
    

    def get_scoped_values(self, response, names):
        possible_values = [
            "//td[strong[text()='{}']]/following-sibling::td/text()".format(name)
            for name in names
        ] + [
            "//tr[td//strong[contains(text(), '{}')]]//text()".format(name)
            for name in names
        ] + [
            "//tr[td[contains(text(),'{}')]]/td[@class='alignleft']/div[@class='rightValue']/text()".format(name)
            for name in names
        ] + [
            "//tr[td[1][contains(text(), '{}')]]/td[2]//span[@class='configuration-content fl']".format(name)
            for name in names
        ] + [
            "//tr[th[contains(text(), '{}')]]/td//text()".format(name)
            for name in names
        ] + [
            "//tr[td[1][contains(., '{}')]]/td[2]//text()".format(name)
            for name in names
        ] + [
            
        ]
        
        for value in possible_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return '\n'.join(scope)
            
        return None
    
    def yield_condition(self, response: Response):
        """
        Returns True if the response is valid to be scraped.
        """
        product_name = response.xpath("//h2[@class='name-product']/text()").get().lower()
        for _ in ["ipad", "tablet", "cũ"]:
            if _ in product_name:
                return False
        
        price = response.xpath("//div[@class='price js-price-config js-price-buildpc']/text()").get().lower()
        if "liên hệ" in price or "call" in price:
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
            product_name = response.xpath("//h2[@class='name-product']/text()").get().lower()
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
        """
        Extracts the name of the laptop from the response.
        """
        try:
            product_name = response.xpath("//h2[@class='name-product']/text()").get().lower()
            return product_name if product_name else "n/a"
        except:
            return "n/a"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        cpu = self.get_scoped_values(response, ['CPU', 'Processor', 'Tên bộ vi xử lý', 'CPU:'])
        return cpu if cpu else 'n/a'
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        gpu = self.get_scoped_values(response, ['Graphics', 'Card VGA', 'Bộ xử lí', 'Card màn hình:'])
        return gpu if gpu else 'n/a'
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        ram_amount = self.get_scoped_values(response, ['Memory', 'Dung lượng', 'RAM', 'Ram:', 'Bộ nhớ trong - Ram', "Bộ nhớ", ])
        return ram_amount if ram_amount else 'n/a'
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        ram = self.get_scoped_values(response, ['Memory', 'Dung lượng', 'RAM', 'Ram:'])
        return ram if ram else 'n/a'
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        storage = self.get_scoped_values(response, ['Ổ cứng', 'Storage', 'Dung lượng ổ cứng', 'Ổ cứng:'])
        return storage if storage else 'n/a'
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        storage = self.get_scoped_values(response, ['Ổ cứng', 'Storage', 'Dung lượng ổ cứng', 'Ổ cứng:'])
        return storage if storage else 'n/a'
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        webcam = self.get_scoped_values(response, ['Webcam', 'Camera', 'Webcam:'])
        return webcam if webcam else 'n/a'
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình'])
        return screen if screen else 'n/a'
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình'])
        return screen if screen else 'n/a'

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình'])
        return screen if screen else 'n/a'
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình'])
        return screen if screen else 'n/a'
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        battery = self.get_scoped_values(response, ['Pin', 'Battery'])
        return battery if battery else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        battery = self.get_scoped_values(response, ['Pin', 'Battery'])
        return battery if battery else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop in cm from the response.
        """
        size = self.get_scoped_values(response, ['Kích thước', 'Dimensions'])
        return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        weight = self.get_scoped_values(response, ['Trọng lượng', 'Weight'])
        return weight if weight else "n/a"

    # Connectivity
    def parse_connectivity(self, response: Response):
        """
        Extracts the connectivity options of the laptop from the response.
        """
        res = self.get_scoped_values(response, ['Cổng kết nối'])
        return res if res else "n/a"
        
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        os = self.get_scoped_values(response, ['Hệ điều hành', 'Operating System'])
        return os if os else 'n/a'
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        warranty = response.xpath("//div[@class='product-warranty']//p[contains(text(), 'Bảo hành')]/text()").get()
        return warranty if warranty else "n/a"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        price = response.xpath("//div[@class='price js-price-config js-price-buildpc']/text()").get()
        return price if price else "n/a"