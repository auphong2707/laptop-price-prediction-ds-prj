import re
from requests import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider

class Laptop88Spider(BaseLaptopshopPageSpider):
    name = "laptop88"
    allowed_domains = ["laptop88.vn"]
    start_urls = [
        "https://laptop88.vn/laptop-moi.html",
    ]
    
    product_site_css = 'h2.product-title a::attr(href)'
    source = 'laptop88'
    

    def get_scoped_values(self, response, names):
        possible_values = [
            "//td[strong[text()='{}']]/following-sibling::td/text()".format(name)
            for name in names
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
        return True
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            product_name = response.xpath("//h2[@class='name-product']/text()").getall().lower()
            for brand in ["dell", "asus", "lenovo", "hp", "msi", "acer", "huawei", "gigabyte", "samsung galaxy", "lg", "microsoft"]:
                if brand in product_name:
                    return brand
            if "macbook" in brand:
                return "apple"
        except:
            return "n/a"
    
    def parse_name(self, response: Response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            product_name = response.xpath("//h2[@class='name-product']/text()").getall()
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        cpu = self.get_scoped_values(response, ['CPU', 'Processor', 'Tên bộ vi xử lý'])
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
        ram_amount = self.get_scoped_values(response, ['Memomy', 'Dung lượng', 'RAM', 'Ram:'])
        return ram_amount if ram_amount else 'n/a'
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
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
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop in cm from the response.
        """
        return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        return "N/A"
    
    # Connectivity
    def parse_connectivity(self, response: Response):
        """
        Extracts the connectivity options of the laptop from the response.
        """
        return "N/A"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        return "N/A"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        return "N/A"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        price = response.xpath("//div[@class='price js-price-config js-price-buildpc']/text()").get()
        return price if price else "n/a"