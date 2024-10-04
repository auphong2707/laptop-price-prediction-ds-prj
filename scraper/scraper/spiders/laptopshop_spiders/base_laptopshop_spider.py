import scrapy
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseLaptopshopSpider(scrapy.Spider):
    
    product_site_css = None
    
    def get_product_sites(self, response: Response):
        """
        Extracts the product sites from the response.
        """
        return [response.follow(url) for url in response.css(self.product_site_css).getall()]
    
    # [GET FEATURES SECTION: START]
    # Brand
    def get_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        return "N/A"
    
    # CPU
    def get_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        return "N/A"
    
    # VGA
    def get_vga(self, response: Response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        return "N/A"
    
    # RAM
    def get_ram_amount(self, response: Response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        return "N/A"
    
    def get_ram_type(self, response: Response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        return "N/A"
    
    # Storage
    def get_storage_amount(self, response: Response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        return "N/A"
    
    def get_storage_type(self, response: Response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        return "N/A"
    
    # Webcam
    def get_webcam_resolution(self, response: Response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"
    
    # Screen
    def get_screen_size(self, response: Response): 
        """
        Extracts the screen size in inches from the response.
        """
        return "N/A"
    
    def get_screen_resolution(self, response: Response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"
    
    def get_screen_ratio(self, response: Response): 
        """
        Extracts the screen ratio from the response.
        Example: 16:9, 16:10, 4:3.
        """
        return "N/A"
    
    def get_screen_refresh_rate(self, response: Response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        return "N/A"
    
    def get_screen_color_gamut(self, response: Response): 
        """
        Extracts the screen color gamut in sRGB from the response.
        """
        return "N/A"
    
    def get_screen_brightness(self, response: Response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        return "N/A"
    
    # Battery
    def get_battery_capacity(self, response: Response): 
        """
        Extracts the battery capacity in Wh from the response.
        """
        return "N/A"
    
    # Weight
    def get_weight(self, response: Response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        return "N/A"
    
    # Connectivity
    def get_number_usb_a_ports(self, response: Response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return "N/A"
    
    def get_number_usb_c_ports(self, response: Response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return "N/A"
    
    def get_number_hdmi_ports(self, response: Response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return "N/A"
    
    def get_number_ethernet_ports(self, response: Response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return "N/A"
    
    def get_number_audio_jacks(self, response: Response):
        """
        Extracts the number of audio jacks from the response.
        """
        return "N/A"
    
    # Operating System
    def get_default_os(self, response: Response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        return "N/A"
    
    # Color
    def get_color(self, response: Response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        return "N/A"
    
    # Material
    def get_material(self, response: Response): 
        """
        Extracts the material of the laptop from the response.
        Example: Plastic, Metal, etc.
        """
        return "N/A"
    
    # Origin
    def get_origin(self, response: Response): 
        """
        Extracts the origin of the laptop from the response.
        Example: China, Taiwan, USA, etc.
        """
        return "N/A"
    
    # Warranty
    def get_warranty(self, response: Response): 
        """
        Extracts the warranty period in months from the response.
        """
        return "N/A"
    
    # Release Date
    def get_release_date(self, response: Response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        return "N/A"
    
    # Price
    def get_price(self, response: Response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        return "N/A"
    
    # [GET FEATURES SECTION: END]
    
    def get_one_observation(self, response: Response):
        return {
            'brand': self.get_brand(response),
            'cpu': self.get_cpu(response),
            'vga': self.get_vga(response),
            'ram_amount': self.get_ram_amount(response),
            'ram_type': self.get_ram_type(response),
            'storage_amount': self.get_storage_amount(response),
            'storage_type': self.get_storage_type(response),
            'webcam_resolution': self.get_webcam_resolution(response),
            'screen_size': self.get_screen_size(response),
            'screen_resolution': self.get_screen_resolution(response),
            'screen_ratio': self.get_screen_ratio(response),
            'screen_refresh_rate': self.get_screen_refresh_rate(response),
            'screen_color_gamut': self.get_screen_color_gamut(response),
            'screen_brightness': self.get_screen_brightness(response),
            'battery_capacity': self.get_battery_capacity(response),
            'weight': self.get_weight(response),
            'number_usb_a_ports': self.get_number_usb_a_ports(response),
            'number_usb_c_ports': self.get_number_usb_c_ports(response),
            'number_hdmi_ports': self.get_number_hdmi_ports(response),
            'number_ethernet_ports': self.get_number_ethernet_ports(response),
            'number_audio_jacks': self.get_number_audio_jacks(response),
            'default_os': self.get_default_os(response),
            'color': self.get_color(response),
            'material': self.get_material(response),
            'origin': self.get_origin(response),
            'warranty': self.get_warranty(response),
            'release_date': self.get_release_date(response),
            'price': self.get_price(response)
        }

class BaseLaptopshopNextPageSpider(BaseLaptopshopSpider):
    
    next_page_css = None

    def parse(self, response: Response):
        # Get all the products links
        product_sites = self.get_product_sites(response)
        
        # Extracting the feature from a product website
        for site in product_sites:
            yield self.get_one_observation(site)
        
        next_page = response.css(self.next_page_css).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            
class BaseLaptopshopLoadmoreButtonSpider(BaseLaptopshopSpider):
    
    loadmore_button_css = None
    
    def start_requests(self):
        # Using SeleniumRequest instead of Scrapy's normal request
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callable=self.parse,
                wait_time=10, # Wait for 10 seconds
            )
        
    def parse(self, response):
        driver = response.meta['driver']
        wait = WebDriverWait(driver, 10) # Wait to allow the button to appear
        
        # Scroll and click "Load More" until all the content is loaded
        while True:
            try:
                # Find the "Load more" button using its XPath
                load_more_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.loadmore_button_css))
                )
                load_more_button.click()
                
                # Wait for new content to load (if needed)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.product_site_css))
                )
            except Exception as e:
                # Break the loop if there's no more "Load More" button or something goes wrong
                print(e)
                break
            
        # Get all the products links
        product_sites = self.get_product_sites(driver.page_source)
        
        # Extracting the feature from a product website
        for site in product_sites:
            yield self.get_one_observation(site)
