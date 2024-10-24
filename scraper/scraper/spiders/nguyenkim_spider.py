<<<<<<< HEAD
import scrapy
from scrapy.http import Response, Request
import re
from .base_laptopshop_spider import BaseLaptopshopPageSpider

from selenium import webdriver
=======
from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider
>>>>>>> 4e4f7ffa70db8b55477483bb6a4bdc1733a41bcd

# create scraper
class NguyenkimScraper(BaseLaptopshopPageSpider):
    name = "nguyenkim_spider"
    start_urls = ['https://www.nguyenkim.com/laptop-may-tinh-xach-tay/']
    product_site_css = "h2.product-title a::attr(href)"
    page_css = "a.page.cm-history.ty-pagination__item::attr(href)"
    show_technical_spec_button_xpath = '//*[@id="productSpecification_viewFull"]'
    source = "nguyenkim"
    selenium_page_request = True
    selenium_product_request = True
    
    
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//tr/td[contains(., '{}')]/following-sibling::td/text()".format(name)
                for name in names
            ]
        for value in possibile_values:
            scope = response.xpath(value).getall()
            if scope:
                return '\n'.join(scope)
            
        return None
    
    def parse_brand(self, response: Response):
        try:
            # Adjusting the selector to match the product title inside <h2> tag
            res = response.css('h2.product-title a::text').get()
            
            if "Macbook" in res or "MacBook" in res:
                return "Apple"
            
            # Remove unnecessary terms
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            
            # Split the remaining text to extract the brand
            return res.split()[0]
        except:
            return "N/A"
