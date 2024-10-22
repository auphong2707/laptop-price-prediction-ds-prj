import os
import time
import scrapy
from scrapy.http import Response
import re
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent

logging.disable()

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ["cellphones.com.vn"]
    start_urls = [
        'https://cellphones.com.vn/laptop-asus-tuf-gaming-a14-fa401wv-rg061ws.html',
        'https://cellphones.com.vn/laptop-msi-modern-15-b12mo-487vn.html',
        'https://cellphones.com.vn/macbook-air-m2-2022-16gb.html',
        'https://cellphones.com.vn/laptop-lenovo-loq-15iax9-83gs001svn.html',
        'https://cellphones.com.vn/laptop-asus-gaming-rog-zephyrus-g16-gu603vu-n4019w.html',
    ]
    
    close_button_xpaths = ["//button[@class='cancel-button-top']"]
    
    def get_scoped_value(self, response: Response, names):
        possibile_values = [
                "//li[contains(@class, 'technical-content-modal-item')]//p[text()='{}']/following-sibling::div[1]/text()".format(name)
                for name in names
            ] + [
                "//li[contains(@class, 'technical-content-modal-item')]//p[a[text()='{}']]/following-sibling::div[1]/text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return '\n'.join(scope)
            
        return None
    
    # [PARSE FEATURES SECTION: START]
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            res = response.css('.box-product-name h1::text').get()
            
            if "Macbook" in res or "MacBook" in res:
                return "Apple"
            
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            
            return res.split()[0]
        except:
            return "N/A"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            res = response.css('.box-product-name h1::text').get()
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ', '- Chỉ có tại CellphoneS']:
                res = res.replace(removal, '')

            res = re.sub(r'\([^()]*\)', '', res)
            search_value = re.search('(?<!\w)(\d+)GB(?!\w)', res)
            if search_value:
                res = res.split(search_value.group())[0]
            
            if "Macbook" in res:
                res = "Apple " + ' '.join(res.split()[:2] + res.split()[-1:])
            
            if not res[-1].isalnum():
                res = res[:-1]
            
            return res.strip()
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Loại CPU'])
            
            if self.parse_brand(response) == "Apple":
                res = res.replace('nhân', 'cores')
            else:
                for removal in ['®', '™', ' processor', ' Processor', 'Mobile', 'with Intel AI Boost', 'Processors', '(TM)', '(R)']:
                    res = res.replace(removal, '')

                res = re.sub(r'\s*(\d{1,2}th Gen|Gen \d{1,2}th)\s*', ' ', res)
                
                special_sep = re.search(r'\b(\d+\.\d+\s?upto\s?\d+\.\d+GHz|\d+\.\d+\s?GHz|\d+\s?GB|dGB)\b', res)
                if special_sep:
                    res = res.split(special_sep.group())[0]
                    
                for sep in ['(', 'up to', 'Up to', 'upto', ',']:
                    res = res.split(sep)[0]
                    
                if res.startswith(('i', 'Ultra')):
                    res = 'Intel Core ' + res
                    
                if res.startswith('Ryzen'):
                    res = 'AMD ' + res
            
            return ' '.join(res.split())
        except Exception as e:
            print("ERROR", e)
            return "N/A"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Loại card đồ họa'])
            
            res = re.sub(r'[^\x20-\x7E]|®|™|integrated|gpu', ' ', res, flags=re.IGNORECASE)              
            res = re.sub(r'\([^()]*\)', '', res)
            res = ' '.join(res.split())

            if self.parse_brand(response) == "Apple":
                res = 'N/A'
            else:
                if res.lower() in [
                        "intel arc graphics", 
                        "amd radeon graphics", 
                        "intel iris xe graphics",
                        "intel uhd graphics",
                        "intel iris xe graphics intel uhd graphics",
                        "on board on board",
                        "amd radeon graphics amd radeon graphics",
                        "intel graphics",
                        "intel arcintel arc",
                        "onboardonboard",
                        None
                    ]:
                    res = "N/A"
                else:
                    special_sep = re.search(r'\d+\s?GB|GDDR\d+', res)
                    if special_sep:
                        res = res.split(special_sep.group())[0]

                    for spliter in [' with ', ' Laptop ', '+', ',',  'Up', 'upto', 'Upto', 'up to', 'ROG']:
                        res = res.split(spliter)[0]
                        
                    if res.lower().split()[0] == 'nvidia':
                        res = 'NVIDIA ' + ' '.join(res.split()[1:])
                        
                    if res.startswith('GeForce'):
                        res = 'NVIDIA ' + res
                        
                    res = re.sub(r'(\s\d{3,4})Ti', r'\1 Ti', res)
                    res = re.sub(r'(TX)(\d{4})', r'\1 \2', res)
                    
                    if "Gefore" in res:
                        res = res.replace("Gefore", "Geforce")
                    
                    if "NVIDIA" in res:
                        res = res[res.index("NVIDIA"):]
                    
            return res.strip()
        except:
            return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Dung lượng RAM'])
            
            search_value = re.search(r'\d+\s?GB', res)
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
        try:
            res = self.get_scoped_value(response, ['Loại RAM'])
            
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
        try:
            res = self.get_scoped_value(response, ['Ổ cứng'])
            res = ''.join(res.split())
        
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
        try:
            
            for name in ['Ổ cứng', 'Tính năng đặc biệt']:
                res = self.get_scoped_value(response, [name])
            
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

                if res != "N/A":
                    break
            
            return res.strip()
        except:      
            return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        try:
            res = ''.join(self.get_scoped_value(response, ['Webcam']).lower().split())

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
        try:
            res = self.get_scoped_value(response, ['Kích thước màn hình']).lower()
            res = res.replace(',', '.')
            res = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch|”)', res)
            
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
        Example: HD, FHD, 4K.
        """
        try:
            res = ''.join(self.get_scoped_value(response, ['Độ phân giải màn hình']).lower().split())
            res = res.replace('*', 'x')
            
            search_value = re.search(r'(\d{3,4})x(\d{3,4})', res)
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
        try:
            res = self.get_scoped_value(response, ['Tần số quét']).lower()
            
            search_value = re.search(r'\d+\s*hz', res)
            if search_value:
                res = search_value.group()
                res = int(res.split('hz')[0])
            else:
                res = "N/A"

            return res
        except:
            return "N/A"
    
    def parse_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Công nghệ màn hình']).lower()
            
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
        try:
            res = self.get_scoped_value(response, ['Pin']).lower().replace(',', '.')
            res = re.sub(r'[()]', '', res)
        
            search_value = re.search(r'(\d+(?:\.\d+)?)\s*(wh|battery)', res)
            if search_value:
                res = float(search_value.group().split('wh')[0].split('battery')[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    def parse_battery_cells(self, response: Response):
        """
        Extracts the number of battery cells from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Pin']).lower()
            
            search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells|Chân\s*(\d+)', res)
            
            if search_value:
                res = int(search_value.group()[0])
            else:
                res = "N/A"
            
            return res
        except:
            return "N/A"
    
    # Size
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')

             # Use regex to find all numbers, including those after a hyphen
            numbers = re.findall(r'\d+\.?\d*', res)
            
            # Collect the first three numbers and any number after a hyphen
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[0]
            res = res if res < 100 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')

             # Use regex to find all numbers, including those after a hyphen
            numbers = re.findall(r'\d+\.?\d*', res)
            
            # Collect the first three numbers and any number after a hyphen
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[1]
            res = res if res < 100 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Kích thước']).replace(',', '.')
            numbers = re.findall(r'\d+\.?\d*', res)
            
            # Collect the first three numbers and any number after a hyphen
            extracted_numbers = numbers[:3]
            hyphenated_number = re.search(r'-(\d+\.?\d*)', res)
            if hyphenated_number:
                extracted_numbers[-1] = hyphenated_number.group(1)
            
            extracted_numbers = [float(num) for num in extracted_numbers]
            res = sorted(extracted_numbers, reverse=True)[2]
            res = res if res < 5 else res / 10
            
            return round(res, 2)
        except:
            return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        try:
            res = self.get_scoped_value(response, ['Trọng lượng']).lower()
            res = res.replace(',', '.')
        
            value_kg = re.search(r'(\d+(\.\d+)?)\s*(kg)', res)
            value_g = re.search(r'(\d+(\.\d+)?)\s*(gram|g)', res)
            
            if value_kg:
                res = float(value_kg.group(1))
            elif value_g:
                res = float(value_g.group(1)) / 1000
            else:
                res = "N/A"
                
            return res
        except:
            return "N/A"
    
    # Connectivity
    def parse_number_usb(self, response: Response, pattern_a: str, pattern_c: str, get_a=True):
        try:
            res = self.get_scoped_value(response, ['Cổng giao tiếp'])
            res = res.lower()
            if re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE) != '':
                res = re.sub(r'^\s*[•-].*\n?', '', res, flags=re.MULTILINE)
            
            while '(' in res and ')' in res:
                res = re.sub(r'\([^()]*\)', '', res)
            
            res = re.split(r'[\n,]', res)
            count = 0
            for line in res:
                if get_a:
                    if re.search(pattern_a, line) and not re.search(pattern_c, line):
                        line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                        val = line.split()[0]
                        if val[-1] == 'x': val = val[:-1]
                
                        if val.isnumeric():
                            count += int(val)
                        else:
                            count += 1
                else:
                    if re.search(pattern_c, line):
                        line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                        val = line.split()[0]
                        if val[-1] == 'x': val = val[:-1]
                
                        if val.isnumeric():
                            count += int(val)
                        else:
                            count += 1
            
            return count
        except:
            return "N/A"
    
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return self.parse_number_usb(response, 
                                     r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b',  
                                     r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b',
                                     get_a=True)

    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return self.parse_number_usb(response, 
                                     r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b',  
                                     r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b',
                                     get_a=False)
    
    def parse_has_port(self, response: Response, pattern):
        try:
            res = self.get_scoped_value(response, ['Cổng giao tiếp'])
            res = res.lower()
            
            if res:
                port_search = re.search(pattern, res)
                return 1 if port_search else 0
            else:
                return "N/A"
            
        except:
            return "N/A"
    
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
        try:
            res = self.get_scoped_value(response, ['Hệ điều hành'])
            res = re.sub(r'Bản Quyền|[^\x20-\x7E]|Single Language|SL|64', ' ', res, flags=re.IGNORECASE)
            res = ' '.join(res.split())
            
            for sep in ['+', ',', '-', ';']:
                res = res.split(sep)[0]
                
            if 'Windows' in res:
                res = res[res.index('Windows'):]
            
            
            return res.strip()
        except:
            return "N/A"
    
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        try:
            res = response.css('.item-variant-name::text').getall()
            
            if res:
                res = '/'.join(res)
                return res.strip()
            else:
                return "N/A"
        except:
            return "N/A"
    
    # Origin: Not available
    def parse_origin(self, response: Response): 
        """
        Extracts the origin of the laptop from the response.
        Example: China, Taiwan, USA, etc.
        """
        return "N/A"
    
    # Warranty
    def parse_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        try:
            res = response.xpath("//a[@href='https://cellphones.com.vn/chinh-sach-bao-hanh']/\
                                 parent::div[contains(@class, 'description')]/text()[1]").get()
                
            res = ' '.join(res.split()).lower()
            search_value = re.search(r'(\d+)\s*tháng', res)
    
            if search_value:
                res = int(search_value.group(1))
            else:
                res = "N/A"
            
            return res
            
        except:
            return "N/A"
    
    # Release Date: Not available
    def parse_release_date(self, response: Response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        return "N/A"
    
    # Price
    def parse_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        try:
            price = response.xpath("//div[@id='trade-price-tabs']//div[contains(@class, 'tpt-box') \
                and contains(@class, 'active')]//p[contains(@class, 'tpt---sale-price')]/text()").get()
            
            if price:
                price = price.replace('đ', '').replace('.', '').strip()
                return int(price)
            else:
                return "N/A"
        except:
            return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def start_requests(self):
        # Using SeleniumRequest instead of Scrapy's normal request
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10, # Wait for 10 seconds
                dont_filter=True
            )
    
    def parse(self, response: Response):
        ua = UserAgent()
        USER_AGENT = ua.random 
        
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        option.set_preference("general.useragent.override", USER_AGENT)
        
        service = Service(log_path=os.devnull)  # Redirect geckodriver logs to null
        
        driver = webdriver.Firefox(options=option, service=service)
        driver.get(response.url)
        
        # Scroll down the page slowly
        scroll_pause_time = 0.05 # Time to wait between scrolls
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(1, scroll_height, 100):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(scroll_pause_time)
            
            for xpath in self.close_button_xpaths:
                try:
                    buttons = driver.find_elements(By.XPATH, xpath)
                    
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            button.click()
                            print("Closed the modal successfully.")
                            break
                except Exception as e:
                    print("Failed to close the modal:", e)
            
            opened_modal = False
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR, '.button__show-modal-technical')
                
                for button in buttons:
                    driver.execute_script("arguments[0].click();", button)
                    print("Opened the modal successfully.")
                    opened_modal = True
                    break
            except:
                pass
                
            if opened_modal:
                break
            
        if not opened_modal:
            print("Failed to open the modal.")
        
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        response = scrapy.Selector(text=driver.page_source)
        driver.quit()

        yield {
            'brand': self.parse_brand(response),
            'name': self.parse_name(response),
            'cpu': self.parse_cpu(response),
            'vga': self.parse_vga(response),
            'ram_amount': self.parse_ram_amount(response),
            'ram_type': self.parse_ram_type(response),
            'storage_amount': self.parse_storage_amount(response),
            'storage_type': self.parse_storage_type(response),
            'webcam_resolution': self.parse_webcam_resolution(response),
            'screen_size': self.parse_screen_size(response),
            'screen_resolution': self.parse_screen_resolution(response),
            'screen_refresh_rate': self.parse_screen_refresh_rate(response),
            'screen_brightness': self.parse_screen_brightness(response),
            'battery_capacity': self.parse_battery_capacity(response),
            'battery_cells': self.parse_battery_cells(response),
            'width': self.parse_width(response),
            'depth': self.parse_depth(response),
            'height': self.parse_height(response),
            'weight': self.parse_weight(response),
            'number_usb_a_ports': self.parse_number_usb_a_ports(response),
            'number_usb_c_ports': self.parse_number_usb_c_ports(response),
            'number_hdmi_ports': self.parse_number_hdmi_ports(response),
            'number_ethernet_ports': self.parse_number_ethernet_ports(response),
            'number_audio_jacks': self.parse_number_audio_jacks(response),
            'default_os': self.parse_default_os(response),
            'color': self.parse_color(response),
            'origin': self.parse_origin(response),
            'warranty': self.parse_warranty(response),
            'release_date': self.parse_release_date(response),
            'price': self.parse_price(response)
        }