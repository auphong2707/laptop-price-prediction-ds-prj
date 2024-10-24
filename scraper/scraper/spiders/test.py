import os
import time
import scrapy
from scrapy.http import Response
import re
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent
from scrapy.http import Request

from .base_laptopshop_spider import BaseLaptopshopSpider

logging.disable()

class TestSpider(BaseLaptopshopSpider):
    name = 'testspider'
    start_urls = ['https://www.nguyenkim.com/laptop-may-tinh-xach-tay']
    allowed_domains = ['nguyenkim.com']
    product_site_css = "a.product-render::attr(href)"
    page_css = "a.page.cm-history.ty-pagination__item::attr(href)"
    show_technical_spec_button_xpath = '//*[@id="productSpecification_viewFull"]'
    close_button_xpaths = ["//button[@class='cancel-button-top']"]
    source = "nguyenkim"

    

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse
            )
            print(f"Request sent to: {url}")

    def parse(self, response):
        print("Test parse method called")
        filename = 'nguyenkim.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
    