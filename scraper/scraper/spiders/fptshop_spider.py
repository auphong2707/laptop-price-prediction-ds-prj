import scrapy
from scrapy.http import Response

from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
class FPTShopScraper(BaseLaptopshopLoadmoreButtonSpider):
    name = "fptshop_spider"
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']
    product_site_css = "h3.ProductCard_cardTitle__HlwIo a::attr(href)"
    allowed_domains = ['fptshop.com.vn']
    loadmore_button_css = ".Button_root__LQsbl.Button_btnSmall__aXxTy.Button_whitePrimary__nkoMI.Button_btnIconRight__4VSUO.border.border-iconDividerOnWhite.px-4.py-2"
    # close_button_xpaths = ["//button[@class='close']"]
    
    show_technical_spec_button_xpath = "//button[span[text()='Tất cả thông số']]"
    source = 'fpt'
    selenium_product_request = True


    def get_scoped_value(self, response, names):
        possibile_values = [
            "//div[span[contains(text(), '{}')]]/following-sibling::span/text()".format(name)
            for name in names
        ] + [
            "//div[div/span[contains(text(), '{}')]]//div/p/text()".format(name)
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
        try:
            # Get the initial part of the name
            title = response.css('h1.text-textOnWhitePrimary::text').get()
            if not title:
                return 'n/a'

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
            cpu_brand = self.get_scoped_value(response, ['Hãng CPU'])
            cpu_technology = self.get_scoped_value(response, ['Công nghệ CPU'])
            cpu_type = self.get_scoped_value(response, ['Loại CPU'])
            # # Extract individual CPU features using CSS selectors
            # cpu_brand = response.css('#spec-item-0 > div:nth-child(2) > span:nth-child(2)::text').get()
            # cpu_technology = response.css('#spec-item-0 > div:nth-child(3) > span:nth-child(2)::text').get()
            # cpu_type = response.css('#spec-item-0 > div:nth-child(4) > span:nth-child(2)::text').get()

            # if cpu_brand and cpu_technology and cpu_type:
            #     # Combine the features into a single string
            #     cpu_details = f"{cpu_brand} {cpu_technology} {cpu_type}"
            #     return cpu_details.strip()
            # else: 
            #     return 'N/A'
            return f"{cpu_brand} {cpu_technology} {cpu_type}" if cpu_brand or cpu_technology or cpu_type else 'n/a'

        except Exception as e:
            print("Error:", e)
            return 'n/a'
    
    def parse_vga(self, response):
        """
        Extracts the VGA (not onboard) details from the response and combines them.
        """
        try:
            vga_text = self.get_scoped_value(response, ['Tên đầy đủ (Card rời)'])
            return vga_text if vga_text else 'n/a'
            # if vga_text: 
            #     vga_text = vga_text.strip().split('\n')
            #     for i in range(len(vga_text)): 
            #         if vga_text[i].lower() == "tên đầy đủ (card rời)": 
            #             return vga_text[i+1]
        except Exception as e:
            print("Error:", e)
            return 'n/a'
        
    def parse_ram_amount(self, response):
        """
        Extract the RAM amount from the response
        """
        try: 
            ram_text = self.get_scoped_value(response, ['Dung lượng RAM'])
            return ram_text if ram_text else 'n/a'
            # if ram_text: 
            #     # extract the number and GB
            #     ram_text = ram_text.split('\n')
            #     for i in range(len(ram_text)):
            #         if 'Dung lượng' in ram_text[i]: 
            #             ram = ram_text[i+1]Price
            #             if 'thanh' in ram: 
            #                 ram = ram.split('(')[0]
            #             return ram.strip()
            # return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_ram_type(self, response):
        """
        Extract the RAM type from the response
        """
        try: 
            ram_text = self.get_scoped_value(response, ['Loại RAM'])
            return ram_text if ram_text else 'n/a'
            # if ram_text: 
            #     # extract the number and GB
            #     ram_text = ram_text.split('\n')
            #     for i in range(len(ram_text)):
            #         if 'Loại' in ram_text[i]: 
            #             ram = ram_text[i+1]
            #             return ram.strip()
            # return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_storage_amount(self, response):
        """
        Extract the storage amount from the response
        """
        try: 
            storage_text = self.get_scoped_value(response, ['Dung lượng'])
            return storage_text if storage_text else 'n/a'
            # if storage_text: 
            #     # extract the number and GB
            #     storage_text = storage_text.split('\n')
            #     for i in range(len(storage_text)):
            #         if 'Dung lượng' in storage_text[i]: 
            #             storage = storage_text[i+1]
            #             if 'GB' not in storage: 
            #                 storage = storage + "GB"
            #             return storage.strip()
            # return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    def parse_storage_type(self, response):
        """
        Extract the storage type from the response
        """
        try: 
            storage_text = self.get_scoped_value(response, ['Lưu trữ'])
            return storage_text if storage_text else 'n/a'
            # if storage_text: 
            #     # extract the number and GB
            #     storage_text = storage_text.split('\n')
            #     for i in range(len(storage_text)):
            #         if 'Kiểu ổ cứng' in storage_text[i]: 
            #             storage = storage_text[i+1]
            #             return storage.strip()
            # return 'N/A'
        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    def parse_size(self, response):
        """
        Extract the screen size from the response
        """
        try: 
            size_text = self.get_scoped_value(response, ['Kích thước'])
            return size_text if size_text else 'n/a'

        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_weight(self, response):
        """
        Extract the weight from the response
        """
        try: 
            weight_text = self.get_scoped_value(response, ['Trọng lượng sản phẩm'])
            return weight_text if weight_text else 'n/a'

        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_battery_capacity(self, response):
        """
        Extracts the battery capacity in Whr from the response.
        """
        try: 
            battery_text = self.get_scoped_value(response, ['Dung lượng pin'])
            return battery_text if battery_text else 'n/a'

        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_battery_cells(self, response):
        """
        Extracts the number of battery cells from the response.
        """
        try: 
            battery_text = self.get_scoped_value(response, ['Dung lượng pin'])
            return battery_text if battery_text else 'n/a'

        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_screen_size(self, response):
        """
        Extracts the screen size in inches from the response.
        """
        try: 
            screen_text = self.get_scoped_value(response, ['Kích thước màn hình'])
            return screen_text if screen_text else 'n/a'
        except Exception as e: 
            print("Error: ", e) 
            return 'n/a'
    
    def parse_screen_resolution(self, response):
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        try: 
            screen_text = self.get_scoped_value(response, ['Độ phân giải'])
            return screen_text if screen_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    def parse_screen_refresh_rate(self, response):
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        try: 
            screen_text = self.get_scoped_value(response, ['Tần số quét'])
            return screen_text if screen_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    def parse_screen_brightness(self, response):
        """
        Extracts the screen brightness in nits from the response.
        """
        try: 
            screen_text = self.get_scoped_value(response, ['Độ sáng'])
            return screen_text if screen_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    def parse_webcam_resolution(self, response):
        """
        Extracts the webcam resolution from the response.
        """
        try: 
            webcam_text = self.get_scoped_value(response, ['Webcam'])
            return webcam_text if webcam_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    def parse_connectivity(self, response):
        """
        Extracts the connectivity options from the response.
        """
        try: 
            connectivity_text = self.get_scoped_value(response, ['Cổng giao tiếp'])
            return connectivity_text if connectivity_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    
    def parse_default_os(self, response):
        """
        Extracts the operating system from the response.
        """
        try: 
            os_text = self.get_scoped_value(response, ['Version', 'OS'])
            return os_text if os_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    
    def parse_price(self, response):
        """
        Extracts the price of the laptop from the response.
        """
        try: 
            price_text = response.css('span.text-neutral-gray-5 line-through::text').get()
            return price_text if price_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'
    
    def parse_warranty(self, response):
        """
        Extracts the warranty period in months from the response.
        """
        try: 
            warranty_text = self.get_scoped_value(response, ['Thời gian bảo hành'])
            return warranty_text if warranty_text else 'n/a'
        except Exception as e:
            print("Error: ", e)
            return 'n/a'