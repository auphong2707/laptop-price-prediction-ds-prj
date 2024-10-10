from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopLoadmoreButtonSpider
import html

class HacomSpider(BaseLaptopshopLoadmoreButtonSpider):

    name = "hacom"
    allowed_domains = ["hacom.vn"]
    start_urls = [
        "https://hacom.vn/laptop"
    ]
    product_site_css = ".p-name a::attr(href)"
    loadmore_button_css = ".btn-view-more"

    def parse_brand(self, response: Response):
        try:
            brand = response.css('div.pd-info-right h1.sptitle2024::text').get().split()
            if brand[0] == "Laptop":
                return brand[1]
            else:
                return brand[0]
        except:
            return "N/A"
    
    def parse_name(self, response: Response):
        try:
            name = response.css('div.pd-info-right h1.sptitle2024::text').get().split('(')[0]
            if 'Laptop' in name:
                return name.split('Laptop ')[1]
            else:
                return name.split('Laptop ')[0]
        except:
            return "N/A"
    
    def parse_cpu(self, response: Response):
        try:
            cpus = response.css('div.pd-summary-group div div.item::text').getall()
            for cpu in cpus:
                if "CPU" in cpu:
                    return cpu.split('CPU')[1].split('(')[0].split('\r')[0].strip(' :')
                elif "xử lý" in cpu:
                    return cpu.split('xử lý')[1].split('(')[0].split('\r')[0].strip(' :')
        except:
            return "N/A"
    
    def parse_vga(self, response: Response):
        try:
            vgas = response.css('div.pd-summary-group div div.item::text').getall()
            for vga in vgas:
                if "VGA" in vga:
                    return vga.split('VGA')[-1].split('(')[0].split('\r')[0].strip(' :()')
                elif "đồ họa" in vga:
                    return vga.split('đồ họa')[-1].split('(')[0].split('\r')[0].strip(' :()')
        except:
            return "N/A"
        
    def parse_ram_amount(self, response: Response):
        try:
            rams = response.css('div.pd-summary-group div div.item::text').getall()
            for ram in rams:
                if "RAM" in ram:
                    if "onboard" in ram:
                        tmp = ram.split('onboard')[0].split('Onboard')[0].strip(' :()').split()
                        tp = ''
                        for tm in tmp:
                            if "GB" in tm:
                                if tp.isnumeric():
                                    return tp+tm
                                return tm
                            tp = tm
                    else:
                        tmp = ram.split()
                        tp = ''
                        for tm in tmp:
                            if "GB" in tm:
                                if tp.isnumeric():
                                    return tp+tm
                                return tm
                            tp = tm
        except:
            return "N/A"