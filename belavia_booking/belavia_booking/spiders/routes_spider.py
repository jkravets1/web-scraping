# -*- coding: utf-8 -*-
import scrapy
import json

class RoutesSpiderSpider(scrapy.Spider):
    name = 'routes_spider'
    allowed_domains = ['en.belavia.by']
    start_urls = ['https://ibe.belavia.by/api/settings?lang=en']

    def parse(self, response):
        jsonD = json.loads(response.body)
        all_routes = []
        for route in jsonD['routes']:
        	for destination in route['destinations']:
        		all_routes.append({'src':route['origin'], 'dst':destination, 'direct':None})

        print(all_routes)