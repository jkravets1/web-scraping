# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Yahoofinance.items import MajorholdersItem
from Yahoofinance.items import InsidertransactionsItem
import time, datetime, csv, random, base64, json, re
import requests

class HoldersSpider(scrapy.Spider):
    name = "holders"
    allowed_domains = ["yahoo.com"]

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='', *args, **kwargs):

        super(HoldersSpider, self).__init__(*args, **kwargs)
        
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
            # url = "https://finance.yahoo.com/quote/AAPL/holders?p=AAPL"

            url = "https://finance.yahoo.com/quote/csco/insider-transactions?p=csco"
            variable =''.join(variable).strip()
            # url = "https://finance.yahoo.com/quote/" + variable + "/holders?p=" + variable
            req = self.set_proxies(url, self.getItem)
            req.meta['variable'] = variable
            # req.meta['page_count'] = 0

            yield req



            # return

    def getItem(self, response):

        print "===== get items ====="
        symbol = response.meta["variable"]

        # transactionsItems = response.xpath('//table[@class="W(100%) BdB Bdc($c-fuji-grey-c)"]/tbody/tr')
        # for element in transactionsItems:
        #     date = element.xpath('./td[5]/span/text()').extract()
        #     break
        # print len(transactionsItems)
        # print date
        # return

        json_text = re.search("root.App.main = (.*?);\n", response.body).group(1)
        json_data = json.loads(json_text)
        # print json_data
        print "============== Major Holders Data =============="

        majorholdersItem = MajorholdersItem()

        majorholdersItem["Symbol"] = symbol
        try:
            majorHoldersData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["majorHoldersBreakdown"]
        except:
            return
        
        try:
            Percent_of_Shares_Held_by_All_Insider = majorHoldersData["insidersPercentHeld"]["fmt"]
        except:
            Percent_of_Shares_Held_by_All_Insider = ""
        majorholdersItem['Percent_of_Shares_Held_by_All_Insider'] = Percent_of_Shares_Held_by_All_Insider

        try:
            Percent_of_Shares_Held_by_Institutions = majorHoldersData["institutionsPercentHeld"]["fmt"]
        except:
            Percent_of_Shares_Held_by_Institutions = ""
        majorholdersItem['Percent_of_Shares_Held_by_Institutions'] = Percent_of_Shares_Held_by_Institutions

        try:
            Percent_of_Float_Held_by_Institutions = majorHoldersData["institutionsFloatPercentHeld"]["fmt"]
        except:
            Percent_of_Float_Held_by_Institutions = ""
        majorholdersItem['Percent_of_Float_Held_by_Institutions'] = Percent_of_Float_Held_by_Institutions

        try:
            Number_of_Institutions_Holding_Shares = majorHoldersData["institutionsCount"]["longFmt"]
        except:
            Number_of_Institutions_Holding_Shares = ""
        majorholdersItem['Number_of_Institutions_Holding_Shares'] = Number_of_Institutions_Holding_Shares

        # print Percent_of_Shares_Held_by_All_Insider
        # print Percent_of_Shares_Held_by_Institutions
        # print Percent_of_Float_Held_by_Institutions
        # print Number_of_Institutions_Holding_Shares

        yield majorholdersItem

        print "============== Insider Transactions Data =============="

        insidertransactionsItem = InsidertransactionsItem()
        
        insidertransactionsItem['Symbol'] = symbol

        try:
            insiderTransactionsData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["insiderTransactions"]["transactions"]
        except:
            return
        print len(insiderTransactionsData)
        # print insiderTransactionsData
        return
        for insiderTransactionsEle in insiderTransactionsData:

            print "---------------------------"
            Name = insiderTransactionsEle["filerName"]
            insidertransactionsItem['Name'] = Name

            Relation = insiderTransactionsEle["filerRelation"]
            insidertransactionsItem['Relation'] = Relation

            Transaction = insiderTransactionsEle["transactionText"]
            insidertransactionsItem['Transaction'] = Transaction

            ownership = insiderTransactionsEle["ownership"]
            if ownership == "D":
                Type = "Direct"
            elif ownership == "I":
                Type = "Indirect"
            else:
                Type = ""
            insidertransactionsItem['Type'] = Type

            try:
                Value = insiderTransactionsEle["value"]["longFmt"]
            except:
                Value = ""
            insidertransactionsItem['Value'] = Value

            Date = insiderTransactionsEle["startDate"]["fmt"]
            insidertransactionsItem['Date'] = Date

            Shares = insiderTransactionsEle["shares"]["longFmt"]
            insidertransactionsItem['Shares'] = Shares

            # print Name
            # print Relation
            # print Transaction
            # print Type
            # print Value
            # print Date
            # print Shares

            yield insidertransactionsItem

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