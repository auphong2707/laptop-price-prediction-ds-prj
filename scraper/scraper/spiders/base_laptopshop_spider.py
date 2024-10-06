import scrapy
from scrapy.http import Response, Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector
import time


class BaseLaptopshopSpider(scrapy.Spider):
    
    product_site_css = None
    
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
    
    def parse_screen_ratio(self, response: Response): 
        """
        Extracts the screen ratio from the response.
        Example: 16:9, 16:10, 4:3.
        """
        return "N/A"
    
    def parse_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        return "N/A"
    
    def parse_screen_color_gamut(self, response: Response): 
        """
        Extracts the screen color gamut in sRGB from the response.
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
        Extracts the battery capacity in Wh from the response.
        """
        return "N/A"
    
    # Size
    def parse_length(self, response: Response):
        """
        Extracts the length of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_width(self, response: Response):
        """
        Extracts the width of the laptop in cm from the response.
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
    
    # Color
    def parse_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        return "N/A"
    
    # Origin
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
        return "N/A"
    
    # Release Date
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
        return "N/A"
    
    # [PARSE FEATURES SECTION: END]
    
    def parse_one_observation(self, response: Response):
        return {
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
            'screen_ratio': self.parse_screen_ratio(response),
            'screen_refresh_rate': self.parse_screen_refresh_rate(response),
            'screen_color_gamut': self.parse_screen_color_gamut(response),
            'screen_brightness': self.parse_screen_brightness(response),
            'battery_capacity': self.parse_battery_capacity(response),
            'length': self.parse_length(response),
            'width': self.parse_width(response),
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

class BaseLaptopshopNextPageSpider(BaseLaptopshopSpider):
    
    next_page_css = None
    
    def get_product_sites(self, response: Response):
        """
        Extracts the product sites from the response.
        """
        return [response.follow(url=url, callback=self.parse_one_observation) for url in response.css(self.product_site_css).getall()]
    

    def parse(self, response: Response):
        # Get all the products links
        product_site_requests = self.get_product_sites(response)
        
        # Extracting the feature from a product website
        for site_request in product_site_requests:
            yield site_request
        
        next_page = response.css(self.next_page_css).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            
class BaseLaptopshopLoadmoreButtonSpider(BaseLaptopshopSpider):
    
    loadmore_button_css = None
    
    def get_product_sites(self, response: Response, body: Selector):
        """
        Extracts the product sites from the response.
        """
        return [
            response.follow(url, callback=self.parse_one_observation) 
            for url in body.css(self.product_site_css).getall()
        ]
    
    
    def start_requests(self):
        # Using SeleniumRequest instead of Scrapy's normal request
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10, # Wait for 10 seconds
            )
        
    def parse(self, response):
        driver = webdriver.Edge()
        driver.get(response.url)
        wait = WebDriverWait(driver, 5) # Wait to allow the button to appear
        
        # Scroll and click "Load More" until all the content is loaded
        while True:
            try:
                load_more_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                )
                load_more_button.click()
                
                # Wait for new content to load (if needed)
                time.sleep(2)
            except Exception as e:
                # Break the loop if there's no more "Load More" button or something goes wrong
                print("No more 'Load More' button")
                break

        
        # Get all the products links
        product_site_requests = self.get_product_sites(response, Selector(text=driver.page_source))
        assert type(product_site_requests[0]) is Request
        # Extracting the feature from a product website
        for site_request in product_site_requests:
            yield site_request
