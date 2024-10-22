import scrapy
from scrapy.http import Response
import re

class Test1Spider(scrapy.Spider):
    name = "test1"
    allowed_domains = ["phongvu.vn"]
    start_urls = [
        'https://phongvu.vn/may-tinh-xach-tay-macbook-air-13-6-m2-8-core-cpu-10-core-gpu-16gb-256gb-ssd-30w-silver-z15w005j9--s240706417',
        'https://phongvu.vn/laptop-hp-envy-x360-14-fc0090tu-a19c0pa-ultra-7-155u-bac--s240602671',
        'https://phongvu.vn/laptop-msi-pulse-16-ai-c1vgkg-061vn-ultra-9-185h-den--s240601551',
        'https://phongvu.vn/laptop-acer-nitro-v-16-propanel-anv16-41-r36y--s240802643',
        'https://phongvu.vn/may-tinh-xach-tay-laptop-gigabyte-g5-mf-f2vn333sh-i5-12450h-den--s230604051'
    ]

    def get_scoped_value(self, response, names):
        possibile_values = [
            "div.css-1i3ajxp > div[type='body'].css-1lchwqw".format(name)
            for name in names
        ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return "".join(scope).strip()
        return None

    
    # [PARSE FEATURES SECTION: START]
    
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            full_text = response.css('h1.css-nlaxuc::text').get()
            return re.sub(r'\s*\(.*?\)', '', full_text).strip()
        except Exception:
            return "N/A"
    
    # Brand
    def parse_brand(self, response: Response): 
        """
        Extracts the brand of the laptop from the response.
        Example: Dell, HP, etc.
        """
        try:
            return self.get_scoped_value(response, ['Thương hiệu:'])
        except Exception:
            return "N/A"
        
        # RAM
    def parse_ram_amount(self, response: Response):
        """
        Extracts the amount of RAM in GB from the response.
        """
        return response.xpath("//div[text()='Ram']/following-sibling::div/text()").get()
        
    def parse(self, response: Response):
        yield {
            'brand': self.parse_brand(response),
            'name': self.parse_name(response),
            'ram_amount': self.parse_ram_amount(response)
        }

