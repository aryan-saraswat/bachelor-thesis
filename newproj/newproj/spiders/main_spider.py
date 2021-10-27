import scrapy

class MainSpider(scrapy.Spider):
    name = "bruh"
    start_urls = [
        'https://campus.uni-due.de/lsf/rds?state=wtree&search=1&trex=step&root120212=288350%7C292081%7C290850&P.vx=kurz'
    ]

    def parse(self, response):
        page = response.url
        filename = 'urlResponse.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('saved file', filename)