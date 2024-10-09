from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider

class GearvnSpider(BaseLaptopshopLoadmoreButtonSpider):
    name = "gearvn"
    allowed_domains = ["gearvn.com"]
    start_urls = [
        'https://gearvn.com/collections/laptop',
    ]
    
    product_site_css = 'h3.proloop-name a::attr(href)'
    loadmore_button_css = 'button#load_more'
    
    
    def parse_brand(self, response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        return "N/A"
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            res = response.css('.product-name h1::text').get()
            for front_removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(front_removal, '')
            
            if "Macbook" in res:
                res = "Apple " + ' '.join(res.split()[:2] + res.split()[-1:])
            
            return res
        except:
            return "N/A"
    
    # CPU
    def parse_cpu(self, response):
        """
        Extracts the CPU name of the laptop from the response.
        """
        return "N/A"
    
    # VGA
    def parse_vga(self, response):
        """
        Extracts the VGA name of the laptop from the response.
        """
        return "N/A"
    
    # RAM
    def parse_ram_amount(self, response): 
        """
        Extracts the amount of RAM in GB from the response.
        """
        return "N/A"
    
    def parse_ram_type(self, response): 
        """
        Extracts the type of RAM from the response.
        Example: DDR3, DDR4, etc.
        """
        return "N/A"
    
    # Storage
    def parse_storage_amount(self, response): 
        """
        Extracts the amount of storage in GB from the response.
        """
        return "N/A"
    
    def parse_storage_type(self, response): 
        """
        Extracts the type of storage from the response.
        Example: HDD, SSD, SSHD.
        """
        return "N/A"
    
    # Webcam
    def parse_webcam_resolution(self, response): 
        """
        Extracts the webcam resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"
    
    # Screen
    def parse_screen_size(self, response): 
        """
        Extracts the screen size in inches from the response.
        """
        return "N/A"
    
    def parse_screen_resolution(self, response): 
        """
        Extracts the screen resolution from the response.
        Example: HD, FHD, 4K.
        """
        return "N/A"
    
    def parse_screen_ratio(self, response): 
        """
        Extracts the screen ratio from the response.
        Example: 16:9, 16:10, 4:3.
        """
        return "N/A"
    
    def parse_screen_refresh_rate(self, response): 
        """
        Extracts the screen refresh rate in Hz from the response.
        """
        return "N/A"
    
    def parse_screen_color_gamut(self, response): 
        """
        Extracts the screen color gamut in sRGB from the response.
        """
        return "N/A"
    
    def parse_screen_brightness(self, response): 
        """
        Extracts the screen brightness in nits from the response.
        """
        return "N/A"
    
    # Battery
    def parse_battery_capacity(self, response): 
        """
        Extracts the battery capacity in Wh from the response.
        """
        return "N/A"
    
    # Size
    def parse_length(self, response):
        """
        Extracts the length of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_width(self, response):
        """
        Extracts the width of the laptop in cm from the response.
        """
        return "N/A"
    
    def parse_height(self, response):
        """
        Extracts the height of the laptop in cm from the response.
        """
        return "N/A"
    
    # Weight
    def parse_weight(self, response): 
        """
        Extracts the weight of the laptop in kg from the response.
        """
        return "N/A"
    
    # Connectivity
    def parse_number_usb_a_ports(self, response):
        """
        Extracts the number of USB-A ports from the response.
        """
        return "N/A"
    
    def parse_number_usb_c_ports(self, response):
        """
        Extracts the number of USB-C ports from the response.
        """
        return "N/A"
    
    def parse_number_hdmi_ports(self, response):
        """
        Extracts the number of HDMI ports from the response.
        """
        return "N/A"
    
    def parse_number_ethernet_ports(self, response):
        """
        Extracts the number of Ethernet ports from the response.
        """
        return "N/A"
    
    def parse_number_audio_jacks(self, response):
        """
        Extracts the number of audio jacks from the response.
        """
        return "N/A"
    
    # Operating System
    def parse_default_os(self, response): 
        """
        Extracts the default operating system of the laptop from the response.
        Example: Windows, Linux, etc.
        """
        return "N/A"
    
    # Color
    def parse_color(self, response): 
        """
        Extracts the color of the laptop from the response.
        Example: Black, White, etc.
        """
        return "N/A"
    
    # Origin
    def parse_origin(self, response): 
        """
        Extracts the origin of the laptop from the response.
        Example: China, Taiwan, USA, etc.
        """
        return "N/A"
    
    # Warranty
    def parse_warranty(self, response): 
        """
        Extracts the warranty period in months from the response.
        """
        return "N/A"
    
    # Release Date
    def parse_release_date(self, response): 
        """
        Extracts the release date of the laptop from the response.
        Format: dd/mm/yyyy.
        """
        return "N/A"
    
    # Price
    def parse_price(self, response): 
        """
        Extracts the price of the laptop from the response.
        Example: in VND.
        """
        return "N/A"