import scrapy
from scrapy.http import Response, Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector
import time 
# for chrome usage
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager   

from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
class FPTShopScraper(BaseLaptopshopLoadmoreButtonSpider):
    name = "fptshop_spider"
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']
    product_site_css = "h3.ProductCard_cardTitle__HlwIo a::attr(href)"
    allowed_domains = ['fptshop.com.vn']
    # loadmore_button_css = "button.Button_root__LQsbI.Button.btnSmall__aXxTy.Button_whitePrimary__nIconRight__4V5UO"
    close_button_xpaths = ["//button[@class='close']"]
    
    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
        service = ChromeService(executable_path='/usr/local/bin/chromedriver')  # Update this to the correct path to your ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(response.url)
        wait = WebDriverWait(driver, 10)  # Wait to allow the button to appear
        
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

    
    def parse_one_observation(self, response: Response):
        """
        Parse the detailed information of a laptop after clicking the 'Tất cả thông số' button using Selenium with ChromeDriver.
        """
        # Parse these 2 features first, since it's not in the pop-up details
        brand = self.parse_brand(response)
        name = self.parse_name(response)
        url = response.url

        # Initialize the webdriver (using Chrome)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
        service = ChromeService(executable_path='/usr/local/bin/chromedriver')  # Update this to the correct path to your ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the webpage using the extracted URL
        driver.get(url)

        try:
            # Click the 'Tất cả thông số' button to open the detailed pop-up
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".min-h-max > div:nth-child(1) > button:nth-child(2)"))
            )
            button.click()

            time.sleep(1)
            response = Selector(text=driver.page_source)

            # Extract and return the product details
            yield {
                'brand': brand,
                'name': name,
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

        except Exception as e:
            print("Error while scraping:", str(e))

        finally:
            driver.quit()


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
            cpu_brands = response.css("#spec-item-0 > div:nth-child(2) > span:nth-child(2)").getall()
            # print("cpu_brands:", cpu_brands)  # Add this line
            cpu_technologys = response.css("#spec-item-0 > div:nth-child(3) > span:nth-child(2)::text").getall()
            # print("cpu_technologys:", cpu_technologys)  # Add this line
            cpu_types = response.css("#spec-item-0 > div:nth-child(4) > span:nth-child(2)::text").getall()
            # print("cpu_types:", cpu_types)  # Add this line
            for cpu_brand, cpu_technology, cpu_type in zip(cpu_brands, cpu_technologys, cpu_types):
                if cpu_brand and cpu_technology and cpu_type:
                    # Combine the features into a single string
                    cpu_details = f"{cpu_brand} {cpu_technology} {cpu_type}"
                    if cpu_details:
                        return cpu_details.strip()

                    else: 
                        return 'N/A'

        except Exception as e:
            print("Error:", e)
            return 'N/A'
    
    # def parse_vga(self, response):
    #     """
    #     Extracts the VGA (not onboard) details from the response and combines them.
    #     """
    #     try:
    #         vga_texts = response.css('span:contains("Tên đầy đủ (Card rời)") + span::text').getall()
    #         for vga_text in vga_texts: 
    #             if vga_text: 
    #                 return vga_text.strip().lower()
            
    #         return 'N/A'
    #     except Exception as e:
    #         print("Error:", e)
    #         return 'N/A'
    def parse_height(self, response):
        return super().parse_height(response)
    def parse_width(self, response):
        return super().parse_width(response)
    def parse_depth(self, response):
        return super().parse_depth(response)