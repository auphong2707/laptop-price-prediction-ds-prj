import scrapy
from scrapy.http import Response
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector
import time 
# for firefox usage
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent

from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
class FPTShopScraper(BaseLaptopshopLoadmoreButtonSpider):
    name = "fptshop_spider"
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']
    product_site_css = "h3.ProductCard_cardTitle__HlwIo a::attr(href)"
    allowed_domains = ['fptshop.com.vn']
    loadmore_button_css = ".Button_root__LQsbl.Button_btnSmall__aXxTy.Button_whitePrimary__nkoMI.Button_btnIconRight__4VSUO.border.border-iconDividerOnWhite.px-4.py-2"
    close_button_xpaths = ["//button[@class='close']"]
    service = Service(executable_path='/snap/bin/geckodriver')
    
    show_technical_spec_button_xpath = "//button[span[text()='Tất cả thông số']]"
    selenium_product_request = True

    def get_source_selenium(self, url: str):
        ua = UserAgent()
        USER_AGENT = ua.random 
        
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        option.set_preference("general.useragent.override", USER_AGENT)
        
        driver = webdriver.Firefox(options=option, service=self.service)
        driver.get(url)
        
        # Scroll down the page slowly
        scroll_pause_time = 0.01 # Time to wait between scrolls
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        driver.execute_script("document.body.style.zoom='10%'")

        for i in range(1, scroll_height, 30):
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
                buttons = driver.find_elements(By.XPATH, self.show_technical_spec_button_xpath)
                
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
        
        response = Selector(text=driver.page_source)
        driver.quit()
        
        return response


    def start_requests(self):
        
        for url in self.start_urls:     
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            options.set_preference("general.useragent.override", self.ua.random)
            
            driver = webdriver.Firefox(options=options, service=self.service)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            
            # Scroll and click "Load More" until all the content is loaded
            while True:
                time.sleep(1)
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
                
                try:
                    load_more_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                    )
                    driver.execute_script("arguments[0].click();", load_more_button)
                    time.sleep(3)
                    load_more_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                    )
                except Exception:
                    print("No more 'Load More' button")
                    break
                
            # Get all the products links
            page_source = Selector(text=driver.page_source)
            driver.quit()
            print('Quit driver')
            # Extracting the feature from a product website
            for product_url in page_source.css(self.product_site_css).getall():
                yield Response(url=url).follow(
                    url=product_url,
                    callback=self.parse_one_observation
                )
                def get_scoped_value(self, response, names):
                    possible_values = [
                        "//span[text()='{}']/ancestor::div[1]/following-sibling::div//span/b/text()".format(name)
                        for name in names
                    ]

                    for value in possible_values:
                        scope = response.xpath(value).getall()
                        if scope:
                            return '\n'.join(scope)
                    
                    return None
    def get_scoped_value(self, response, names):
        possibile_values = [
            "//span[text()='{}']/ancestor::div[1]/following-sibling::div//span/text()".format(name)
            for name in names
        ]

        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return '\n'.join(scope)
         
        return None
    

    def parse_brand(self, response: Response):
        """
        Extracts the brand of the laptop from the title attribute of the anchor tag.
        Example: Dell, HP, Acer, etc.
        """
        try:
            title = response.css('h1.text-textOnWhitePrimary::text').get()
            if title:
                # Extract the brand, assuming it's the first word in the title
                if 'Macbook' in title or 'MacBook' in title: 
                    return 'Apple'
                else: 
                    brand = title.split()[1]  # Assuming the title is formatted as "Laptop [Brand] [Model]"
                    return brand.strip()
            else:
                return 'N/A'
        except Exception as e:
            print("Error")
            return 'N/A'
    def parse_name(self, response: Response): 
        """
        Extracts the name of the laptop from the response.
        """
        try:
            # Get the initial part of the name
            title = response.css('h1.text-textOnWhitePrimary::text').get()
            if not title:
                return 'N/A'

            # Extract the model number from the span element
            model_number = response.css('h1.text-textOnWhitePrimary > span::text').get()

            # Combine the parts to get the full name
            if model_number:
                full_name = f"{title.replace('Laptop ', '').strip()} {model_number.strip()}"
            else:
                full_name = title.replace('Laptop ', '').strip()

            return full_name

        except Exception as e:
            print("Error:", e)  # Print the actual error for debugging
            return 'N/A'
    
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU details from the response and combines them.
        """
        try:
            # Extract individual CPU features using CSS selectors
            cpu_brand = response.css('#spec-item-0 > div:nth-child(2) > span:nth-child(2)::text').get()
            cpu_technology = response.css('#spec-item-0 > div:nth-child(3) > span:nth-child(2)::text').get()
            cpu_type = response.css('#spec-item-0 > div:nth-child(4) > span:nth-child(2)::text').get()

            if cpu_brand and cpu_technology and cpu_type:
                # Combine the features into a single string
                cpu_details = f"{cpu_brand} {cpu_technology} {cpu_type}"
                return cpu_details.strip()
            else: 
                return 'N/A'

        except Exception as e:
            print("Error:", e)
            return 'N/A'
    
    def parse_vga(self, response):
        """
        Extracts the VGA (not onboard) details from the response and combines them.
        """
        try:
            vga_text = self.get_scoped_value(response, ['Đồ họa'])
            return vga_text
            # if vga_text: 
            #     vga_text = vga_text.strip().split('\n')
            #     for i in range(len(vga_text)): 
            #         if vga_text[i].lower() == "tên đầy đủ (card rời)": 
            #             return vga_text[i+1]
            return 'N/A'
        except Exception as e:
            print("Error:", e)
            return 'N/A'
        
    def parse_ram_amount(self, response):
        """
        Extract the RAM amount from the response
        """
        try: 
            ram_text = self.get_scoped_value(response, ['RAM'])
            return ram_text
            # if ram_text: 
            #     # extract the number and GB
            #     ram_text = ram_text.split('\n')
            #     for i in range(len(ram_text)):
            #         if 'Dung lượng' in ram_text[i]: 
            #             ram = ram_text[i+1]
            #             if 'thanh' in ram: 
            #                 ram = ram.split('(')[0]
            #             return ram.strip()
            # return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'N/A'
    
    def parse_ram_type(self, response):
        """
        Extract the RAM type from the response
        """
        try: 
            ram_text = self.get_scoped_value(response, ['RAM'])
            if ram_text: 
                # extract the number and GB
                ram_text = ram_text.split('\n')
                for i in range(len(ram_text)):
                    if 'Loại' in ram_text[i]: 
                        ram = ram_text[i+1]
                        return ram.strip()
            return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'N/A'
    
    def parse_storage_amount(self, response):
        """
        Extract the storage amount from the response
        """
        try: 
            storage_text = self.get_scoped_value(response, ['Lưu trữ'])
            if storage_text: 
                # extract the number and GB
                storage_text = storage_text.split('\n')
                for i in range(len(storage_text)):
                    if 'Dung lượng' in storage_text[i]: 
                        storage = storage_text[i+1]
                        if 'GB' not in storage: 
                            storage = storage + "GB"
                        return storage.strip()
            return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'N/A'
    def parse_storage_type(self, response):
        """
        Extract the storage type from the response
        """
        try: 
            storage_text = self.get_scoped_value(response, ['Lưu trữ'])
            if storage_text: 
                # extract the number and GB
                storage_text = storage_text.split('\n')
                for i in range(len(storage_text)):
                    if 'Kiểu ổ cứng' in storage_text[i]: 
                        storage = storage_text[i+1]
                        return storage.strip()
            return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'N/A'
    def parse_height(self, response):
        return super().parse_height(response)
    def parse_width(self, response):
        return super().parse_width(response)
    def parse_depth(self, response):
        return super().parse_depth(response)