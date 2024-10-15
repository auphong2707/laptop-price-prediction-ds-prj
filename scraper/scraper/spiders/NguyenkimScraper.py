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
    product_site_css = "h2.product-title a::attr(href)"
    page_css = "a.ty-pagination__item::attr(href)"
    custom_settings = {
    'COOKIES_ENABLED': True,
    'COOKIES_DEBUG': True,
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.nguyenkim.com/',
    },
    'REDIRECT_ENABLED': False,
    'COOKIES': {
        # Insert the relevant cookie values here
        'cookie_name': 'cookie_value',
        '_ac_an_session': 'zmzqznzqzmzlzhzrzjzqznzjzrzmzmzrzdzizlznzizjzhzqzmzrznzdzizkzhzrzqznzqzrzhzmzdzizdzizkzhzrzqznzqzrzhzmzdzizkzhzrzqznzqzrzhzmzdzizdzhznzdzhzd2f27zdzgzdzlzmzmznzrzdzd321v272624',
        '_pk_id.554926188.973b': '0.1728949836.1.1728949837.1728949836.',
        '_tt_enable_cookie': '1',
        '_asm_uid': '1641029584',
        'cto_bundle': '_ZFPjF9xdjlVYmVxNkJWaHdhRW5xbDhheUhMejI4dEhCc25Rd3ZMaFhPTTFvek1HaGdJZUluWERVTnd1V1RRWURDQkx3R0FNV3JQVjRHbUZ6a3NaaDRFaTI5TWx6aXFpSVQlMkZzWnRWSFNHQWRzR3I2bm5LT21Zdm1wR2lTNEl6YXAlMkIzcG5UTzNBdFFDWVpYJTJGREVLJTJGSXg3YWVJNnFDTUZmanN5d2lwT0lLOEtBd2hHRSUzRA',
        '_utm_objs': '',
        '_clck': 'jqg493%7C2%7Cfq0%7C0%7C1748',
        '_fbp': 'fb.1.1728949836107.1100467294',
        '_asm_visitor_type': 'n',
        '_pk_ses.554926188.973b': '*',
        'installmentLocation_code': '001',
        '_atm_objs': 'eyJzb3VyY2UiOiIiLCJtZWRpdW0iOiIiLCJjYW1wYWlnbiI6IiIsImNvbnRlbnQiOiIiLCJ0ZXJt%0D%0AIjoiIiwidHlwZSI6IiIsImNoZWNrc3VtIjoiKiJ9',
        '_cdp_fsid': '5949562809408558',
        '_gid': 'GA1.2.127425857.1728949836',
        'au_id': '1641029584',
        '_ga': 'GA1.2.87613397.1728949835',
        '_gat_UA-17048930-1': '1',
        '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22A45x1jwEXKOJSGdiqcje%22%7D',
        'storeLocation_code': '001',
        '_asm_ss_view': '%7B%22time%22%3A1728949836060%2C%22sid%22%3A%225949562809408558%22%2C%22page_view_order%22%3A1%2C%22utime%22%3A%222024-10-14T23%3A50%3A36%22%2C%22duration%22%3A0%7D',
        '__nxquid': '6IFKev3DxiroKCgjiDqArPK5FUkQqg==0017',
        'nkcache_id': 'febc09d1cde97df1a49b166ca8e78f89',
        'installmentLocation_name': 'TP.HCM',
        '_ac_au_gt': '1728949824801',
        'nk_auth': 'unauth',
        'storeLocation_name': 'TP.HCM',
        'unauthHomeLocation_code': '001',
        'login_form_event': 'sign_in',
        '_ga_8S8EFGF74J': 'GS1.2.1728949836.1.0.1728949836.60.0.0',
        '__zi': '2000.SSZzejyD5ja-a_QhmHqUcJQLzgUEK0FNE8sq-vnQ7SLwdwBfamGKmJ_IfUwS31N3EfUXw9n87S0nbwhfC3Gs.1',
        'mp_skin': 'desktop',
        '_ac_client_id': '1641029584.1728949825',
        'sid_customer_5120c': '46a80eab065bed6197d62795df63b93f-C',
        'state_name': 'TP.HCM',
        '_cdp_cfg': '%257B%2522refferal_exclusion%2522%3A%255B%2522secureacceptance.cybersource.com%2522%2C%2522nguyenkim.com%2522%255D%257D',
        '_ga_H9PWBQFBY9': 'GS1.1.1728949835.1.0.1728949835.60.0.0',
        '_ttp': 'grHFx1lESVCcgk70Lm8fkEc_fYG',
        'state_code': '001',
        'login_form_event_time': '1728949055'
    }
}
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
