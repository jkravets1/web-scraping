# -*- coding: utf-8 -*-
import scrapy
import json, requests
from scrapy.http import Request, FormRequest
from time import sleep

class CalendarSpiderSpider(scrapy.Spider):
    name = 'calendar_spider'
    allowed_domains = ['ibe.belavia.by']
    start_urls = ['http://ibe.belavia.by/']

    headers = {
        'Origin': 'https://ibe.belavia.by',
        'Accept-Language': 'en-US,en;q=0.9,sq;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
    }
    captcha_api_key = '475b40a2099c9cf59f5129299650a485'
    calendar = []

    def __init__(self, src=None, dst=None, dtime=None, atime=None, t_t=0, *args, **kwargs):

        super(CalendarSpiderSpider, self).__init__(*args, **kwargs)
        
        self.src = src
        self.dst = dst
        self.dtime = dtime
        self.atime = atime
        self.trip_type = t_t

    def parse(self, response):

        print ("===== Start =====")
        if self.src==None or self.dtime==None or self.dst==None:
            print('Enter correct parameters!!!')
            return

        url = 'https://ibe.belavia.by/api/flights/outbound'
        if self.trip_type == 0:
            print('===========================')
            data = {
                "currency":"USD",
                "searchRoutes":[{"origin":self.src,"destination":self.dst,"departing":self.dtime,"direction":0}],
                "passengerQuantities":[{"code":"ADT","quantity":1}]
            }
            req = Request(url=url, method="POST", callback=self.getCalendar, headers=self.headers, body=json.dumps(data), dont_filter=True)
            yield req

        else:
            print('++++++++++++++++++++++++++')

            data = {
                "currency":"USD",
                "searchRoutes":[
                    {"origin":self.src,"destination":self.dst,"departing":self.dtime,"direction":0},
                    {"origin":self.dst,"destination":self.src,"departing":self.atime,"direction":1}],
                "passengerQuantities":[{"code":"ADT","quantity":1}]
            }

            req = Request(url=url, method="POST", callback=self.getCalendar, headers=self.headers, body=json.dumps(data), dont_filter=True)
            yield req

    def getCalendar(self, response):
        print("===== Get price =====")

        jsonData = json.loads(response.body)
        result = []
        try:
            if len(jsonData['itineraries']) == 0:
                print(" !!! We didn't find any flights that matched your search. !!! ")
                return
            src = jsonData['itineraries'][0]['origin']
            dst = jsonData['itineraries'][0]['destination']

            for flight in jsonData['airLowFares']:
                currency = flight['currency']
                total = flight['total']
                date = flight['departing'].split('T')[0]
                self.calendar.append({
                    'src':src,
                    'dst':dst,
                    'date':date,
                    'price':{'amount':total,'currency':currency}                    
                    })
            # print('---------- G --------------')
            print(self.calendar)

            if self.trip_type == '1':
                print('-----------------------------------------')
                fareBasis1 = jsonData['itineraries'][0]['brands'][0]['fares'][0]['fareBasis']
                rbd1 = jsonData['itineraries'][0]['brands'][0]['fares'][0]['rbd']

                fareBasis2 = jsonData['itineraries'][0]['brands'][0]['fares'][1]['fareBasis']
                rbd2 = jsonData['itineraries'][0]['brands'][0]['fares'][1]['rbd']

                arrivalDateTime1 = jsonData['itineraries'][0]['flights'][0]['arrivalDateTime']
                departureDateTime1 = jsonData['itineraries'][0]['flights'][0]['departureDateTime']

                arrivalDateTime2 = jsonData['itineraries'][0]['flights'][1]['arrivalDateTime']
                departureDateTime2 = jsonData['itineraries'][0]['flights'][1]['departureDateTime']

                marketingAirline1 = jsonData['itineraries'][0]['flights'][0]['marketingAirline']
                marketingAirline2 = jsonData['itineraries'][0]['flights'][1]['marketingAirline']

                flightNumber1 = jsonData['itineraries'][0]['flights'][0]['flightNumber']
                flightNumber2 = jsonData['itineraries'][0]['flights'][1]['flightNumber']

                data = {
                        "currency":"USD",
                        "searchRoutes":[
                            {"origin":self.src,"destination":self.dst,"departing":self.dtime,"direction":0},
                            {"origin":self.dst,"destination":self.src,"departing":self.atime,"direction":1}],
                        "passengerQuantities":[{"code":"ADT","quantity":1}],
                        "flightSelects":[
                            {"rbd":rbd1,
                            "fareBasis":fareBasis1,
                            "brand":"EF",
                            "airline":marketingAirline1,
                            "marketingAirline":marketingAirline1,
                            "arrival":arrivalDateTime1,
                            "flightNumber":flightNumber1,
                            "departing":departureDateTime1},
                            {"rbd":rbd2,
                            "fareBasis":fareBasis2,
                            "brand":"EF",
                            "airline":marketingAirline2,
                            "marketingAirline":marketingAirline2,
                            "arrival":arrivalDateTime2,
                            "flightNumber":flightNumber2,
                            "departing":departureDateTime2}]
                        }
                url = 'https://ibe.belavia.by/api/flights/inbound'
                req = Request(url=url, method="POST", callback=self.getreturnCalendar, headers=self.headers, body=json.dumps(data), dont_filter=True)
                yield req

        except:
            try:
                if jsonData['errorCode'] == '400':
                    if self.trip_type == 0:
                        url = 'https://ibe.belavia.by/select/{}{}/{}/adults-1/children-0/infants-0'.format(self.src, self.dst, self.dtime)
                    else:
                        url = 'https://ibe.belavia.by/select/{}{}/{}/{}/adults-1/children-0/infants-0'.format(self.src, self.dst, self.dtime, self.atime)

                    print('Solve the recaptcha')
                    recaptcha_key = '6Lddc5MUAAAAAO8mj_nDS6lk2UoWEvhOWX57OcDE'
                    recaptcha_answer = self.solve_captcha(recaptcha_key, url)
                    yield recaptcha_answer

                    req = Request(url=self.start_urls[0], dont_filter=True)
                    yield req
            except:
                pass

    def getreturnCalendar(self, response):
        # print("===== Get price 1 =====")
        jsonData = json.loads(response.body)
        result = []
        try:
            src = jsonData['itineraries'][0]['origin']
            dst = jsonData['itineraries'][0]['destination']
            for flight in jsonData['airLowFares']:
                currency = flight['currency']
                total = flight['total']
                date = flight['departing'].split('T')[0]                
                self.calendar.append({
                    'src':src,
                    'dst':dst,
                    'date':date,
                    'price':{'amount':total,'currency':currency}                    
                    })
            # print('---------- R --------------')
            print(self.calendar)                
        except:
            pass

    def solve_captcha(self, captcha_site_key, url):
        print(url)
        #
        try:
            s = requests.Session()

            # here we post site key to 2captcha to get captcha ID (and we parse it here too)
            captcha_id = s.post("http://2captcha.com/in.php?key=%s&method=userrecaptcha&googlekey=%s&pageurl=%s" %(self.captcha_api_key, captcha_site_key, url)).text.split('|')[1]
            # then we parse gresponse from 2captcha response
            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.captcha_api_key, captcha_id)).text

            #print("+++++++++++++++++++solving ref captcha++++++++++++++++++++")
            try_count = 0
            total_count = 0
            while 'CAPCHA_NOT_READY' in recaptcha_answer or 'ERROR_CAPTCHA_UNSOLVABLE' in recaptcha_answer:
                sleep(5)
                print( "Prev Answer: {}, Call 2Captcha....{}".format(recaptcha_answer, captcha_id))

                recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.captcha_api_key, captcha_id)).text
               
                if total_count == 30:
                    print("Captcha ID count reached at limit value.")
                    break

                if try_count == 12:
                    print( "Captcha ID was changed." )
                    captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(self.captcha_api_key, captcha_site_key, url)).text.split('|')[1]
                    total_count += 1
                    try_count = 0

                try_count += 1
            
            if ('CAPCHA_NOT_READY' not in recaptcha_answer) and ('ERROR_CAPTCHA_UNSOLVABLE' not in recaptcha_answer):
                recaptcha_answer = recaptcha_answer.split('|')[1]
                #print("^^^^^^^^^^^^^^^^^^^^^^^solved ref captcha^^^^^^^^^^^^^^^^^^^^^^^^^")
            else:
                print("-----------------------not solved ref captcha----------------------")
        except Exception as e:
            print(e)
            recaptcha_answer = "CAPCHA_NOT_READY"


        data = '{"token":"'+recaptcha_answer+'"}'

        response = s.post('https://ibe.belavia.by/api/verify', headers=self.headers, data=data)
