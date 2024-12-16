import time
import re
from scrapy.http import Response
from selenium.webdriver.common.by import By

from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider

class FPTShopScraper(BaseLaptopshopLoadmoreButtonSpider):
    name = "fptshop_spider"
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']
    product_site_css = "h3.ProductCard_cardTitle__HlwIo a::attr(href)"
    allowed_domains = ['fptshop.com.vn']
    loadmore_button_css = ".Button_root__LQsbl.Button_btnSmall__aXxTy.Button_whitePrimary__nkoMI.Button_btnIconRight__4VSUO.border.border-iconDividerOnWhite.px-4.py-2"
    # close_button_xpaths = ["//button[@class='close']"]
    
    show_technical_spec_button_xpath = "//button[span[text()='Tất cả thông số']]"
    source = 'fptshop'
    selenium_product_request = True
    
    def _get_driver_options(self):
        options = super()._get_driver_options()
        options.set_preference('permissions.default.image', 1)
        return options

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
                self.driver.execute_script("document.body.style.zoom='40%'")
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
                    num_retries = 500
                    while not self.driver.find_elements(By.CLASS_NAME, 'Swipeable_swipeable__BTB2L') and num_retries > 0:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(1)
                        
                        num_retries -= 1
                    
                    if num_retries == 0:
                        print("Failed to open the modal.")
                        continue

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
        
        html = self.driver.page_source

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return html

    def get_scoped_value(self, response, names):
        possibile_values = [
            "//div[span[contains(text(), '{}')]]/following-sibling::span/text()".format(name)
            for name in names
        ] + [
            "//div[div/span[contains(text(), '{}')]]//div/p/text()".format(name)
            for name in names
        ] + [
            "//div[contains(@id, 'spec-item')]//div[span[contains(text(), '{}')]]/following-sibling::span/text()".format(name)
            for name in names
        ]
    
        for value in possibile_values:
            scope = response.xpath(value).getall()

            if len(scope) > 0:
                return '\n'.join(scope)
                
        print(f"Value {names} not found")
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
                return 'n/a'
        except Exception as e:
            print("Error", e)
            return 'n/a'
        
    def parse_name(self, response: Response): 
        """
        Extracts the name of the laptop from the response.
        """
        # Get the initial part of the name
        title = response.css('h1.text-textOnWhitePrimary::text').get()
        return title if title else 'n/a'
    
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU details from the response and combines them.
        """
        cpu_brand = self.get_scoped_value(response, ['Hãng CPU']).lower()
        cpu_technology = self.get_scoped_value(response, ['Công nghệ CPU']).lower()
        cpu_type = self.get_scoped_value(response, ['Loại CPU']).lower()

        cpu_parts = [part for part in [cpu_brand, cpu_technology, cpu_type] if part and "đang cập nhật" not in part]
        return " ".join(cpu_parts) if cpu_parts else 'n/a'
    
    def parse_vga(self, response):
        """
        Extracts the VGA (not onboard) details from the response and combines them.
        """
        vga_text = self.get_scoped_value(response, ['Tên đầy đủ (Card rời)'])
        return vga_text if vga_text else 'n/a'

    def parse_ram_amount(self, response):
        """
        Extract the RAM amount from the response
        """
        ram_text = self.get_scoped_value(response, ['Dung lượng RAM'])
        return ram_text if ram_text else 'n/a'
    
    def parse_ram_type(self, response):
        """
        Extract the RAM type from the response
        """
        ram_text = self.get_scoped_value(response, ['Loại RAM'])
        return ram_text if ram_text else 'n/a'
    
    def parse_storage_amount(self, response):
        """
        Extract the storage amount from the response
        """
        storage_text = self.get_scoped_value(response, ['Dung lượng'])
        return storage_text if storage_text else 'n/a'

    def parse_storage_type(self, response):
        """
        Extract the storage type from the response
        """
        storage_text = self.get_scoped_value(response, ['Lưu trữ'])
        return storage_text if storage_text else 'n/a'

    def parse_size(self, response):
        """
        Extract the screen size from the response
        """
        size_text = self.get_scoped_value(response, ['Kích thước'])
        return size_text if size_text else 'n/a'

    def parse_weight(self, response):
        """
        Extract the weight from the response
        """
        weight_text = self.get_scoped_value(response, ['Trọng lượng sản phẩm'])
        return weight_text if weight_text else 'n/a'

    def parse_battery_capacity(self, response):
        """
        Extracts the battery capacity in Whr from the response.
        """
        battery_text = self.get_scoped_value(response, ['Dung lượng pin'])
        return battery_text if battery_text else 'n/a'
    
    def parse_battery_cells(self, response):
        """
        Extracts the number of battery cells from the response.
        """
        battery_text = self.get_scoped_value(response, ['Dung lượng pin'])
        return battery_text if battery_text else 'n/a'

    def parse_screen_size(self, response):
        """
        Extracts the screen size in inches from the response.
        """
        screen_text = self.get_scoped_value(response, ['Kích thước màn hình'])
        return screen_text if screen_text else 'n/a'
    
    def parse_screen_resolution(self, response):
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        screen_text = self.get_scoped_value(response, ['Độ phân giải'])
        return screen_text if screen_text else 'n/a'
    
    def parse_screen_refresh_rate(self, response):
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        screen_text = self.get_scoped_value(response, ['Tần số quét'])
        return screen_text if screen_text else 'n/a'
    
    def parse_screen_brightness(self, response):
        """
        Extracts the screen brightness in nits from the response.
        """
        screen_text = self.get_scoped_value(response, ['Độ sáng'])
        return screen_text if screen_text else 'n/a'
    
    def parse_webcam_resolution(self, response):
        """
        Extracts the webcam resolution from the response.
        """
        webcam_text = self.get_scoped_value(response, ['Webcam'])
        return webcam_text if webcam_text else 'n/a'
    
    def parse_connectivity(self, response):
        """
        Extracts the connectivity options from the response.
        """
        connectivity_text = self.get_scoped_value(response, ['Cổng giao tiếp'])
        if connectivity_text:
            # Step 1: Add '1 x ' for standalone "USB" without a number before it
            connectivity_text = re.sub(r'\b(?<!\d\s)(usb)', r'1 x \1', connectivity_text, flags=re.IGNORECASE)

            # Step 2: Format cases where a number exists before "USB"
            connectivity_text = re.sub(r'(\d+)\s*(usb)', r'\1 x \2', connectivity_text, flags=re.IGNORECASE)
            
        return connectivity_text if connectivity_text else 'n/a'
    
    def parse_default_os(self, response):
        """
        Extracts the operating system from the response.
        """
        os_text = self.get_scoped_value(response, ['Version', 'OS'])
        return os_text if os_text else 'n/a'
    
    def parse_price(self, response):
        """
        Extracts the price of the laptop from the response.
        """
        price_text = response.xpath("//div[@id='tradePrice']//span[@class='text-black-opacity-100 h4-bold']//text()").getall()
        price_text = ' '.join(price_text)
        return price_text if price_text else 'n/a'

    def parse_warranty(self, response):
        """
        Extracts the warranty period in months from the response.
        """
        warranty_text = self.get_scoped_value(response, ['Thời gian bảo hành'])
        return warranty_text + ' tháng' if warranty_text else 'n/a'
