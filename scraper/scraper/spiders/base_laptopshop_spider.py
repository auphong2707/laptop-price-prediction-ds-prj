import scrapy
from scrapy.http import Response, Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector
import time
import logging
from fake_useragent import UserAgent

logging.disable()

class BaseLaptopshopSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.TransformPipeline': 300
        }
    }

    product_site_css = None
    show_technical_spec_button_xpath = None
    close_button_xpaths = []
    selenium_product_request = False
    
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'none'
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    _num_product = 0
    
    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.ua = UserAgent()
        
    def __del__(self):
        self.driver.quit()
    
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
        return "N/A"
    
    def parse_name(self, response: Response):
        """
        Extracts the name of the laptop from the response.
        """
        return "N/A"
    
    # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        return "N/A"
    
    # VGA
    def parse_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        return "N/A"
    
    # RAM
    def parse_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        return "N/A"
    
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
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_depth(self, response: Response):
        """
        Extracts the depth of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_height(self, response: Response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        return "N/A"
    
    # Weight
    def parse_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        return "N/A"
    
    # Connectivity
    def parse_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return "N/A"
    
    def parse_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return "N/A"
    
    def parse_number_hdmi_ports(self, response: Response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return "N/A"
    
    def parse_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return "N/A"
    
    def parse_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
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
        return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def parse_one_observation(self, response: Response):
        if self.yield_condition(response):
            self._num_product += 1
            print(f'Found item: {self._num_product}')
            
            if self.selenium_product_request:
                response = self.get_source_selenium(response.url)

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
                'warranty': self.parse_warranty(response),
                'price': self.parse_price(response)
            }

    def get_source_selenium(self, url: str):
        time.sleep(1)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: () => '{self.ua.random}'}});")
        self.driver.get(url)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(4)
        if self.show_technical_spec_button_xpath:
            retries = 5
            while retries > 0:
                self.driver.execute_script("document.body.style.zoom='1%'")
                time.sleep(3)
                try:
                    buttons = self.driver.find_elements(By.XPATH, self.show_technical_spec_button_xpath)
                    if buttons:
                        break
                    else:
                        print("Technical spec button not found, reloading the page.")
                        self.driver.refresh()
                        time.sleep(2)
                        retries -= 1
                except Exception as e:
                    print("Error while trying to find the technical spec button:", e)
                    self.driver.refresh()
                    time.sleep(2)
                    retries -= 1
                
            for xpath in self.close_button_xpaths:
                try:
                    buttons = self.driver.find_elements(By.XPATH, xpath)
                    
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            button.click()
                            print("Closed the modal successfully.")
                            break
                except Exception as e:
                    print("Failed to close the modal:", e)
            
            opened_modal = False
            try:
                buttons = self.driver.find_elements(By.XPATH, self.show_technical_spec_button_xpath)
                
                for button in buttons:
                    self.driver.execute_script("arguments[0].click();", button)
                    print("Opened the modal successfully.")
                    opened_modal = True
                    break
            except:
                pass
                
            if not opened_modal:
                print("Failed to open the modal.")
        else:
            time.sleep(2)
            self.driver.execute_script("document.body.style.zoom='1%'")
            time.sleep(3)
        
        response = Selector(text=self.driver.page_source)
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        return response

class BaseLaptopshopPageSpider(BaseLaptopshopSpider):
    page_css = None
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse
            )
    

    def parse(self, response: Response):
        for url in response.css(self.product_site_css).getall():
            yield response.follow(
                url=url,
                callback=self.parse_one_observation,
                headers={'User-Agent': self.ua.random}
            )
        
        pages = response.css(self.page_css).getall()
        for page in pages:
            yield response.follow(
                url=page,
                callback=self.parse,
                headers={'User-Agent': self.ua.random}
            )
            
class BaseLaptopshopLoadmoreButtonSpider(BaseLaptopshopSpider):
    
    loadmore_button_css = None
    
    def start_requests(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        for url in self.start_urls:
            self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: () => '{self.ua.random}'}});")
            self.driver.get(url)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            wait = WebDriverWait(self.driver, 10)
            
            # Scroll and click "Load More" until all the content is loaded
            while True:
                time.sleep(1)
                for xpath in self.close_button_xpaths:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, xpath)
                        
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
                    self.driver.execute_script("arguments[0].click();", load_more_button)
                    print("'Load More' button clicked sucessfully.")
                    time.sleep(3)
                    load_more_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                    )
                except Exception:
                    print("No more 'Load More' button")
                    break
                
            # Get all the products links
            page_source = Selector(text=self.driver.page_source)
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            # Extracting the feature from a product website
            for product_url in page_source.css(self.product_site_css).getall():
                yield Response(url=url).follow(
                    url=product_url,
                    callback=self.parse_one_observation
                )
