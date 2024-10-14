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

class BaseLaptopshopPageSpider(BaseLaptopshopSpider):
    page_css = None
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse
            )
    
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
        
        pages = response.css(self.page_css).getall()
        for page in pages:
            
            yield response.follow(
                url=page,
                callback=self.parse
            )
            
class BaseLaptopshopLoadmoreButtonSpider(BaseLaptopshopSpider):
    
    loadmore_button_css = None
    close_button_xpaths = []
    
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
        wait = WebDriverWait(driver, 10) # Wait to allow the button to appear
        
        time.sleep(5)
        # Try to find and click the close button from the list of XPaths
        close_button_found = False
        for xpath in self.close_button_xpaths:
            try:
                buttons = driver.find_elements(By.XPATH, xpath)  # Get all buttons with class 'close'
                
                for button in buttons:
                    # Here you can add more specific checks, like checking text or SVG
                    if button.is_displayed() and button.is_enabled():  # Ensure the button is visible and clickable
                        button.click()
                        print("Closed the modal successfully.")
                        break
                else:
                    print("No clickable close button found.")
            except Exception as e:
                print("Failed to close the modal:", e)

        if not close_button_found:
            print("No close button found from the provided list.")
        
        
        # Scroll and click "Load More" until all the content is loaded
        while True:
            try:
                load_more_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                )
                load_more_button.click()
                
                # Wait for new content to load (if needed)
                time.sleep(5)
            except Exception:
                # Break the loop if there's no more "Load More" button or something goes wrong
                print("No more 'Load More' button")
                break

        
        # Get all the products links
        product_site_requests = self.get_product_sites(response, Selector(text=driver.page_source))
        
        # Extracting the feature from a product website
        for site_request in product_site_requests:
            yield site_request
