import scrapy
from scrapy.http import Response, Request
import re
import logging 
from .base_laptopshop_spider import BaseLaptopshopPageSpider
from scrapy_selenium import SeleniumRequest

# create scraper
class NguyenkimScraper(BaseLaptopshopPageSpider):
    name = "nguyenkim_spider"
    start_urls = ['https://www.nguyenkim.com/laptop-may-tinh-xach-tay']
    allowed_domains = ['nguyenkim.com']
    product_site_css = "h2.product-title a::attr(href)"
    page_css = "a.page.cm-history.ty-pagination__item::attr(href)"
    show_technical_spec_button_xpath = '//*[@id="productSpecification_viewFull"]'
    source = "nguyenkim"
    
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
