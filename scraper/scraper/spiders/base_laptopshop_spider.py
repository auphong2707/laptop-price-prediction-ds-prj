import scrapy
from scrapy.http import Response, Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from scrapy.selector import Selector
import time
import logging
from fake_useragent import UserAgent
from selenium.webdriver.firefox.service import Service


# logging.disable()

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
    require_specific_transform = False
    
    source = None
    
    def _get_driver_options(self):
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = 'none'
        options.add_argument('--headless')
        
        options.set_preference('dom.webnotifications.enabled', False)  # Disable notifications
        options.set_preference('security.cert_pinning.enforcement_level', 0)  # Ignore certificate errors
        options.set_preference('browser.safebrowsing.malware.enabled', False)  # Disable safe browsing (optional)

        # To reduce GPU load (Firefox doesn’t have a direct equivalent to --disable-gpu):
        options.set_preference('layers.acceleration.disabled', True)

        # You can also set other preferences as needed
        options.set_preference('permissions.default.image', 2)  # Disable image loading to speed up browsing
        options.set_preference("privacy.trackingprotection.enabled", True) # Enable tracking protection
        
        return options

    _num_product = 0
    
    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.ua = UserAgent()
        self.driver = webdriver.Firefox(options=self._get_driver_options(), service=FirefoxService(executable_path='/usr/local/bin/geckodriver'))
        
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
        return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def parse_one_observation(self, response: Response):
        if not self.yield_condition(response):
            return
        
        if self.selenium_product_request:
            response = response.replace(body=self.get_source_selenium(response.url))
            if not self.yield_condition(response):
                return

        self._num_product += 1
        print(f'Found item: {self._num_product}')
        
        yield {
            'source': self.source,
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
            'size': self.parse_size(response),
            'weight': self.parse_weight(response),
            'connectivity': self.parse_connectivity(response),
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
                    time.sleep(1)
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
        
        html = self.driver.page_source

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return html


class BaseLaptopshopPageSpider(BaseLaptopshopSpider):
    page_css = None
    selenium_page_request = False
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                headers={'User-Agent': self.ua.random},
                dont_filter=True
            )

    def parse(self, response: Response):
        if self.selenium_page_request and response.status == 200:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: () => '{self.ua.random}'}});")
            self.driver.get(response.url)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            wait = WebDriverWait(self.driver, 20)
            
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            self.driver.execute_script("document.body.style.zoom='1%'")
            
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            response = response.replace(body=self.driver.page_source)
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        
        print('Reached page:', response.url)
        
        for url in response.css(self.product_site_css).getall():
            yield response.follow(
                url=url,
                callback=self.parse_one_observation,
                headers={'User-Agent': self.ua.random}
            )
        
        pages = response.css(self.page_css).getall()
        for page in pages:
            if response.urljoin(page) in self.start_urls:
                continue
            
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
