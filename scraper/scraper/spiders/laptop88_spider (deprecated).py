import re
from requests import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider

class Laptop88Spider(BaseLaptopshopPageSpider):
    name = "laptop88_spider"
    allowed_domains = ["laptop88.vn"]
    start_urls = ["https://laptop88.vn/laptop-moi.html"]
    
    product_site_css = 'h2.product-title a::attr(href)'
    page_css = '.paging a::attr(href)' 
    selenium_product_request = True
    # show_technical_spec_button_xpath = "//div[@class='thongsokythuat']/a[@class='button-box']"
    
    source = 'laptop88'
    

    def get_scoped_values(self, response, list_names, category_names=[]):
        possible_values = [
            "//div[@class='thongsokythuat']//tr[td[normalize-space(.) = '{}']]/following-sibling::tr[1][td[normalize-space(.) = '{}']]/td[2]//text()".format(name[0], name[1])
            for name in category_names
        ] + [
            "//div[@class='thongsokythuat']//tr[td[normalize-space(.) = '{}']]/following-sibling::tr[td[normalize-space(.) = '{}']]/td[2]//text()".format(name[0], name[1])
            for name in category_names
        ] + [
            "//div[@class='thongsokythuat']//tr[td//strong[normalize-space(text()) = '{}']]//text()".format(name)
            for name in list_names
        ] + [
            "//h4[normalize-space(text()) = '{}']/following-sibling::table[1]//td[contains(normalize-space(text()), '{}')]/following-sibling::td/p/text()".format(name[0], name[1])
            for name in category_names
        ] + [
            "//div[@class='thongsokythuat']//tr[th[normalize-space(text()) = '{}']]/td//text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='thongsokythuat']//tr[td[1][normalize-space(text()) = '{}']]/td[2]//text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='thongsokythuat']//tr[td[contains(normalize-space(text()), '{}')]]/td[2]//text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='thongsokythuat']//tr[th[contains(normalize-space(text()), '{}')]]/td//text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='thongsokythuat']//td[normalize-space(text()) = '{}']/following-sibling::th/strong/text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='thongsokythuat']//li[contains(normalize-space(), '{}')]/text()".format(name)
            for name in list_names
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
        valid = True
        # number_of_stores = response.xpath("//div[@class='product_store']//span[@id='total-store']/text()").get()
        # if number_of_stores and int(number_of_stores) == 0:
        #     valid = False
        
        product_name = response.xpath("//h2[@class='name-product']/text()").get().lower()
        for _ in ["ipad", "tablet", "cũ", "new outlet"]:
            if _ in product_name:
                valid = False
        
        price = response.xpath("//div[@class='price js-price-config js-price-buildpc']/text()").get().lower()
        if "liên hệ" in price or "call" in price:
            valid = False
            
        if not valid:
            print("Skipped: ", product_name)
        
        return valid
    
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
            res = response.xpath("//h2[@class='name-product']/text()").get().lower()
            for removal in ['laptop gaming ', 'laptop ', 'gray', 'black', 'silver', 'iceblue', '2 in 1']:
                res = res.replace(removal, '')

            res = re.sub(r'\([^()]*\)', '', res)
            if ']' in res:
                res = res.split(']')[1]
            
            res = res.split('- ')[0].split('|')[0].split('/')[0]
            
            if "macbook" in res:
                res = "apple " + ' '.join(res.split()[:2] + res.split()[-1:])
            
            if not res[-1].isalnum():
                res = res[:-1]
            
            return res.strip()
        except:
            return "n/a"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        cpu = self.get_scoped_values(response, ['CPU', 'Processor', 'Tên bộ vi xử lý', 'CPU:', 
                                                'Bộ vi xử lý', ])
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
        ram_amount = self.get_scoped_values(response, ['Bộ nhớ trong', 'RAM', 'Ram', 'Ram:', 'Bộ nhớ trong - Ram', 
                                                       'Bộ nhớ trong (RAM)', 'Dung lượng RAM', 'Memory', 'Dung lượng',
                                                       'Bộ nhớ'], 
                                                    [['Bộ nhớ trong', 'Dung lượng'], ['Bộ nhớ trong', 'RAM'],
                                                     ['Bộ nhớ trong (RAM)', 'RAM'], ['Bộ vi xử lý', 'RAM'], ['BỘ NHỚ RAM', 'Dung lượng RAM'],
                                                     ['BỘ NHỚ MÁY (RAM)', 'Dung lượng'], ['Bộ nhớ trong (RAM)', 'Dung lượng']])
        return ram_amount if ram_amount else 'n/a'
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        ram = self.get_scoped_values(response, ['Bộ nhớ trong', 'RAM', 'Ram', 'Ram:', 'Bộ nhớ trong - Ram', 'Memory', 'Dung lượng', 'Bộ nhớ'],
                                     [['BỘ NHỚ MÁY (RAM)', 'Công nghệ'] ])
        return ram if ram else 'n/a'
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        storage = self.get_scoped_values(response, ['Ổ cứng', 'Ổ Cứng', 'Ổ cứng:', 'SSD', 'Storage',
                                                    'Dung lượng ổ cứng', 'Ổ đĩa cứng - HDD', 'Dung lượng']) \
                + self.get_scoped_values(response, [ 'Dung lượng', 'Ổ cứng', 'Ổ Cứng', 'Ổ cứng:', 'SSD', 'Storage',
                                                    'Dung lượng ổ cứng', 'Ổ đĩa cứng - HDD',])
        return storage if storage else 'n/a'
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        storage = self.get_scoped_values(response, ['Ổ cứng', 'Ổ Cứng', 'Ổ cứng:', 'SSD', 'Storage',
                                                    'Dung lượng ổ cứng', 'Ổ đĩa cứng - HDD', 'Dung lượng'])
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
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình', 'Kích cỡ màn hình',
                                                   'Kích thước màn hình', 'MÀN HÌNH HIỂN THỊ', 'Màn hình - Monitor', 
                                                   'Hiển thị', 'Screen size', 'Size màn hình', 'Màn Hình', 'Màn hình:'])
        return screen if screen else 'n/a'
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình', 'Hiển thị', 
                                                   'Kích cỡ màn hình', 'Kích thước màn hình', 'MÀN HÌNH HIỂN THỊ',
                                                   'Màn hình - Monitor', 'Screen size', 'Size màn hình',
                                                   'Màn Hình', 'Màn hình:'])
        return screen if screen else 'n/a'

    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        screen = self.get_scoped_values(response, ['Display', 'Độ phân giải:', 'Màn hình', 'Hiển thị', 
                                                   'Kích cỡ màn hình', 'Kích thước màn hình', 'MÀN HÌNH HIỂN THỊ',
                                                   'Màn hình - Monitor', 'Screen size', 'Size màn hình',
                                                   'Màn Hình', 'Màn hình:'])
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
        battery = self.get_scoped_values(response, ['Pin', 'Battery', 'Kiểu Pin', 'Pin:'])
        return battery if battery else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        battery = self.get_scoped_values(response, ['Pin', 'Battery', 'Kiểu Pin', 'Pin:'])
        return battery if battery else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the size of the laptop in cm from the response.
        """
        size = self.get_scoped_values(response, ['Kích thước', 'Dimensions', 'Trọng lượng', 
                                                 'Kích thước & trọng lượng', 'Kích thước (Dài x Rộng x Cao)'])
        return size if size else "n/a"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        weight = self.get_scoped_values(response, ['Trọng lượng', 'Weight', 'Cân nặng', 'Trọng Lượng', 
                                                   'Kích thước & trọng lượng', 'Trọng lượng (kg)', 
                                                   'Trọng lượng:',])
        return weight if weight else "n/a"

    # Connectivity
    def parse_connectivity(self, response: Response):
        """
        Extracts the connectivity options of the laptop from the response.
        """
        res = self.get_scoped_values(response, ['Cổng kết nối', 'Kết nối', 'Cổng giao tiếp', 'Cổng Kết Nối	'
                                                'Standard Ports', 'Cổng Kết Nối', 'Cổng giao tiếp	',
                                                'CỔNG KẾT NỐI (I/O PORT)', 'Cổng kết nối:	'
                                                'Kết nối USB', 'Kết nối HDMI/VGA', 'Tai nghe'])
        return res if res else "n/a"
        
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        os = self.get_scoped_values(response, ['Hệ điều hành', 'Operating System', 'Hệ điều hành:'])
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