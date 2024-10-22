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
    page_css = "a.ty-pagination__item::attr(href)"
    COOKIES_ENABLED = True
    COOKIES_DEBUG = True

    def start_requests(self):
        # Use a regular Request, handle redirects manually
        yield Request(
            url='https://www.nguyenkim.com/laptop-may-tinh-xach-tay',
            callback=self.parse,
            meta={'handle_httpstatus_list': [302]}  # Key change: handle 302 redirects
        )

    def parse(self, response: Response):
        # Check for redirect as before
        if response.status in (301, 302, 307):
            logging.info(f"Following redirect to: {response.headers['Location']}")
            yield Request(response.urljoin(response.headers['Location'].decode()), callback=self.parse)  # Call parse again after redirect

        else:  # Proceed with normal parsing if not a redirect
            # Use the base class's get_product_sites method
            for site_request in self.get_product_sites(response):
                yield site_request

            # Pagination (using the base class's logic)
            for page in response.css(self.page_css).getall():
                yield response.follow(url=page, callback=self.parse)
    
    def parse_one_observation(self, response: Response):
        # Create an empty item dictionary
        item = {}

        # Initiate the SeleniumRequest, passing the item through meta
        yield SeleniumRequest(
            url=response.url,
            callback=self.parse_product_selenium,  # New callback function
            wait_time=3,
            screenshot=True,
            meta={'item': item}
        )
    
    def parse_product_selenium(self, response: Response):
        # Retrieve the item from meta
        item = response.meta['item']

        # Now perform all your parsing logic using Selenium
        item['brand'] = self.parse_brand(response)
        item['name'] = self.parse_name(response)
        item['cpu'] = self.parse_cpu(response)
        
        item['price'] = self.parse_price(response)

        # Yield the populated item
        yield item

    
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//tr/td[contains(., '{}')]/following-sibling::td//span//text()".format(name)
                for name in names
            ] + [
                "//li/div[contains(., '{}')]/following-sibling::div/text()".format(name)
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
