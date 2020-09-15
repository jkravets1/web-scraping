# -*- coding: utf-8 -*-
import scrapy
import json

class AirportsSpiderSpider(scrapy.Spider):
    name = 'airports_spider'
    allowed_domains = ['en.belavia.by']
    start_urls = ['https://en.belavia.by/api/hotel_cities/en']

    def parse(self, response):
        all_airports = []
        json_airports = json.loads(response.body)
        for val in json_airports:
            all_airports.append(val['Id'])

        print(all_airports)