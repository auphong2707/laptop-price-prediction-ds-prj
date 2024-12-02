from scrapy.http import Response
from .base_laptopshop_spider import BaseLaptopshopPageSpider

# create scraper
class NguyenkimScraper(BaseLaptopshopPageSpider):
    name = "nguyenkim_spider"
    start_urls = ['https://www.nguyenkim.com/laptop-may-tinh-xach-tay/']
    product_site_css = "a.product-render::attr(href)"
    page_css = "a.btn_next.ty-pagination__item.ty-pagination__btn.ty-pagination__next::attr(href)"
    show_technical_spec_button_xpath = '//*[@id="productSpecification_viewFull"]'
    source = "nguyenkim"
    selenium_page_request = True
    selenium_product_request = True
    
    def yield_condition(self, response):
        res = response.css('h1.product_info_name::text').get()
        if "(Hàng xả kho)" in res or "Hàng xả kho" in res:
            return False
        return True
    
    def get_scoped_value(self, response, names):
        possibile_values = [
                "//tr/td[contains(., '{}')]/following-sibling::td/text()".format(name)
                for name in names
            ] + [
                "//tr/td[contains(., '{}')]/following-sibling::td//a/text()".format(name)
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
            res = response.css('h1.product_info_name::text').get()
            
            if "Macbook" in res or "MacBook" in res:
                return "Apple"
            
            # Remove unnecessary terms
            for removal in ['Laptop gaming ', 'Laptop Gaming ', 'Laptop ']:
                res = res.replace(removal, '')
            # Split the remaining text to extract the brand
            return res.split()[0] if res else "n/a"
        except:
            return "n/a"
        
    def parse_name(self, response: Response):
        res = response.css('h1.product_info_name::text').get()
        return res if res else "n/a"
        
    def parse_price(self, response: Response):
        res = response.css('span.nk-price-final::text').get()
        return res if res else "n/a"
        
    def parse_cpu(self, response: Response):
        res1 = self.get_scoped_value(response, ["CPU:"])
        res2 = self.get_scoped_value(response, ["Loại CPU:"])
        if res1: 
            if res2: 
                res = res1 + res2
            else: 
                res = res1
        return res if res else "n/a"
    
    def parse_vga(self, response: Response):
        res = self.get_scoped_value(response, ["Bộ xử lý đồ họa:"]) 
        return res if res else "n/a"
    
    def parse_ram_amount(self, response):
        res = self.get_scoped_value(response, ["Dung lượng RAM:"])
        return res if res else "n/a"
    
    def parse_ram_type(self, response):
        res = self.get_scoped_value(response, ["Loại RAM:"])
        return res if res else "n/a"
    
    def parse_storage_amount(self, response):
        res = self.get_scoped_value(response, ["Dung lượng ổ cứng:"])
        return res if res else "n/a"
    
    def parse_storage_type(self, response):
        res = self.get_scoped_value(response, ["Loại ổ đĩa cứng:"])
        return res if res else "n/a"
    
    def parse_default_os(self, response):
        res = self.get_scoped_value(response, ["HĐH kèm theo máy:"])
        return res if res else "n/a"
    
    def parse_size(self, response):
        res = self.get_scoped_value(response, ["Kích thước sản phẩm:"])
        return res if res else "n/a"
    
    def parse_weight(self, response):
        res = self.get_scoped_value(response, ["Khối lượng sản phẩm (kg):", "Khối lượng sản phẩm:", "Khối lượng sản phẩm (g):"])
        return res if res else "n/a"
    
    def parse_battery_capacity(self, response):
        res = self.get_scoped_value(response, ["Loại Pin Laptop :"])
        return res if res else "n/a"
    
    def parse_battery_cells(self, response):
        res = self.get_scoped_value(response, ["Loại Pin Laptop :"])
        return res if res else "n/a"
    
    def parse_screen_size(self, response):
        res = self.get_scoped_value(response, ["Kích thước màn hình:"])
        return res if res else "n/a"
    
    def parse_screen_resolution(self, response):
        res = self.get_scoped_value(response, ["Độ phân giải màn hình:"])
        return res if res else "n/a"
    
    def parse_connectivity(self, response):
        res = self.get_scoped_value(response, ["Cổng USB:"]) + self.get_scoped_value(response, ["Cổng HDMI:"])
        return res if res else "n/a"
    
    def parse_default_os(self, response):
        res = self.get_scoped_value(response, ["HĐH kèm theo máy:"])
        return res if res else "n/a"
    
    def parse_webcam_resolution(self, response):
        res = self.get_scoped_value(response, ["Camera:"])
        return res if res else "n/a"
    
    def parse_color(self, response):
        res = self.get_scoped_value(response, ["Màu sắc:"])
        return res if res else "n/a"
    
    def parse_warranty(self, response):
        res = self.get_scoped_value(response, ["Thời gian bảo hành:"])
        return res if res else "n/a"
    
    def parse_screen_refresh_rate(self, response):
        res = self.get_scoped_value(response, ['Tần số quét màn hình:'])
        return res if res else 'n/a'
