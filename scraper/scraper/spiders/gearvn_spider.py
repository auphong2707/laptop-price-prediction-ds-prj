from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
from scrapy.http import Response
import re

class GearvnSpider(BaseLaptopshopLoadmoreButtonSpider):
    name = "gearvn_spider"
    allowed_domains = ["gearvn.com"]
    start_urls = [
        'https://gearvn.com/collections/laptop',
    ]
    
    product_site_css = 'h3.proloop-name a::attr(href)'
    loadmore_button_css = 'button#load_more'
    close_button_xpaths = ["//button[@class='close']"]
    
    source = 'gearvn'
    
    
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//tr/td[contains(., '{}')]/following-sibling::td//span//text()".format(name)
                for name in names
            ] + [
                "//li/div[contains(., '{}')]/following-sibling::div/text()".format(name)
                for name in names
            ] + [
                "//tr/td[contains(., '{}')]/following-sibling::td/text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if len(scope) > 0:
                return '\n'.join(scope)
            
        return None
    
    def yield_condition(self, response):
        if response.xpath("//button[@id='buy-now']/span[@class='maintext']/text()").get() == 'HẾT HÀNG':
            print(f"Skipped: {response.url}")
            return False
        return True
    
    #  [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            res = response.css('.product-name h1::text').get().lower()
            
            if "macbook" in res or "macBook" in res:
                return "apple"
            
            for removal in ['laptop gaming ', 'laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0]
        except:
            return "n/a"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        res = response.css('.product-name h1::text').get().lower()
        return res if res else "n/a"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['CPU'])
        return res if res else "n/a"
    
        # try:
        #     res = self.get_scoped_value(response, ['CPU']).lower()
            
        #     if self.parse_brand(response) == "apple":
        #         res = re.sub(r'(\d+)cpu', r'\1 core', res)
        #         res = re.sub(r'\s?\d+gpu', '', res)
        #         res = "apple " + res
        #     else:
        #         for removal in ['®', '™', 'processors', ' processor', 'mobile', 'with intel ai boost', '(tm)', '(r)']:
        #             res = res.replace(removal, '')

        #         res = re.sub(r'\s*(\d{1,2}th gen|gen \d{1,2}th)\s*', ' ', res)
                
        #         special_sep = re.search(r'\b(\d+\.\d+\s?upto\s?\d+\.\d+ghz|\d+\.\d+\s?ghz|\d+\s?gb|dgb)\b', res)
        #         if special_sep:
        #             res = res.split(special_sep.group())[0]
                    
        #         for sep in ['(', 'up to', 'upto', ',']:
        #             res = res.split(sep)[0]
                    
        #         if res.startswith(('i', 'ultra')):
        #             res = 'intel core ' + res
                    
        #         if res.startswith('ryzen'):
        #             res = 'amd ' + res
            
        #     return ' '.join(res.split())
        # except:
        #     return "n/a"
        
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['VGA', 'Card đồ họa'])
        return res if res else "n/a"
        
        # try:
        #     res = self.get_scoped_value(response, ['VGA', 'Card đồ họa']).lower()
            
        #     res = re.sub(r'[^\x20-\x7E]|®|™|integrated|gpu', ' ', res, flags=re.IGNORECASE)              
        #     res = re.sub(r'\([^()]*\)', '', res)

        #     special_sep = re.search(r'\d+\s?gb|gddr\d+', res)
        #     if special_sep:
        #         res = res.split(special_sep.group())[0]
            
        #     for spliter in [' with ', ' laptop ', '+', ',',  'up', 'upto', 'up to', 'rog']:
        #         res = res.split(spliter)[0]
                
        #     res = ' '.join(res.split())
    
        #     if self.parse_brand(response) == "apple":
        #         res = "n/a"
        #     else:
        #         if any([keyword in res.lower() for keyword in ['nvidia', 'geforce', 'rtx', 'gtx']]):
        #             for removal in ['amd radeon graphics', 'intel uhd graphics', 'laptop', 'nvidia', 'intel iris xe', 'graphics']:
        #                 res = res.replace(removal, '')
        #                 res = ' '.join(res.split())
                    
        #             if (res.startswith('rtx') and 'ada' not in res) or res.startswith('gtx'):
        #                 res = 'geforce ' + res
                        
        #             res = re.sub(r'(\s\d{3,4})ti', r'\1 ti', res)
        #             res = re.sub(r'(ti)(\d{4})', r'\1 \2', res)
                    
        #             if res.startswith('mx'):
        #                 res = 'geforce ' + res
        #             if 'geforce' in res:
        #                 res = res[res.index('geforce'):]
        #         elif any([keyword in res for keyword in ['iris xe', 'intel uhd', 'intel hd', 'intel graphics', 
        #                                                  'intel arc', 'onboard', 'on board', 'qualcomm']]):
        #             res = "n/a"
        #         elif any([keyword in res for keyword in ['amd', 'radeon']]):
        #             res = res.replace('amd', '')
        #             if 'vega' in res:
        #                 res = "n/a"
        #             elif not 'rx' in res:
        #                 res = "n/a"
                        
        #     return res.strip()
        # except:
        #     return "n/a"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ['RAM', 'Ram', 'ĐẬP'])
        return res if res else "n/a"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res = self.get_scoped_value(response, ['RAM', 'Ram', 'ĐẬP'])
        return res if res else "n/a"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD', 'Ổ Cứng'])
        return res if res else "n/a"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD', 'Ổ Cứng'])
        return res if res else "n/a"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Webcam', 'Camera'])
        return res if res else "n/a"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'])
        return res if res else "n/a"
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: 1920x1080, 2560x1600, etc.
        """
        res = self.get_scoped_value(response, ['Màn hình'])
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
        Extracts the battery capacity in Whr from the response.
        """
        res = self.get_scoped_value(response, ['Pin', 'Ghim'])
        return res if res else "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ['Pin', 'Ghim'])
        return res if res else "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        res = self.get_scoped_value(response, ['Kích thước', 'Kích thước', 'Kích cỡ'])
        return res if res else "n/a"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ['Trọng lượng', 'Trọng lượng', 'Cân nặng'])
        return res if res else "n/a"
    
    # Connectivity
    def parse_connectivity(self, response: Response):
        """
        Extracts the connectivity features of the laptop from the response.
        Example: Wi-Fi, Bluetooth, etc.
        """
        res = self.get_scoped_value(response, ['Cổng kết nối', 'Cổng giao tiếp', 'Port next', 'Cổng tiếp theo', 'Cổng tiếp theo'])
        return res if res else "n/a"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ['Hệ điều hành', 'Hệ thống điều chỉnh'])
        return res if res else "n/a"
        # try:
        #     res = self.get_scoped_value(response, ['Hệ điều hành', 'Hệ thống điều chỉnh']).lower()
        #     res = re.sub(r'bản quyền|[^\x20-\x7E]|single language|sl|64|sea', ' ', res)
        #     res = ' '.join(res.split())
            
        #     for sep in ['+', ',', '-', ';']:
        #         res = res.split(sep)[0]
                
        #     if 'windows' in res:
        #         res = res[res.index('windows'):]
            
        #     return res.strip()
        # except:
        #     return "n/a"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        res = self.get_scoped_value(response, ['Bảo hành'])
        if res is None:
            res = response.xpath("//strong[contains(text(), 'Bảo hành')]/following-sibling::text()").get()
        if res is None:
            res = response.xpath('//span[contains(text(), "Bảo hành")]/text()').get()
            
        return res if res else "n/a"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        res = response.xpath('//span[@class="pro-price a"]/text()').get()
        return res if res else "n/a"
    
    # [PARSE FEATURES SECTION: END]