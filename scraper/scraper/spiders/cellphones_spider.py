import re
from requests import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider


class CellphoneSpider(BaseLaptopshopLoadmoreButtonSpider):
    name = "cellphones_spider"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = [
        'https://cellphones.com.vn/laptop.html',
    ]
    
    product_site_css = 'div.product-info a::attr(href)'
    loadmore_button_css = '.btn-show-more'
    close_button_xpaths = ["//button[@class='cancel-button-top']"]
    show_technical_spec_button_xpath = "//button[contains(@class, 'button__show-modal-technical')]"
    selenium_product_request = True
    
    source = 'cellphones'
    
    def get_scoped_value(self, response: Response, names):
        possibile_values = [
                "//li[contains(@class, 'technical-content-modal-item')]//p[text()='{}']/following-sibling::div[1]//text()".format(name)
                for name in names
            ] + [
                "//li[contains(@class, 'technical-content-modal-item')]//p[a[text()='{}']]/following-sibling::div[1]//text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return '\n'.join(scope)
            
        return None
    
    def yield_condition(self, response):
        name = response.css('.box-product-name h1::text').get().lower()
        price = response.css('.product__price--show::text').get()
        if 'cũ' in name \
            or ('mac' in name and 'macbook' not in name) \
            or 'đã kích hoạt' in name \
            or (price is not None and 'Giá Liên Hệ' in price):
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
        try:
            res = response.css('.box-product-name h1::text').get().lower()
            
            if "mac" in res:
                return "apple"
            
            for removal in ['laptop gaming ', 'laptop Gaming ', 'laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0].lower()
        except:
            return "n/a"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        res = response.css('.box-product-name h1::text').get().lower()
        return res if res else "n/a"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['Loại CPU'])
        return res if res else "n/a"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['Loại card đồ họa'])
        return res if res else "n/a"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ['Dung lượng RAM'])
        return res if res else "n/a"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res = self.get_scoped_value(response, ['Loại RAM'])
        return res if res else "n/a"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ['Ổ cứng'])
        return res if res else "n/a"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ['Ổ cứng']) + ' '\
                + self.get_scoped_value(response, ['Tính năng đặc biệt'])
        return res if res else "n/a"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Webcam'])
        return res if res else "n/a"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ['Kích thước màn hình'])
        return res if res else "n/a"
        
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Độ phân giải màn hình']) + ' '\
                + self.get_scoped_value(response, ['Công nghệ màn hình'])
        return res if res else "n/a"

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        res = self.get_scoped_value(response, ['Tần số quét'])
        return res if res else "n/a"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        res = self.get_scoped_value(response, ['Công nghệ màn hình'])
        return res if res else "n/a"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        res = self.get_scoped_value(response, ['Pin'])
        return res if res else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ['Pin'])
        return res if res else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop in cm from the response.
        """
        res = self.get_scoped_value(response, ['Kích thước'])
        return res if res else "n/a"
        
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ['Trọng lượng'])
        return res if res else "n/a"
    
    # Connectivity
    def parse_connectivity(self, response):
        """
        Extracts the connectivity features from the response.
        """
        res = self.get_scoped_value(response, ['Cổng giao tiếp'])
        return res if res else "n/a"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ['Hệ điều hành'])
        return res if res else "n/a"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        res = response.xpath("//a[@href='https://cellphones.com.vn/chinh-sach-bao-hanh']/\
                                 parent::div[contains(@class, 'description')]/text()[1]").get()
        return res if res else "n/a"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        for css in ['div.tpt-box.active p.tpt---sale-price::text', '.product__price--show::text']:
            price = response.css(css).get()
            if price:
                return price

        return "n/a"
    
    # [PARSE FEATURES SECTION: END]