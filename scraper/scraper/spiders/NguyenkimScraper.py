import scrapy
from scrapy.http import Response, Request
import logging
from scrapy_selenium import SeleniumRequest  # Ensure this is installed: pip install scrapy-selenium

class NguyenkimScraper(scrapy.Spider):
    name = "nguyenkim_spider"
    start_urls = ['https://www.nguyenkim.com/laptop-may-tinh-xach-tay']
    product_site_css = "h2.product-title a::attr(href)"
    # page_css = "a.ty-pagination__item::attr(href)"

    def start_requests(self):
        # Initial request with redirect handling
        yield Request(
            url=self.start_urls[0], 
            callback=self.parse,
            meta={'handle_httpstatus_list': [302]}
        )

    def parse(self, response: Response):
        # Handle redirect.  Don't call parse recursively. Let Scrapy handle redirects.
        if response.status in (301, 302, 307):
            logging.info(f"Redirect detected.  Scrapy will handle it: {response.url}")
            return  # Important: Stop processing here. Scrapy will follow the redirect.

        # Normal parsing (after redirect is handled)
        for product_url in response.css(self.product_site_css).getall():
            yield response.follow(product_url, callback=self.parse_one_observation)

        # Pagination
        for page in response.css(self.page_css).getall():
            yield response.follow(page, callback=self.parse)

    def parse_one_observation(self, response: Response):
        item = {}
        yield SeleniumRequest(
            url=response.url,
            callback=self.parse_product_selenium,
            wait_time=3,  # Adjust wait time as needed
            screenshot=True,
            meta={'item': item}
        )

    def parse_product_selenium(self, response: Response):
        item = response.meta['item']

        item['brand'] = self.parse_brand(response)
        item['name'] = self.parse_name(response)
        item['cpu'] = self.parse_cpu(response)
        item['price'] = self.parse_price(response)
        yield item


    def parse_brand(self, response: Response):
        try:
            title = response.css('h2.product-title a::text').get()
            if "Macbook" in title or "MacBook" in title:
                return "Apple"
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                title = title.replace(removal, '')
            return title.split()[0]
        except:
            return "N/A"

    def get_scoped_value(self, response, names):
        for name in names:
            # Try table rows first
            value = response.xpath(f"//tr/td[contains(., '{name}')]/following-sibling::td//span//text()").get()
            if value:
                return value
            # Try list items if not found in table rows
            value = response.xpath(f"//li/div[contains(., '{name}')]/following-sibling::div/text()").get()
            if value:
                return value
        return None