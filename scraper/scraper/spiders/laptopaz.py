from .base_laptopshop_spider import BaseLaptopshopPageSpider
from scrapy.http import Response
import re

class LaptopazSpider(BaseLaptopshopPageSpider):
    name = 'laptopaz'
    allowed_domains = ["laptopaz.vn"]
    start_urls = ['https://laptopaz.vn/laptop-moi.html']

    product_site_css = "div.p-entry a.p-name::attr(href)"
    #next_page_css = "a.page-link::attr(href)"

    # [PARSE FEATURES SECTION: START]
    # Name
    def parse_name(self, response):
        """
        Extracts the name of the laptop from the response.
        """
        try:
            full_text = response.css("h1.bg-white.border-bottom.mb-0.p-3.text-18.title.w-100.bk-product-name::text").get()
            #return re.sub(r"\[.*?\]|\(.*?\)|\b\d{4}\b", "", full_text).strip()
            return full_text.strip()
        except Exception:
            return "N/A"
    
     # CPU
    def parse_cpu(self, response: Response):
        """
        Extracts the CPU name of the laptop from the response.
        """
    