# run following command to store results of scraping in temp_results.json
# scrapy crawl main -o temp_results.json
# -*- coding: utf-8 -*-
import scrapy
from ..items import VdbCatalogItem

class CourseCatalogSpider(scrapy.Spider):
    name = 'vdb-scraper'
    allowed_domains = ['uni-due.de']
    start_urls = [
        'https://www.uni-due.de/vdb/studiengang/liste'
    ]

    def __init__(self, keywords=["angewandte informatik", "angewandte kognitions- und medienwissenschaft", "computer engineering"]):
        self.keywords = keywords

    def parse(self, response):
        return self.get_links(response)

    def get_links(self, response):
        links = response.xpath("//div[@class='highlight-blue']/ul/li/a")
        print("PAAAY ATTENTION")
        for link in links:
            yield {
                "link": link.get(),
                "string": link.xpath("/text()")
            }
