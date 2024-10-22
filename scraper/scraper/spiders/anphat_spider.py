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

    def get_scoped_value(self, response: Response, list_names):
        possible_values = [
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
        return self.get_scoped_value(response, ["Hãng sản xuất"])
        try:
            brand = self.get_scoped_value(response, ["Hãng sản xuất"]).split()
            if brand[0] == "laptop":
                return brand[1]
            else:
                return brand[0]
        except:
            return "n/a"
        
    
    def parse_name(self, response: Response):
        return self.get_scoped_value(response, ["Tên sản phẩm"])
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
        return self.get_scoped_value(response, ['Công nghệ CPU'])
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
        return self.get_scoped_value(response, ['Card màn hình'])
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
        return self.get_scoped_value(response, ['RAM'])
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
        return self.get_scoped_value(response, ['Loại RAM'])
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
        return self.get_scoped_value(response, ['Dung lượng'])
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
        return self.get_scoped_value(response, ['Dung lượng'])
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
        return self.get_scoped_value(response, ['Webcam', 'Camera'])
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
        return self.get_scoped_value(response, ['Kích thước màn hình'])
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
        return self.get_scoped_value(response, ['Độ phân giải'])
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
        return self.get_scoped_value(response, ['Tần số quét'])
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
        return self.get_scoped_value(response, ['Công nghệ màn hình'])
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
        return self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
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
        return self.get_scoped_value(response, ['Pin', 'Kiểu Pin'])
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
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        return self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
        try:
            res = self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])

            values = [float(num) for num in re.findall(r'-?\d+\.\d+|-?\d+', res)]
            values = sorted(values[:3], reverse=True)
            
            res = values[0] if values[0] < 100 else values[0] / 10
            
            return round(res, 2)
        except:
            return "n/a"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
        """
        return self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
        try:
            res = self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
            values = [float(num) for num in re.findall(r'-?\d+\.\d+|-?\d+', res)]
            values = sorted(values[:3], reverse=True)

            res = values[1] if values[1] < 100 else values[0] / 10
                
            return round(res, 2)
        except:
            return "n/a"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        return self.get_scoped_value(response, ['Kích thước (Dài x Rộng x Cao)'])
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
        return self.get_scoped_value(response, ['Trọng Lượng'])
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
    def parse_number_usb(self, response: Response, pattern):
        return self.get_scoped_value(response, ['Kết nối USB'])
        try:
            res = self.get_scoped_value(response, ['Kết nối USB'])
            res = res.lower()
            if re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE) != '':
                res = re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE)
            
            
            while '(' in res and ')' in res:
                res = re.sub(r'\([^()]*\)', '', res)

            res = re.split(r'[\n,]', res)
            count = 0
            for line in res:
                if re.search(pattern, line):
                    line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                    val = line.split()[0]
                    if val[-1] == 'x': val = val[:-1]
            
                    if val.isnumeric():
                        count += int(val)
                    else:
                        count += 1
            
            return count
        except:
            return "n/a"
    
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return self.parse_number_usb(response, r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a)\b')
    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return self.parse_number_usb(response, r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b')
    
    def parse_has_port(self, response: Response, pattern):
        return self.get_scoped_value(response, ['Kết nối HDMI/VGA']) + self.get_scoped_value(response, ["Tai nghe"])
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
    
    def parse_number_hdmi_ports(self, response: Response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return self.parse_has_port(response, r'\bhdmi\b')
    
    def parse_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return self.parse_has_port(response, r'\brj-45|ethernet\b')
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        return self.parse_has_port(response, r'\bheadphone|3.5mm\b')
    
    # Operating System
    def parse_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        return self.get_scoped_value(response, ['Hệ điều hành', "OS"])
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
        return self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"])
        try:
            res = self.get_scoped_value(response, ['Màu sắc', "Mầu sắc"])
            
            if res:
                return res.strip()
            else:
                return "n/a"
        except:
            return "n/a"
    
    # Origin: Not available
    def parse_origin(self, response: Response): 
        """
        Extracts the origin of the laptop from the response.
        Example: China, Taiwan, USA, etc.
        """
        return self.get_scoped_value(response, ['Xuất xứ'])
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        try:
            
            return response.xpath("//b[contains(., 'Bảo hành')]/text()").get()
                
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
        try:
            return response.xpath("//td[contains(., 'Giá khuyến mại:')]/following-sibling::td//b/text()").get()

            for path in paths:
                price = response.xpath(path).get()
                
                if price:
                    price = price.replace('₫', '').replace('.', '').strip()
                    return int(price)
            return "n/a"
        except:
            return "n/a"