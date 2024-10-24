from scrapy.http import Response
import re

from .base_laptopshop_spider import BaseLaptopshopPageSpider

class AnphatSpider(BaseLaptopshopPageSpider):
    name = "anphat"
    allowed_domains = ["anphatpc.com.vn"]
    start_urls = [
        "https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html",
    ]
    product_site_css = ".p-img::attr(href)"   
    #page_css = "div.paging a[href]:not(:has(i))::attr(href)"
    page_css = None
    source = 'anphat'

    def get_scoped_value(self, response: Response, list_names, category_names = []):
        possible_values = [
            "//p[normalize-space()='{}']/ancestor::tr/following-sibling::tr[1]//td[2]//p".format(name)
            for name in category_names
        ] + [
            "//td[.//strong/span[contains(text(), '{}')]]/following-sibling::td//a/text()".format(name)
            for name in list_names
        ] + [
            "//td[.//span[contains(text(), '{}')]]/following-sibling::td//a/text()".format(name)
            for name in list_names
        ] + [
            "//tr[td//span[contains(text(), '{}')]]/td[2]//a//span/text()".format(name)
            for name in list_names
        ] + [
            "//tr[td//strong//span[contains(text(), '{}')]]/td[2]//a//span/text()".format(name)
            for name in list_names
        ] + [
            "//td[contains(., '{}')]/following-sibling::td//span/text()".format(name)
            for name in list_names
        ]
        
        for value in possible_values:
            scope = response.xpath(value).getall()
            if len(scope) != 0:
                scope = list(set(scope))
                return ' '.join(re.sub(r'[^\x20-\x7E\u00C0-\u024F\u1E00-\u1EFF]', ' ', ' '.join(scope)).split()).encode('utf-8').decode('latin1').encode('latin1').decode('utf-8').lower()
            
        return None

    def parse_brand(self, response: Response):
        brand = self.get_scoped_value(response, ["Hãng sản xuất"])
        return brand if brand else 'n/a'
        try:
            brand = self.get_scoped_value(response, ["Hãng sản xuất"]).split()
            if brand[0] == "laptop":
                return brand[1]
            else:
                return brand[0]
        except:
            return "n/a"
        
    
    def parse_name(self, response: Response):
        name = self.get_scoped_value(response, ["Tên sản phẩm"])
        return name if name else 'n/a'
        try:
            name = self.get_scoped_value(response, ["Tên sản phẩm"])
            if 'laptop' in name:
                return name.split('laptop ')[1]
            else:
                return name
        except:
            return "n/a"
        
    
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        cpu = self.get_scoped_value(response, ['Công nghệ CPU', 'Bộ vi xử lý'])
        return cpu if cpu else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Công nghệ CPU'])
            
            if self.parse_brand(response) == "apple":
                res = re.sub(r'(\d+)CPU', r'\1 cores', res)
                res = re.sub(r'\s?\d+GPU', '', res)
                res = "apple " + res
            else:
                res = res.split(' (')[0]
                
                for removal in ['®', '™', ' processor', 'mobile', '\xa0']:
                    res = res.replace(removal, '')
                
                if 'ghz' in res:
                    res = re.sub(r'\d+(\.\d+)?(\s)?GHz', '', res)
            
            return res.strip()
        except:
            return "n/a"
        
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        vga = self.get_scoped_value(response, ['Card màn hình'])
        return vga if vga else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Card màn hình'])
            
            if res in ["Intel® ARC™ Graphics", "AMD Radeon™ Graphics", None]:
                res = "n/a"
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
            return "n/a"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        ram = self.get_scoped_value(response, ['RAM'], ['Bộ nhớ trong (RAM)'])
        return ram if ram else 'n/a'
        try:
            res = self.get_scoped_value(response, ['RAM'])
            
            search_value = re.search(r'\d+(\s)?GB', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('GB')[0])
            
            return res
        except:
            return "n/a"
    
    def parse_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        ram = self.get_scoped_value(response, ['Loại RAM'])
        return ram if ram else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Loại RAM'])
            
            search_value = re.search(r'DDR+\d', res)
            if search_value:
                res = search_value.group()
            else:
                res = "n/a"
            
            return res.strip()
        except:
            return "n/a"
    
    # Storage
    def parse_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        storage = self.get_scoped_value(response, ['Dung lượng'], ["Ổ cứng"])
        return storage if storage else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Dung lượng'])
            res = re.sub(r'\s', '', res)
            search_value = re.search(r'\d+GB|\d+TB', res)
            if search_value:
                res = search_value.group()
                if 'TB' in res:
                    res = int(res.split('TB')[0]) * 1024
                else:
                    res = int(res.split('GB')[0])
            else:
                res = "n/a"
                
            return res
        except:
            return "n/a"
    
    def parse_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        storage = self.get_scoped_value(response, ['Dung lượng'])
        return storage if storage else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Dung lượng'])
        
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
                res = "n/a"
            
            return res.strip()
        except:      
            return "n/a"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        webcam = self.get_scoped_value(response, ['Webcam', 'Camera'])
        return webcam if webcam else 'n/a'
        try:
            res = ''.join(self.get_scoped_value(response, ['Webcam', 'Camera']))

            if any(term in res for term in ['qhd', '2k', '1440p', '2560x1440']):
                return 'QHD'
            elif any(term in res for term in ['fhd', '1080p', '1920x1080']):
                return 'FHD'
            elif any(term in res for term in ['hd', '720p', '1280x720']):
                return 'HD'
            else:
                return "n/a"
        except:
            return "n/a"
    
    # Screen
    def parse_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        scr = self.get_scoped_value(response, ['Kích thước màn hình', 'Màn hình'])
        return scr if scr else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Kích thước màn hình'])
            res = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch)', res)
            
            if res:
                res = float(res.group(1))
            else:
                res = "n/a"
                
            return res
        except:
            return "n/a"
    
    def parse_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: 1920x1080, 2560x1600, etc.
        """
        scr = self.get_scoped_value(response, ['Độ phân giải', 'Màn hình'])
        return scr if scr else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Độ phân giải'])
            
            res = ''.join(res.split())
            
            search_value = re.search(r'\d+x\d+', res)
            if search_value:
                res = search_value.group()
            else:
                res = "n/a"
            
            return res
        except:
            return "n/a"
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        scr = self.get_scoped_value(response, ['Tần số quét', 'Màn hình'])
        return scr if scr else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Tần số quét'])
            search_value = re.search(r'\d+(\s)?Hz', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('Hz')[0])
            else:
                res = "n/a"

            return res
        except:
            return "n/a"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        scr = self.get_scoped_value(response, ['Công nghệ màn hình', 'Màn hình'])
        return scr if scr else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Công nghệ màn hình'])
            
            search_value = re.search(r'\d+\s*nits', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('nits')[0])
            else:
                res = "n/a"
                
            return res
        except:
            return "n/a"
    
    # Battery
    def parse_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Whr from the response.
        """
        battery = self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
        return battery if battery else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
            res = res.lower()
            
            search_value = re.search(r'\d+\s*whr', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('whr')[0])
            else:
                res = "n/a"
            
            return res
        except:
            return "n/a"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        battery = self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
        return battery if battery else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
            res = res.lower()
            search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells', res)
            
            if search_value:
                res = int(search_value.group()[0])
            else:
                res = "n/a"
            
            return res
        except:
            return "n/a"
    
    # Size
    def parse_size(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        size = self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
        return size if size else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
            
            values = [float(num) for num in re.findall(r'-?\d+\.\d+|-?\d+', res)]
            values = sorted(values[:3], reverse=True)
            
            res = values[2] if values[2] < 100 else values[0] / 10
                
            return round(res, 2)
        except:
            return "n/a"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        weight = self.get_scoped_value(response, ['Trọng Lượng'])
        return weight if weight else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Trọng Lượng'])
            res = re.search(r'(\d+(\.\d+)?)\s*(kg|Kg|KG)', res)
            
            if res:
                res = float(res.group(1))
            else:
                res = "n/a"
                
            return res
        except:
            return "n/a"
    
    # Connectivity
    def parse_connectivity(self, response: Response):
        ketnoi = self.get_scoped_value(response, ['Kết nối USB']) + self.get_scoped_value(response, ['Kết nối HDMI/VGA']) + self.get_scoped_value(response, ["Tai nghe"])
        return ketnoi if ketnoi else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Kết nối HDMI/VGA'])
            res = res.lower()
            
            if res:
                port_search = re.search(pattern, res)
                return 1 if port_search else 0
            else:
                return "n/a"
            
        except:
            return "n/a"
        
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        os = self.get_scoped_value(response, ['Hệ điều hành', "OS"])
        return os if os else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Hệ điều hành', "OS"])
            
            res = res.split('+')[0]
            for removal in ['Single Language']:
                res = res.replace(removal, '')
            
            return res.strip()
        except:
            return "n/a"
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        color = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"])
        return color if color else 'n/a'
        try:
            res = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"])
            
            if res:
                return res.strip()
            else:
                return "n/a"
        except:
            return "n/a"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        warranty = response.xpath("//b[contains(., 'Bảo hành')]/text()").get()
        return warranty if warranty else 'n/a'
    
        try:
            search_value = re.search(r'(\d+)\s*tháng', res)
            if search_value:
                res = int(search_value.group(1))
            else:
                search_value = re.search(r'(\d+)\s*Tháng', res)
                if search_value:
                    res = int(search_value.group(1))
                else:
                    res = "n/a"
            return res
            
        except:
            return "n/a"
    
    # Release Date: Not available
    def parse_release_date(self, response: Response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        return "n/a"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        price = response.xpath("//tr//td[contains(., 'Giá khuyến mại:')]/following-sibling::td//b/text()").get()
        return price if price else 'n/a'
        try:
            return response.xpath("//tr//td[contains(., 'Giá khuyến mại:')]/following-sibling::td//b/text()").get()

            for path in paths:
                price = response.xpath(path).get()
                
                if price:
                    price = price.replace('₫', '').replace('.', '').strip()
                    return int(price)
            return "n/a"
        except:
            return "n/a"