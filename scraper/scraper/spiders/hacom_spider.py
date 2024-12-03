from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
import html
import re

class HacomSpider(BaseLaptopshopLoadmoreButtonSpider):

    name = "hacom_spider"
    allowed_domains = ["hacom.vn"]
    start_urls = [
        "https://hacom.vn/laptop"
    ]
    product_site_css = ".p-name a::attr(href)"
    loadmore_button_css = ".btn-view-more"
    source = 'hacom'

    def get_scoped_value(self, response: Response, list_names, category_names=[]):
        possible_values = [
            "//tr[td/p/strong[contains(text(),'{}')]]/following-sibling::tr[1][td/p[contains(text(),'{}')]]/td[2]//text()".format(name[0], name[1])
            for name in category_names
        ] + [
            "//tr[td/p/strong[contains(text(),'{}')]]/following-sibling::tr[td/p[contains(text(),'{}')]][1]/td[2]/p/text()".format(name[0], name[1])
            for name in category_names
        ] + [
            "//h4[text()='{}']/following-sibling::table[1]//tr[td[p[text()='{}']]]/td[2]/p/text()".format(name[0], name[1])
            for name in category_names   
        ] + [
            "//td[p/strong[text()='{}']]/following-sibling::td/p/text()".format(name) 
            for name in list_names
        ] + [
            "//td[p[text()='{}']]/following-sibling::td/p/text()".format(name)
            for name in list_names
        ] + [
            "//div[@class='item' and contains(text(), '{}')]/text()".format(name)
            for name in list_names
        ] + [
            "//td[p/strong[contains(text(),'{}')]]/following-sibling::td/p/text()".format(name) 
            for name in list_names
        ] + [
            "//td[p[contains(text(),'{}')]]/following-sibling::td/p/text()".format(name)
            for name in list_names
        ]
        scope = []
        for value in possible_values:
            scope += response.xpath(value).getall()
        if len(scope) > 0:    
            return ' '.join(re.sub(r'[^\x20-\x7E\u00C0-\u024F\u1E00-\u1EFF]', ' ', ' '.join(scope)).split()).encode('utf-8').decode('latin1').encode('latin1').decode('utf-8').lower()
            
        return None

    def parse_brand(self, response: Response):
        try:
            brand = response.css('div.pd-info-right h1.sptitle2024::text').get().lower().split()
            for _ in ['lenovo', 'dell', 'lg']:
                if _ in brand:
                    return _
            if 'surface' in brand:
                return 'microsoft'
            if 'macbook' in brand:
                return 'apple'
            if brand[0] == "laptop":
                return brand[1]
            else:
                return brand[0]
        except:
            return "n/a"
    
    def parse_name(self, response: Response):
        name = response.css('div.pd-info-right h1.sptitle2024::text').get()
        return name if name else 'n/a'
    
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['CPU', 'Bộ vi xử lý', 'Tên bộ vi xử lý', 'Bộ vi xử lý'], 
                                        [("Bộ vi xử lý (CPU)", "Tên bộ vi xử lý")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['CPU', 'Bộ vi xử lý', 'Tên bộ vi xử lý'], 
                                        [("Bộ vi xử lý (CPU)", "Tên bộ vi xử lý")])
            
            if self.parse_brand(response) == "Apple":
                res = re.sub(r'(\d+)CPU', r'\1 cores', res)
                res = re.sub(r'\s?\d+GPU', '', res)
                res = "Apple " + res
            else:
                res = res.split(' (')[0]
                
                for removal in ['®', '™', ' processor', ' Processor', 'Mobile', '\xa0']:
                    res = res.replace(removal, '')
                
                if 'GHz' in res:
                    res = re.sub(r'\d+(\.\d+)?(\s)?GHz', '', res)
            
            return res.strip()
        except:
            return "N/A"
        
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        res = self.get_scoped_value(response, ['VGA', 'Card đồ họa', 'Bộ xử lý'],
                                        [("Đồ Họa (VGA)", "Bộ xử lý")])
        if "<" in res or ">" in res:
            res.split(">")[1]
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['VGA', 'Card đồ họa', 'Bộ xử lý'],
                                        [("Đồ Họa (VGA)", "Bộ xử lý")])
            
            if res in ["Intel® ARC™ Graphics", "AMD Radeon™ Graphics", None]:
                res = "N/A"
            else:
                for spliter in [' with ', ' Laptop ']:
                    res = res.split(spliter)[0]

                for removal in ['®', '™']:
                    res = res.replace(removal, '')

                if res.startswith('GeForce RTX'):
                    res = 'NVIDIA ' + res
                    
                res = re.sub(r'\d+GB|GDDR\d+', '', res)
                
            if "VGA:" in res:
                res = re.sub(r'VGA:(\s)?', '', res)

            return res.strip()
        except:
            return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        res = self.get_scoped_value(response, ['RAM', "Số khe cắm", "Ram", "Bộ nhớ trong"], 
                                        [("Bộ nhớ trong", "Dung lượng"), ("Bộ nhớ RAM", "Dung lượng RAM"), 
                                         ("Bộ nhớ trong", "RAM")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['RAM', "Bộ nhớ trong", "Ram"], 
                                        [("Bộ nhớ trong (RAM Laptop)", "Dung lượng")])
            
            search_value = re.search(r'\d+(\s)?GB', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('GB')[0])
            
            return res
        except:
            return "N/A"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        res = self.get_scoped_value(response, ['RAM', "Bộ nhớ trong", "Ram", "Dung lượng"],
                                        [("Bộ nhớ trong", "Dung lượng"), ("Bộ nhớ RAM", "Loại RAM"), 
                                         ("Bộ nhớ trong", "Loại RAM")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['RAM', "Bộ nhớ trong", "Ram", "Dung lượng"],
                                        [("Bộ nhớ trong (RAM Laptop)", "Dung lượng")])
            
            search_value = re.search(r'DDR+\d', res)
            if search_value:
                res = search_value.group()
            else:
                res = "N/A"
            
            return res.strip()
        except:
            return "N/A"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', "SSD", "Ổ cứng:"],
                                        [('Ổ cứng', 'Dung lượng')])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', "SSD"],
                                        [('Ổ cứng', 'Dung lượng')])
            res = re.sub(r'\s', '', res)
            search_value = re.search(r'\d+GB|\d+TB', res)
            if search_value:
                res = search_value.group()
                if 'TB' in res:
                    res = int(res.split('TB')[0]) * 1024
                else:
                    res = int(res.split('GB')[0])
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD'],
                                        [("Ổ cứng", "Dung lượng")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Ổ cứng', 'Ổ lưu trữ', 'Bộ nhớ', 'SSD'],
                                        [("Ổ cứng", "Dung lượng")])
        
            if "SSD" in res and "HDD" in res:
                if res.index("SSD") < res.index("HDD"):
                    res = "SSD"
                else:
                    res = "HDD"
            elif "SSD" in res:
                res = "SSD"
            elif "HDD" in res:
                res = "HDD"
            else:
                res = "N/A"
            
            return res.strip()
        except:      
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        res = self.get_scoped_value(response, ['Webcam', 'Camera'], [("tiếp mở", "Camera")])
        return ''.join(res.lower().split()) if res else 'n/a'
        try:
            res = ''.join(self.get_scoped_value(response, ['Webcam', 'Camera'], [("tiếp mở", "Camera")])
                          .lower().split())

            if any(term in res for term in ['qhd', '2k', '1440p', '2560x1440']):
                return 'QHD'
            elif any(term in res for term in ['fhd', '1080p', '1920x1080']):
                return 'FHD'
            elif any(term in res for term in ['hd', '720p', '1280x720']):
                return 'HD'
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình', 'Kích thước màn hình:'], [("Hiển thị", "Màn hình")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
            res = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch)', res)
            
            if res:
                res = float(res.group(1))
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: 1920x1080, 2560x1600, etc.
        """
        res = self.get_scoped_value(response, ['Độ phân giải', 'Màn hình', 'Kích thước màn hình:'], 
                                    [("Hiển thị", "Độ phân giải"), ("MÀN HÌNH HIỂN THỊ (LCD)", "Độ phân giải")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Độ phân giải")])
            
            res = ''.join(res.split())
            
            search_value = re.search(r'\d+x\d+', res)
            if search_value:
                res = search_value.group()
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình"), ("MÀN HÌNH HIỂN THỊ (LCD)", "Tần số quét")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
            search_value = re.search(r'\d+(\s)?Hz', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('Hz')[0])
            else:
                res = "N/A"

            return res
        except:
            return "N/A"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màn hình'], [("Hiển thị", "Màn hình")])
            
            search_value = re.search(r'\d+\s*nits', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('nits')[0])
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
            res = res.lower()
            
            search_value = re.search(r'\d+\s*whr', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('whr')[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Pin'], [("Pin Laptop", "Dung lượng pin")])
            res = res.lower()
            search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells', res)
            
            if search_value:
                res = int(search_value.group()[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        res = self.get_scoped_value(response, ['Kích thước', 'Kích thước (rộng x dài x cao)', 'Thiết kế (rộng x dài x cao)'], [("Thông tin khác", "Thiết kế")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Kích thước (rộng x dài x cao)', 'Thiết kế (rộng x dài x cao)'], [("Thông tin khác", "Thiết kế")])
            
            values = [float(num) for num in re.findall(r'-?\d+\.\d+|-?\d+', res)]
            values = sorted(values[:3], reverse=True)
            
            res = values[2] if values[2] < 100 else values[0] / 10
                
            return round(res, 2)
        except:
            return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        res = self.get_scoped_value(response, ['Trọng lượng', 'Cân nặng', "Khối lượng"],
                                        [("Thông tin khác", "Trọng Lượng")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Trọng lượng', 'Cân nặng', "Khối lượng"],
                                        [("Thông tin khác", "Trọng Lượng")])
            res = re.search(r'(\d+(\.\d+)?)\s*(kg|Kg|KG)', res)
            
            if res:
                res = float(res.group(1))
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    # Connectivity
    def parse_connectivity(self, response: Response):
        res = self.get_scoped_value(response, ['Cổng kết nối', 'Cổng giao tiếp'],
                                        [("Giao tiếp mở rộng", "Kết nối USB"), ("Giao tiếp mở rộng", "Kết nối HDMI/ VGA"), ("Giao tiếp mở rộng", "Jack tai nghe"), ("Kết nối", "Cổng giao tiếp")])
        return res if res else 'n/a'
        # try:
        #     res = self.get_scoped_value(response, ['Cổng kết nối', 'Cổng giao tiếp'],
        #                                 [("Giao tiếp mở rộng", "Kết nối USB"), ("Giao tiếp mở rộng", "Kết nối HDMI/ VGA"), ("Giao tiếp mở rộng", "Jack tai nghe")])
        #     res = res.lower()
        #     if re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE) != '':
        #         res = re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE)
            
            
        #     while '(' in res and ')' in res:
        #         res = re.sub(r'\([^()]*\)', '', res)

        #     res = re.split(r'[\n,]', res)
        #     count = 0
        #     for line in res:
        #         if re.search(pattern, line):
        #             line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
        #             val = line.split()[0]
        #             if val[-1] == 'x': val = val[:-1]
            
        #             if val.isnumeric():
        #                 count += int(val)
        #             else:
        #                 count += 1
            
        #     return count
        # except:
        #     return "N/A"
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        res = self.get_scoped_value(response, ['Hệ điều hành', "OS"],
                                        [("Hệ điều hành (Operating System)", "Hệ điều hành đi kèm")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Hệ điều hành', "OS"],
                                        [("Hệ điều hành (Operating System)", "Hệ điều hành đi kèm")])
            
            res = res.split('+')[0]
            for removal in ['Single Language']:
                res = res.replace(removal, '')
            
            return res.strip()
        except:
            return "N/A"
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        res = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"], [("Thông tin khác", "Màu sắc")])
        return res if res else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"], [("Thông tin khác", "Màu sắc")])
            
            if res:
                return res.strip()
            else:
                return "N/A"
        except:
            return "N/A"
    
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
        '''try:
            res = response.xpath("//div[contains(@class, 'pd-warranty-group')]//p[contains(text(), 'Bảo hành')]/text()").get()
            if res is None:
                res = response.xpath("//strong[contains(text(), 'Bảo hành')]/following-sibling::text()").get()
            if res is None:
                res = response.xpath('//span[contains(text(), "Bảo hành")]/text()').get()
                
            search_value = re.search(r'(\d+)\s*tháng', res)
            if search_value:
                res = int(search_value.group(1))
            else:
                search_value = re.search(r'(\d+)\s*Tháng', res)
                if search_value:
                    res = int(search_value.group(1))
                else:
                    res = "N/A"
            return res
            
        except:
            return "N/A"'''
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        paths = ["//p[@class='pd-price']/@data-price", '//span[@class="pro-price a"]/text()']

        for path in paths:
            res = response.xpath(path).get().lower()
            if "deal:" in res:
                res = res.split('deal:')[1] 
            return res if res else 'n/a'
        
