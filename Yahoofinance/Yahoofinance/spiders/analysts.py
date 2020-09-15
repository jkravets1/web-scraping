# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Yahoofinance.items import AnalystsItem
import time, datetime, csv, random, base64, json, re
import requests

class AnalystsSpider(scrapy.Spider):
    name = "analysts"
    allowed_domains = ["yahoo.com"]

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='', *args, **kwargs):

        super(AnalystsSpider, self).__init__(*args, **kwargs)
        
        self.select_param = param

    def set_proxies(self, url, callback):

        req = Request(url=url, callback=callback, dont_filter=True)
        user_pass=base64.encodestring(b'pp-eiffykey:reyerobf').strip().decode('utf-8')
        req.meta['proxy'] = "http://ofurgody.proxysolutions.net:11355"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):

        self.clearLog()
        self.makeLog("=================== Start ===================")

        # if (self.select_param!="all" and self.select_param.isdigit()!=True):
        #     print("===== Please Insert Correct Command!!! =====")
        #     print("* Case Get All Data : scrapy crawl googlespider -a param=all")
        #     print("* Case Get Last x pages : scrapy crawl googlespider -a param=x (ex : param=3)")

            # return

        # ipUrl = 'http://lumtest.com/myip.json'
        # proxy_ip_req = self.set_proxies(ipUrl, self.get_proxy_ip)
        # yield proxy_ip_req
        # return

        myfile = open("url_list.csv", "rb")
        urllist = csv.reader(myfile)

        for i, variable in enumerate(urllist):
            
            # test
            # url = "https://finance.yahoo.com/quote/AAPL/analysts?p=AAPL"

            variable =''.join(variable).strip()
            url = "https://finance.yahoo.com/quote/" + variable + "/analysts?p=" + variable
            req = self.set_proxies(url, self.getItem)
            req.meta['variable'] = variable
            # req.meta['page_count'] = 0

            yield req

            # return

    def getItem(self, response):
        print "===== get items ====="
        symbol = response.meta["variable"]

        analystsItem = AnalystsItem()

        json_text = re.search("root.App.main = (.*?);\n", response.body).group(1)
        json_data = json.loads(json_text)
        # print json_data
        analystsData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"]
        analystsData1 = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsHistory"]["history"]

        analystsItem['Symbol'] = symbol

        for count, analystsEle in enumerate(analystsData):
            if count == 4:
                break
            print "----------------"

            Date = analystsEle["endDate"]
            analystsItem['Date'] = Date

            Earnings_Estimate_No_of_Analysts = analystsEle["earningsEstimate"]["numberOfAnalysts"]["longFmt"]
            analystsItem['Earnings_Estimate_No_of_Analysts'] = Earnings_Estimate_No_of_Analysts

            Earnings_Estimate_Avg_Estimate = analystsEle["earningsEstimate"]["avg"]["fmt"]
            analystsItem['Earnings_Estimate_Avg_Estimate'] = Earnings_Estimate_Avg_Estimate

            Earnings_Estimate_Low_Estimate = analystsEle["earningsEstimate"]["low"]["fmt"]
            analystsItem['Earnings_Estimate_Low_Estimate'] = Earnings_Estimate_Low_Estimate

            Earnings_Estimate_High_Estimate = analystsEle["earningsEstimate"]["high"]["fmt"]
            analystsItem['Earnings_Estimate_High_Estimate'] = Earnings_Estimate_High_Estimate

            Earnings_Estimate_Year_Ago_EPS = analystsEle["earningsEstimate"]["yearAgoEps"]["fmt"]
            analystsItem['Earnings_Estimate_Year_Ago_EPS'] = Earnings_Estimate_Year_Ago_EPS

            Revenue_Estimate_No_of_Analysts = analystsEle["revenueEstimate"]["numberOfAnalysts"]["longFmt"]
            analystsItem['Revenue_Estimate_No_of_Analysts'] = Revenue_Estimate_No_of_Analysts

            Revenue_Estimate_Avg_Estimate = analystsEle["revenueEstimate"]["avg"]["fmt"]
            analystsItem['Revenue_Estimate_Avg_Estimate'] = Revenue_Estimate_Avg_Estimate

            Revenue_Estimate_Low_Estimate = analystsEle["revenueEstimate"]["low"]["fmt"]
            analystsItem['Revenue_Estimate_Low_Estimate'] = Revenue_Estimate_Low_Estimate

            Revenue_Estimate_High_Estimate = analystsEle["revenueEstimate"]["high"]["fmt"]
            analystsItem['Revenue_Estimate_High_Estimate'] = Revenue_Estimate_High_Estimate

            Revenue_Estimate_Year_Ago_EPS = analystsEle["revenueEstimate"]["yearAgoRevenue"]["fmt"]
            analystsItem['Revenue_Estimate_Year_Ago_EPS'] = Revenue_Estimate_Year_Ago_EPS
            
            Revenue_Estimate_Sales_Growth = analystsEle["revenueEstimate"]["growth"]["fmt"]
            analystsItem['Revenue_Estimate_Sales_Growth'] = Revenue_Estimate_Sales_Growth


            Earnings_History_Date = analystsData1[count]["quarter"]["fmt"]
            analystsItem['Earnings_History_Date'] = Earnings_History_Date

            EPS_Est = analystsData1[count]["epsEstimate"]["fmt"]
            analystsItem['EPS_Est'] = EPS_Est

            EPS_Actual = analystsData1[count]["epsActual"]["fmt"]
            analystsItem['EPS_Actual'] = EPS_Actual

            Difference = analystsData1[count]["epsDifference"]["fmt"]
            analystsItem['Difference'] = Difference

            Surprise = analystsData1[count]["surprisePercent"]["fmt"]
            analystsItem['Surprise'] = Surprise

            try:
                Current_Estimate = analystsEle["epsTrend"]["current"]["fmt"]
            except:
                Current_Estimate = ""
            analystsItem['Current_Estimate'] = Current_Estimate

            try:
                Days_7_Ago = analystsEle["epsTrend"]["7daysAgo"]["fmt"]
            except:
                Days_7_Ago = ""
            analystsItem['Days_7_Ago'] = Days_7_Ago

            try:
                Days_30_Ago = analystsEle["epsTrend"]["30daysAgo"]["fmt"]
            except:
                Days_30_Ago = ""
            analystsItem['Days_30_Ago'] = Days_30_Ago

            try:
                Days_60_Ago = analystsEle["epsTrend"]["60daysAgo"]["fmt"]
            except:
                Days_60_Ago = ""
            analystsItem['Days_60_Ago'] = Days_60_Ago

            try:
                Days_90_Ago = analystsEle["epsTrend"]["90daysAgo"]["fmt"]
            except:
                Days_90_Ago = ""
            analystsItem['Days_90_Ago'] = Days_90_Ago

            try:
                Up_Last_7_Days = analystsEle["epsRevisions"]["upLast7days"]["fmt"]
            except:
                Up_Last_7_Days = ""
            analystsItem['Up_Last_7_Days'] = Up_Last_7_Days

            try:
                Up_Last_30_Days = analystsEle["epsRevisions"]["upLast30days"]["fmt"]
            except:
                Up_Last_30_Days = ""
            analystsItem['Up_Last_30_Days'] = Up_Last_30_Days

            try:
                Down_Last_30_Days = analystsEle["epsRevisions"]["downLast30days"]["fmt"]
            except:
                Down_Last_30_Days = ""
            analystsItem['Down_Last_30_Days'] = Down_Last_30_Days

            try:
                Down_Last_90_Days = analystsEle["epsRevisions"]["downLast90days"]["fmt"]
            except:
                Down_Last_90_Days = ""
            analystsItem['Down_Last_90_Days'] = Down_Last_90_Days

            # Current_Qtr = analystsEle["growth"]["fmt"]

            # Next_Qtr = analystsEle["growth"]["fmt"]

            # Current_Year = analystsEle["growth"]["fmt"]

            # Next_Qtr = analystsEle["growth"]["fmt"]

            # Next_5_Years_per_annum = analystsEle["growth"]["fmt"]

            # Past_5_Years_per_annum = analystsEle["growth"]["fmt"]

            # print Date
            # print Earnings_Estimate_No_of_Analysts
            # print Earnings_Estimate_Avg_Estimate
            # print Earnings_Estimate_Low_Estimate
            # print Earnings_Estimate_High_Estimate
            # print Earnings_Estimate_Year_Ago_EPS
            # print Revenue_Estimate_No_of_Analysts
            # print Revenue_Estimate_Avg_Estimate
            # print Revenue_Estimate_Low_Estimate
            # print Revenue_Estimate_High_Estimate
            # print Revenue_Estimate_Year_Ago_EPS
            # print Revenue_Estimate_Sales_Growth
            # print Earnings_History_Date
            # print EPS_Est
            # print EPS_Actual
            # print Difference
            # print Surprise

            # print Current_Estimate
            # print Days_7_Ago
            # print Days_30_Ago
            # print Days_60_Ago
            # print Days_90_Ago
            # print Up_Last_7_Days
            # print Up_Last_30_Days
            # print Down_Last_30_Days
            # print Down_Last_90_Days

            yield analystsItem

            # break

        self.makeLog(symbol)

    def makeLog(self, txt):

        standartdate = datetime.datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()             