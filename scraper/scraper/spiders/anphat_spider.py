from scrapy.http import Response

from .base_laptopshop_spider import BaseLaptopshopNextPageSpider

class AnphatSpider(BaseLaptopshopNextPageSpider):
    name = "anphat"
    allowed_domains = ["anphatpc.com.vn"]
    start_urls = [
        "https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html",
    ]
    product_site_css = 'a.p-img::attr(href)'

    def get_next_page(self, response: Response):
        return response.css('a:has(i.fa.fa-angle-right)::attr(href)').get()

    def parse_brand(self, response: Response):
        laptop_info = response.css('section.product-detail-page div.popup-spec\
                                    table tbody tr:nth-child(0) td:nth-child(1) p span a')

        #return "N/A"
        return laptop_info.css('a::text').get()