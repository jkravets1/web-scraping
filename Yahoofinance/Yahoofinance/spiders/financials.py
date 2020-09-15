# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Yahoofinance.items import IncomestatementsItem
from Yahoofinance.items import BalancesheetItem
from Yahoofinance.items import CashflowItem
import time, datetime, csv, random, base64, json, re
import requests

class FinancialsSpider(scrapy.Spider):
    name = "financials"
    allowed_domains = ["yahoo.com"]
    start_urls = (
        'http://www.yahoo.com/',
    )

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='', *args, **kwargs):

        super(FinancialsSpider, self).__init__(*args, **kwargs)
        
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
            # url = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"

            variable =''.join(variable).strip()
            url = "https://finance.yahoo.com/quote/" + variable + "/financials?p=" + variable
            req = self.set_proxies(url, self.getItem)
            req.meta['variable'] = variable
            # req.meta['page_count'] = 0

            yield req

            # return

    def getItem(self, response):
        print "===== get items ====="
        symbol = response.meta["variable"]

        json_text = re.search("root.App.main = (.*?);\n", response.body).group(1)
        json_data = json.loads(json_text)
        # print json_data

        IncomeItem = IncomestatementsItem()

        print "============== IncomeStatement Quarterly Data =============="
        incomeQuarterlyData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["incomeStatementHistoryQuarterly"]["incomeStatementHistory"]
        
        for incomeQuarterly in incomeQuarterlyData:
            print "----------------"
            date = incomeQuarterly["endDate"]["fmt"]
            IncomeItem['Date'] = date

            try:
                Total_Revenue = incomeQuarterly["totalRevenue"]["longFmt"]
            except:
                Total_Revenue = ""
            IncomeItem['Total_Revenue'] = Total_Revenue

            try:
                Cost_of_Revenue = incomeQuarterly["costOfRevenue"]["longFmt"]
            except:
                Cost_of_Revenue = ""
            IncomeItem['Cost_of_Revenue'] = Cost_of_Revenue

            try:
                Gross_Profit = incomeQuarterly["grossProfit"]["longFmt"]
            except:
                Gross_Profit = ""
            IncomeItem['Gross_Profit'] = Gross_Profit

            try:
                Research_Development = incomeQuarterly["researchDevelopment"]["longFmt"]
            except:
                Research_Development = ""
            IncomeItem['Research_Development'] = Research_Development

            try:
                Selling_General_and_Administrative = incomeQuarterly["sellingGeneralAdministrative"]["longFmt"]
            except:
                Selling_General_and_Administrative = ""
            IncomeItem['Selling_General_and_Administrative'] = Selling_General_and_Administrative

            try:
                Non_Recurring = incomeQuarterly["nonRecurring"]["longFmt"]
            except:
                Non_Recurring = "-"
            IncomeItem['Non_Recurring'] = Non_Recurring

            try:
                Others = incomeQuarterly["otherOperatingExpenses"]["longFmt"]
            except:
                Others = "-"
            IncomeItem['Others'] = Others

            try:
                Total_Operating_Expenses = incomeQuarterly["totalOperatingExpenses"]["longFmt"]
            except:
                Total_Operating_Expenses = ""
            IncomeItem['Total_Operating_Expenses'] = Total_Operating_Expenses

            try:
                Operating_Income_or_Loss = incomeQuarterly["operatingIncome"]["longFmt"]
            except:
                Operating_Income_or_Loss = ""
            IncomeItem['Operating_Income_or_Loss'] = Operating_Income_or_Loss

            try:
                Total_Other_IncomeExpenses_Net = incomeQuarterly["totalOtherIncomeExpenseNet"]["longFmt"]
            except:
                Total_Other_IncomeExpenses_Net = ""
            IncomeItem['Total_Other_IncomeExpenses_Net'] = Total_Other_IncomeExpenses_Net

            try:
                Earnings_Before_Interest_and_Taxes = incomeQuarterly["ebit"]["longFmt"]
            except:
                Earnings_Before_Interest_and_Taxes = ""
            IncomeItem['Earnings_Before_Interest_and_Taxes'] = Earnings_Before_Interest_and_Taxes

            try:
                Interest_Expense = incomeQuarterly["interestExpense"]["longFmt"]
            except:
                Interest_Expense = "-"
            IncomeItem['Interest_Expense'] = Interest_Expense

            try:
                Income_Before_Tax = incomeQuarterly["incomeBeforeTax"]["longFmt"]
            except:
                Income_Before_Tax = ""
            IncomeItem['Income_Before_Tax'] = Income_Before_Tax

            try:
                Income_Tax_Expense = incomeQuarterly["incomeTaxExpense"]["longFmt"]
            except:
                Income_Tax_Expense = ""
            IncomeItem['Income_Tax_Expense'] = Income_Tax_Expense

            try:
                Minority_Interest = incomeQuarterly["minorityInterest"]["longFmt"]
            except:
                Minority_Interest = "-"
            IncomeItem['Minority_Interest'] = Minority_Interest

            try:
                Net_Income_From_Continuing_Ops = incomeQuarterly["netIncomeFromContinuingOps"]["longFmt"]
            except:
                Net_Income_From_Continuing_Ops = ""
            IncomeItem['Net_Income_From_Continuing_Ops'] = Net_Income_From_Continuing_Ops

            try:
                Discontinued_Operations = incomeQuarterly["discontinuedOperations"]["longFmt"]
            except:
                Discontinued_Operations = "-"
            IncomeItem['Discontinued_Operations'] = Discontinued_Operations

            try:
                Extraordinary_Items = incomeQuarterly["extraordinaryItems"]["longFmt"]
            except:
                Extraordinary_Items = "-"
            IncomeItem['Extraordinary_Items'] = Extraordinary_Items

            try:
                Effect_Of_Accounting_Changes = incomeQuarterly["effectOfAccountingCharges"]["longFmt"]
            except:
                Effect_Of_Accounting_Changes = "-"
            IncomeItem['Effect_Of_Accounting_Changes'] = Effect_Of_Accounting_Changes

            try:
                Other_Items = incomeQuarterly["otherItems"]["longFmt"]
            except:
                Other_Items = "-"
            IncomeItem['Other_Items'] = Other_Items

            try:
                Net_Income = incomeQuarterly["netIncome"]["longFmt"]
            except:
                Net_Income = ""
            IncomeItem['Net_Income'] = Net_Income

            try:
                Preferred_Stock_And_Other_Adjustments = incomeQuarterly["preferredStockAndOtherAdjustments"]["longFmt"]
            except:
                Preferred_Stock_And_Other_Adjustments = "-"
            IncomeItem['Preferred_Stock_And_Other_Adjustments'] = Preferred_Stock_And_Other_Adjustments

            try:
                Net_Income_Applicable_To_Common_Shares = incomeQuarterly["netIncomeApplicableToCommonShares"]["longFmt"]
            except:
                Net_Income_Applicable_To_Common_Shares = ""
            IncomeItem['Net_Income_Applicable_To_Common_Shares'] = Net_Income_Applicable_To_Common_Shares
            
            IncomeItem['Symbol'] = symbol
            IncomeItem['Period'] = "Quarterly"

            # print date
            # print Total_Revenue
            # print Cost_of_Revenue
            # print Gross_Profit
            # print Research_Development
            # print Selling_General_and_Administrative
            # print Non_Recurring
            # print Others
            # print Total_Operating_Expenses
            # print Operating_Income_or_Loss
            # print Total_Other_IncomeExpenses_Net
            # print Earnings_Before_Interest_and_Taxes
            # print Interest_Expense
            # print Income_Before_Tax
            # print Income_Tax_Expense
            # print Minority_Interest
            # print Net_Income_From_Continuing_Ops
            # print Discontinued_Operations
            # print Extraordinary_Items
            # print Effect_Of_Accounting_Changes
            # print Other_Items
            # print Net_Income
            # print Preferred_Stock_And_Other_Adjustments
            # print Net_Income_Applicable_To_Common_Shares

            yield IncomeItem

            # break

        print "============== IncomeStatement Annual Data =============="

        incomeAnnualData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["incomeStatementHistory"]["incomeStatementHistory"]

        for incomeAnnual in incomeAnnualData:
            print "----------------"
            date = incomeAnnual["endDate"]["fmt"]
            IncomeItem['Date'] = date

            try:
                Total_Revenue = incomeAnnual["totalRevenue"]["longFmt"]
            except:
                Total_Revenue = ""
            IncomeItem['Total_Revenue'] = Total_Revenue

            try:
                Cost_of_Revenue = incomeAnnual["costOfRevenue"]["longFmt"]
            except:
                Cost_of_Revenue = ""
            IncomeItem['Cost_of_Revenue'] = Cost_of_Revenue

            try:
                Gross_Profit = incomeAnnual["grossProfit"]["longFmt"]
            except:
                Gross_Profit = ""
            IncomeItem['Gross_Profit'] = Gross_Profit

            try:
                Research_Development = incomeAnnual["researchDevelopment"]["longFmt"]
            except:
                Research_Development = ""
            IncomeItem['Research_Development'] = Research_Development

            try:
                Selling_General_and_Administrative = incomeAnnual["sellingGeneralAdministrative"]["longFmt"]
            except:
                Selling_General_and_Administrative = ""
            IncomeItem['Selling_General_and_Administrative'] = Selling_General_and_Administrative

            try:
                Non_Recurring = incomeAnnual["nonRecurring"]["longFmt"]
            except:
                Non_Recurring = "-"
            IncomeItem['Non_Recurring'] = Non_Recurring

            try:
                Others = incomeAnnual["otherOperatingExpenses"]["longFmt"]
            except:
                Others = "-"
            IncomeItem['Others'] = Others

            try:
                Total_Operating_Expenses = incomeAnnual["totalOperatingExpenses"]["longFmt"]
            except:
                Total_Operating_Expenses = ""
            IncomeItem['Total_Operating_Expenses'] = Total_Operating_Expenses

            try:
                Operating_Income_or_Loss = incomeAnnual["operatingIncome"]["longFmt"]
            except:
                Operating_Income_or_Loss = ""
            IncomeItem['Operating_Income_or_Loss'] = Operating_Income_or_Loss

            try:
                Total_Other_IncomeExpenses_Net = incomeAnnual["totalOtherIncomeExpenseNet"]["longFmt"]
            except:
                Total_Other_IncomeExpenses_Net = ""
            IncomeItem['Total_Other_IncomeExpenses_Net'] = Total_Other_IncomeExpenses_Net

            try:
                Earnings_Before_Interest_and_Taxes = incomeAnnual["ebit"]["longFmt"]
            except:
                Earnings_Before_Interest_and_Taxes = ""
            IncomeItem['Earnings_Before_Interest_and_Taxes'] = Earnings_Before_Interest_and_Taxes

            try:
                Interest_Expense = incomeAnnual["interestExpense"]["longFmt"]
            except:
                Interest_Expense = "-"
            IncomeItem['Interest_Expense'] = Interest_Expense

            try:
                Income_Before_Tax = incomeAnnual["incomeBeforeTax"]["longFmt"]
            except:
                Income_Before_Tax = ""
            IncomeItem['Income_Before_Tax'] = Income_Before_Tax

            try:
                Income_Tax_Expense = incomeAnnual["incomeTaxExpense"]["longFmt"]
            except:
                Income_Tax_Expense = ""
            IncomeItem['Income_Tax_Expense'] = Income_Tax_Expense

            try:
                Minority_Interest = incomeAnnual["minorityInterest"]["longFmt"]
            except:
                Minority_Interest = "-"
            IncomeItem['Minority_Interest'] = Minority_Interest

            try:
                Net_Income_From_Continuing_Ops = incomeAnnual["netIncomeFromContinuingOps"]["longFmt"]
            except:
                Net_Income_From_Continuing_Ops = ""
            IncomeItem['Net_Income_From_Continuing_Ops'] = Net_Income_From_Continuing_Ops

            try:
                Discontinued_Operations = incomeAnnual["discontinuedOperations"]["longFmt"]
            except:
                Discontinued_Operations = "-"
            IncomeItem['Discontinued_Operations'] = Discontinued_Operations

            try:
                Extraordinary_Items = incomeAnnual["extraordinaryItems"]["longFmt"]
            except:
                Extraordinary_Items = "-"
            IncomeItem['Extraordinary_Items'] = Extraordinary_Items

            try:
                Effect_Of_Accounting_Changes = incomeAnnual["effectOfAccountingCharges"]["longFmt"]
            except:
                Effect_Of_Accounting_Changes = "-"
            IncomeItem['Effect_Of_Accounting_Changes'] = Effect_Of_Accounting_Changes

            try:
                Other_Items = incomeAnnual["otherItems"]["longFmt"]
            except:
                Other_Items = "-"
            IncomeItem['Other_Items'] = Other_Items

            try:
                Net_Income = incomeAnnual["netIncome"]["longFmt"]
            except:
                Net_Income = ""
            IncomeItem['Net_Income'] = Net_Income

            try:
                Preferred_Stock_And_Other_Adjustments = incomeAnnual["preferredStockAndOtherAdjustments"]["longFmt"]
            except:
                Preferred_Stock_And_Other_Adjustments = "-"
            IncomeItem['Preferred_Stock_And_Other_Adjustments'] = Preferred_Stock_And_Other_Adjustments

            try:
                Net_Income_Applicable_To_Common_Shares = incomeAnnual["netIncomeApplicableToCommonShares"]["longFmt"]
            except:
                Net_Income_Applicable_To_Common_Shares = ""
            IncomeItem['Net_Income_Applicable_To_Common_Shares'] = Net_Income_Applicable_To_Common_Shares
            
            IncomeItem['Symbol'] = symbol
            IncomeItem['Period'] = "Annual"

            # print date
            # print Total_Revenue
            # print Cost_of_Revenue
            # print Gross_Profit
            # print Research_Development
            # print Selling_General_and_Administrative
            # print Non_Recurring
            # print Others
            # print Total_Operating_Expenses
            # print Operating_Income_or_Loss
            # print Total_Other_IncomeExpenses_Net
            # print Earnings_Before_Interest_and_Taxes
            # print Interest_Expense
            # print Income_Before_Tax
            # print Income_Tax_Expense
            # print Minority_Interest
            # print Net_Income_From_Continuing_Ops
            # print Discontinued_Operations
            # print Extraordinary_Items
            # print Effect_Of_Accounting_Changes
            # print Other_Items
            # print Net_Income
            # print Preferred_Stock_And_Other_Adjustments
            # print Net_Income_Applicable_To_Common_Shares

            yield IncomeItem

            # break

        print "============== Balance Sheet Quarterly Data =============="

        BalanceItem = BalancesheetItem()

        balanceQuarterlyData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistoryQuarterly"]["balanceSheetStatements"]

        for balanceQuarterly in balanceQuarterlyData:
            print '---------------------'
            date = balanceQuarterly["endDate"]["fmt"]
            BalanceItem['Date'] = date

            try:
                Cash_And_Cash_Equivalents = balanceQuarterly["cash"]["longFmt"]
            except:
                Cash_And_Cash_Equivalents = ""
            BalanceItem['Cash_And_Cash_Equivalents'] = Cash_And_Cash_Equivalents

            try:
                Short_Term_Investments = balanceQuarterly["shortTermInvestments"]["longFmt"]
            except:
                Short_Term_Investments = ""
            BalanceItem['Short_Term_Investments'] = Short_Term_Investments

            try:
                Net_Receivables = balanceQuarterly["netReceivables"]["longFmt"]
            except:
                Net_Receivables = ""
            BalanceItem['Net_Receivables'] = Net_Receivables

            try:
                Inventory = balanceQuarterly["inventory"]["longFmt"]
            except:
                Inventory = ""
            BalanceItem['Inventory'] = Inventory

            try:
                Other_Current_Assets = balanceQuarterly["otherCurrentAssets"]["longFmt"]
            except:
                Other_Current_Assets = ""
            BalanceItem['Other_Current_Assets'] = Other_Current_Assets

            try:
                Total_Current_Assets = balanceQuarterly["totalCurrentAssets"]["longFmt"]
            except:
                Total_Current_Assets = ""
            BalanceItem['Total_Current_Assets'] = Total_Current_Assets

            try:
                Long_Term_Investments = balanceQuarterly["longTermInvestments"]["longFmt"]
            except:
                Long_Term_Investments = ""
            BalanceItem['Long_Term_Investments'] = Long_Term_Investments

            try:
                Property_Plant_and_Equipment = balanceQuarterly["propertyPlantEquipment"]["longFmt"]
            except:
                Property_Plant_and_Equipment = ""
            BalanceItem['Property_Plant_and_Equipment'] = Property_Plant_and_Equipment

            try:
                Goodwill = balanceQuarterly["goodWill"]["longFmt"]
            except:
                Goodwill = ""
            BalanceItem['Goodwill'] = Goodwill

            try:
                Intangible_Assets = balanceQuarterly["intangibleAssets"]["longFmt"]
            except:
                Intangible_Assets = ""
            BalanceItem['Intangible_Assets'] = Intangible_Assets

            try:
                Accumulated_Amortization = balanceQuarterly["accumulatedAmortization"]["longFmt"]
            except:
                Accumulated_Amortization = ""
            BalanceItem['Accumulated_Amortization'] = Accumulated_Amortization

            try:
                Other_Assets = balanceQuarterly["otherAssets"]["longFmt"]
            except:
                Other_Assets = ""
            BalanceItem['Other_Assets'] = Other_Assets

            try:
                Deferred_Long_Term_Asset_Charges = balanceQuarterly["deferredLongTermAssetCharges"]["longFmt"]
            except:
                Deferred_Long_Term_Asset_Charges = ""
            BalanceItem['Deferred_Long_Term_Asset_Charges'] = Deferred_Long_Term_Asset_Charges

            try:
                Total_Assets = balanceQuarterly["totalAssets"]["longFmt"]
            except:
                Total_Assets = ""
            BalanceItem['Total_Assets'] = Total_Assets

            try:
                Accounts_Payable = balanceQuarterly["accountsPayable"]["longFmt"]
            except:
                Accounts_Payable = ""
            BalanceItem['Accounts_Payable'] = Accounts_Payable

            try:
                ShortCurrent_Long_Term_Debt = balanceQuarterly["shortLongTermDebt"]["longFmt"]
            except:
                ShortCurrent_Long_Term_Debt = ""
            BalanceItem['ShortCurrent_Long_Term_Debt'] = ShortCurrent_Long_Term_Debt

            try:
                Other_Current_Liabilities = balanceQuarterly["otherCurrentLiab"]["longFmt"]
            except:
                Other_Current_Liabilities = ""
            BalanceItem['Other_Current_Liabilities'] = Other_Current_Liabilities

            try:
                Total_Current_Liabilities = balanceQuarterly["totalCurrentLiabilities"]["longFmt"]
            except:
                Total_Current_Liabilities = ""
            BalanceItem['Total_Current_Liabilities'] = Total_Current_Liabilities

            try:
                Long_Term_Debt = balanceQuarterly["longTermDebt"]["longFmt"]
            except:
                Long_Term_Debt = ""
            BalanceItem['Long_Term_Debt'] = Long_Term_Debt

            try:
                Other_Liabilities = balanceQuarterly["otherLiab"]["longFmt"]
            except:
                Other_Liabilities = ""
            BalanceItem['Other_Liabilities'] = Other_Liabilities

            try:
                Deferred_Long_Term_Liability_Charges = balanceQuarterly["deferredLongTermLiab"]["longFmt"]
            except:
                Deferred_Long_Term_Liability_Charges = ""
            BalanceItem['Deferred_Long_Term_Liability_Charges'] = Deferred_Long_Term_Liability_Charges

            try:
                Minority_Interest = balanceQuarterly["minorityInterest"]["longFmt"]
            except:
                Minority_Interest = ""
            BalanceItem['Minority_Interest'] = Minority_Interest

            try:
                Negative_Goodwill = balanceQuarterly["negativeGoodwill"]["longFmt"]
            except:
                Negative_Goodwill = ""
            BalanceItem['Negative_Goodwill'] = Negative_Goodwill

            try:
                Total_Liabilities = balanceQuarterly["totalLiab"]["longFmt"]
            except:
                Total_Liabilities = ""
            BalanceItem['Total_Liabilities'] = Total_Liabilities

            try:
                Misc_Stocks_Options_Warrants = balanceQuarterly["miscStocksOptionsWarrants"]["longFmt"]
            except:
                Misc_Stocks_Options_Warrants = ""
            BalanceItem['Misc_Stocks_Options_Warrants'] = Misc_Stocks_Options_Warrants

            try:
                Redeemable_Preferred_Stock = balanceQuarterly["redeemablePreferredStock"]["longFmt"]
            except:
                Redeemable_Preferred_Stock = ""
            BalanceItem['Redeemable_Preferred_Stock'] = Redeemable_Preferred_Stock

            try:
                Preferred_Stock = balanceQuarterly["preferredStock"]["longFmt"]
            except:
                Preferred_Stock = ""
            BalanceItem['Preferred_Stock'] = Preferred_Stock

            try:
                Common_Stock = balanceQuarterly["commonStock"]["longFmt"]
            except:
                Common_Stock = ""
            BalanceItem['Common_Stock'] = Common_Stock

            try:
                Retained_Earnings = balanceQuarterly["retainedEarnings"]["longFmt"]
            except:
                Retained_Earnings = ""
            BalanceItem['Retained_Earnings'] = Retained_Earnings

            try:
                Treasury_Stock = balanceQuarterly["treasuryStock"]["longFmt"]
            except:
                Treasury_Stock = ""
            BalanceItem['Treasury_Stock'] = Treasury_Stock

            try:
                Capital_Surplus = balanceQuarterly["capitalSurplus"]["longFmt"]
            except:
                Capital_Surplus = ""
            BalanceItem['Capital_Surplus'] = Capital_Surplus

            try:
                Other_Stockholder_Equity = balanceQuarterly["otherStockholderEquity"]["longFmt"]
            except:
                Other_Stockholder_Equity = ""
            BalanceItem['Other_Stockholder_Equity'] = Other_Stockholder_Equity

            try:
                Total_Stockholder_Equity = balanceQuarterly["totalStockholderEquity"]["longFmt"]
            except:
                Total_Stockholder_Equity = ""
            BalanceItem['Total_Stockholder_Equity'] = Total_Stockholder_Equity

            try:
                Net_Tangible_Assets = balanceQuarterly["netTangibleAssets"]["longFmt"]
            except:
                Net_Tangible_Assets = ""
            BalanceItem['Net_Tangible_Assets'] = Net_Tangible_Assets

            BalanceItem['Symbol'] = symbol
            BalanceItem['Period'] = "Quarterly"

            # print date
            # print Cash_And_Cash_Equivalents
            # print Short_Term_Investments
            # print Net_Receivables
            # print Inventory
            # print Other_Current_Assets
            # print Total_Current_Assets
            # print Long_Term_Investments
            # print Property_Plant_and_Equipment
            # print Goodwill
            # print Intangible_Assets
            # print Other_Assets
            # print Total_Assets
            # print Accounts_Payable
            # print ShortCurrent_Long_Term_Debt
            # print Other_Current_Liabilities
            # print Total_Current_Liabilities
            # print Long_Term_Debt
            # print Other_Liabilities
            # print Deferred_Long_Term_Liability_Charges
            # print Total_Liabilities
            # print Common_Stock
            # print Retained_Earnings
            # print Other_Stockholder_Equity
            # print Total_Stockholder_Equity
            # print Net_Tangible_Assets

            yield BalanceItem

            # break

        print "============== Balance Sheet Annual Data =============="

        balanceAnnualData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistory"]["balanceSheetStatements"]

        for balanceAnnual in balanceAnnualData:
            print '---------------------'
            date = balanceAnnual["endDate"]["fmt"]
            BalanceItem['Date'] = date

            try:
                Cash_And_Cash_Equivalents = balanceAnnual["cash"]["longFmt"]
            except:
                Cash_And_Cash_Equivalents = ""
            BalanceItem['Cash_And_Cash_Equivalents'] = Cash_And_Cash_Equivalents

            try:
                Short_Term_Investments = balanceAnnual["shortTermInvestments"]["longFmt"]
            except:
                Short_Term_Investments = ""
            BalanceItem['Short_Term_Investments'] = Short_Term_Investments

            try:
                Net_Receivables = balanceAnnual["netReceivables"]["longFmt"]
            except:
                Net_Receivables = ""
            BalanceItem['Net_Receivables'] = Net_Receivables

            try:
                Inventory = balanceAnnual["inventory"]["longFmt"]
            except:
                Inventory = ""
            BalanceItem['Inventory'] = Inventory

            try:
                Other_Current_Assets = balanceAnnual["otherCurrentAssets"]["longFmt"]
            except:
                Other_Current_Assets = ""
            BalanceItem['Other_Current_Assets'] = Other_Current_Assets

            try:
                Total_Current_Assets = balanceAnnual["totalCurrentAssets"]["longFmt"]
            except:
                Total_Current_Assets = ""
            BalanceItem['Total_Current_Assets'] = Total_Current_Assets

            try:
                Long_Term_Investments = balanceAnnual["longTermInvestments"]["longFmt"]
            except:
                Long_Term_Investments = ""
            BalanceItem['Long_Term_Investments'] = Long_Term_Investments

            try:
                Property_Plant_and_Equipment = balanceAnnual["propertyPlantEquipment"]["longFmt"]
            except:
                Property_Plant_and_Equipment = ""
            BalanceItem['Property_Plant_and_Equipment'] = Property_Plant_and_Equipment

            try:
                Goodwill = balanceAnnual["goodWill"]["longFmt"]
            except:
                Goodwill = ""
            BalanceItem['Goodwill'] = Goodwill

            try:
                Intangible_Assets = balanceAnnual["intangibleAssets"]["longFmt"]
            except:
                Intangible_Assets = ""
            BalanceItem['Intangible_Assets'] = Intangible_Assets

            try:
                Accumulated_Amortization = balanceAnnual["accumulatedAmortization"]["longFmt"]
            except:
                Accumulated_Amortization = ""
            BalanceItem['Accumulated_Amortization'] = Accumulated_Amortization

            try:
                Other_Assets = balanceAnnual["otherAssets"]["longFmt"]
            except:
                Other_Assets = ""
            BalanceItem['Other_Assets'] = Other_Assets

            try:
                Deferred_Long_Term_Asset_Charges = balanceAnnual["deferredLongTermAssetCharges"]["longFmt"]
            except:
                Deferred_Long_Term_Asset_Charges = ""
            BalanceItem['Deferred_Long_Term_Asset_Charges'] = Deferred_Long_Term_Asset_Charges

            try:
                Total_Assets = balanceAnnual["totalAssets"]["longFmt"]
            except:
                Total_Assets = ""
            BalanceItem['Total_Assets'] = Total_Assets

            try:
                Accounts_Payable = balanceAnnual["accountsPayable"]["longFmt"]
            except:
                Accounts_Payable = ""
            BalanceItem['Accounts_Payable'] = Accounts_Payable

            try:
                ShortCurrent_Long_Term_Debt = balanceAnnual["shortLongTermDebt"]["longFmt"]
            except:
                ShortCurrent_Long_Term_Debt = ""
            BalanceItem['ShortCurrent_Long_Term_Debt'] = ShortCurrent_Long_Term_Debt

            try:
                Other_Current_Liabilities = balanceAnnual["otherCurrentLiab"]["longFmt"]
            except:
                Other_Current_Liabilities = ""
            BalanceItem['Other_Current_Liabilities'] = Other_Current_Liabilities

            try:
                Total_Current_Liabilities = balanceAnnual["totalCurrentLiabilities"]["longFmt"]
            except:
                Total_Current_Liabilities = ""
            BalanceItem['Total_Current_Liabilities'] = Total_Current_Liabilities

            try:
                Long_Term_Debt = balanceAnnual["longTermDebt"]["longFmt"]
            except:
                Long_Term_Debt = ""
            BalanceItem['Long_Term_Debt'] = Long_Term_Debt

            try:
                Other_Liabilities = balanceAnnual["otherLiab"]["longFmt"]
            except:
                Other_Liabilities = ""
            BalanceItem['Other_Liabilities'] = Other_Liabilities

            try:
                Deferred_Long_Term_Liability_Charges = balanceAnnual["deferredLongTermLiab"]["longFmt"]
            except:
                Deferred_Long_Term_Liability_Charges = ""
            BalanceItem['Deferred_Long_Term_Liability_Charges'] = Deferred_Long_Term_Liability_Charges

            try:
                Minority_Interest = balanceAnnual["minorityInterest"]["longFmt"]
            except:
                Minority_Interest = ""
            BalanceItem['Minority_Interest'] = Minority_Interest

            try:
                Negative_Goodwill = balanceAnnual["negativeGoodwill"]["longFmt"]
            except:
                Negative_Goodwill = ""
            BalanceItem['Negative_Goodwill'] = Negative_Goodwill

            try:
                Total_Liabilities = balanceAnnual["totalLiab"]["longFmt"]
            except:
                Total_Liabilities = ""
            BalanceItem['Total_Liabilities'] = Total_Liabilities

            try:
                Misc_Stocks_Options_Warrants = balanceAnnual["miscStocksOptionsWarrants"]["longFmt"]
            except:
                Misc_Stocks_Options_Warrants = ""
            BalanceItem['Misc_Stocks_Options_Warrants'] = Misc_Stocks_Options_Warrants

            try:
                Redeemable_Preferred_Stock = balanceAnnual["redeemablePreferredStock"]["longFmt"]
            except:
                Redeemable_Preferred_Stock = ""
            BalanceItem['Redeemable_Preferred_Stock'] = Redeemable_Preferred_Stock

            try:
                Preferred_Stock = balanceAnnual["preferredStock"]["longFmt"]
            except:
                Preferred_Stock = ""
            BalanceItem['Preferred_Stock'] = Preferred_Stock

            try:
                Common_Stock = balanceAnnual["commonStock"]["longFmt"]
            except:
                Common_Stock = ""
            BalanceItem['Common_Stock'] = Common_Stock

            try:
                Retained_Earnings = balanceAnnual["retainedEarnings"]["longFmt"]
            except:
                Retained_Earnings = ""
            BalanceItem['Retained_Earnings'] = Retained_Earnings

            try:
                Treasury_Stock = balanceAnnual["treasuryStock"]["longFmt"]
            except:
                Treasury_Stock = ""
            BalanceItem['Treasury_Stock'] = Treasury_Stock

            try:
                Capital_Surplus = balanceAnnual["capitalSurplus"]["longFmt"]
            except:
                Capital_Surplus = ""
            BalanceItem['Capital_Surplus'] = Capital_Surplus

            try:
                Other_Stockholder_Equity = balanceAnnual["otherStockholderEquity"]["longFmt"]
            except:
                Other_Stockholder_Equity = ""
            BalanceItem['Other_Stockholder_Equity'] = Other_Stockholder_Equity

            try:
                Total_Stockholder_Equity = balanceAnnual["totalStockholderEquity"]["longFmt"]
            except:
                Total_Stockholder_Equity = ""
            BalanceItem['Total_Stockholder_Equity'] = Total_Stockholder_Equity

            try:
                Net_Tangible_Assets = balanceAnnual["netTangibleAssets"]["longFmt"]
            except:
                Net_Tangible_Assets = ""
            BalanceItem['Net_Tangible_Assets'] = Net_Tangible_Assets

            BalanceItem['Symbol'] = symbol
            BalanceItem['Period'] = "Annual"

            # print date
            # print Cash_And_Cash_Equivalents
            # print Short_Term_Investments
            # print Net_Receivables
            # print Inventory
            # print Other_Current_Assets
            # print Total_Current_Assets
            # print Long_Term_Investments
            # print Property_Plant_and_Equipment
            # print Goodwill
            # print Intangible_Assets
            # print Other_Assets
            # print Total_Assets
            # print Accounts_Payable
            # print ShortCurrent_Long_Term_Debt
            # print Other_Current_Liabilities
            # print Total_Current_Liabilities
            # print Long_Term_Debt
            # print Other_Liabilities
            # print Deferred_Long_Term_Liability_Charges
            # print Total_Liabilities
            # print Common_Stock
            # print Retained_Earnings
            # print Other_Stockholder_Equity
            # print Total_Stockholder_Equity
            # print Net_Tangible_Assets

            yield BalanceItem

            # break

        print "============== Cash Flow Quarterly Data =============="

        CashItem = CashflowItem()

        cashflowQuarterlyData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["cashflowStatementHistoryQuarterly"]["cashflowStatements"]

        for cashflowQuarterly in cashflowQuarterlyData:

            print '---------------------'
            date = cashflowQuarterly["endDate"]["fmt"]
            CashItem['Date'] = date

            try:
                Net_Income = cashflowQuarterly["netIncome"]["longFmt"]
            except:
                Net_Income = ""
            CashItem['Net_Income'] = Net_Income

            try:
                Depreciation = cashflowQuarterly["depreciation"]["longFmt"]
            except:
                Depreciation = ""
            CashItem['Depreciation'] = Depreciation

            try:
                Adjustments_To_Net_Income = cashflowQuarterly["changeToNetincome"]["longFmt"]
            except:
                Adjustments_To_Net_Income = ""
            CashItem['Adjustments_To_Net_Income'] = Adjustments_To_Net_Income

            try:
                Changes_In_Accounts_Receivables = cashflowQuarterly["changeToAccountReceivables"]["longFmt"]
            except:
                Changes_In_Accounts_Receivables = ""
            CashItem['Changes_In_Accounts_Receivables'] = Changes_In_Accounts_Receivables

            try:
                Changes_In_Liabilities = cashflowQuarterly["changeToLiabilities"]["longFmt"]
            except:
                Changes_In_Liabilities = ""
            CashItem['Changes_In_Liabilities'] = Changes_In_Liabilities

            try:
                Changes_In_Inventories = cashflowQuarterly["changeToInventory"]["longFmt"]
            except:
                Changes_In_Inventories = ""
            CashItem['Changes_In_Inventories'] = Changes_In_Inventories

            try:
                Changes_In_Other_Operating_Activities = cashflowQuarterly["changeToOperatingActivities"]["longFmt"]
            except:
                Changes_In_Other_Operating_Activities = ""
            CashItem['Changes_In_Other_Operating_Activities'] = Changes_In_Other_Operating_Activities

            try:
                Total_Cash_Flow_From_Operating_Activities = cashflowQuarterly["totalCashFromOperatingActivities"]["longFmt"]
            except:
                Total_Cash_Flow_From_Operating_Activities = ""
            CashItem['Total_Cash_Flow_From_Operating_Activities'] = Total_Cash_Flow_From_Operating_Activities

            try:
                Capital_Expenditures = cashflowQuarterly["capitalExpenditures"]["longFmt"]
            except:
                Capital_Expenditures = ""
            CashItem['Capital_Expenditures'] = Capital_Expenditures

            try:
                Investments = cashflowQuarterly["investments"]["longFmt"]
            except:
                Investments = ""
            CashItem['Investments'] = Investments

            try:
                Other_Cash_flows_from_Investing_Activities = cashflowQuarterly["otherCashflowsFromInvestingActivities"]["longFmt"]
            except:
                Other_Cash_flows_from_Investing_Activities = ""
            CashItem['Other_Cash_flows_from_Investing_Activities'] = Other_Cash_flows_from_Investing_Activities

            try:
                Total_Cash_Flows_From_Investing_Activities = cashflowQuarterly["totalCashflowsFromInvestingActivities"]["longFmt"]
            except:
                Total_Cash_Flows_From_Investing_Activities = ""
            CashItem['Total_Cash_Flows_From_Investing_Activities'] = Total_Cash_Flows_From_Investing_Activities

            try:
                Dividends_Paid = cashflowQuarterly["dividendsPaid"]["longFmt"]
            except:
                Dividends_Paid = ""
            CashItem['Dividends_Paid'] = Dividends_Paid

            try:
                Sale_Purchase_of_Stock = cashflowQuarterly["salePurchaseOfStock"]["longFmt"]
            except:
                Sale_Purchase_of_Stock = ""
            CashItem['Sale_Purchase_of_Stock'] = Sale_Purchase_of_Stock

            try:
                Net_Borrowings = cashflowQuarterly["netBorrowings"]["longFmt"]
            except:
                Net_Borrowings = ""
            CashItem['Net_Borrowings'] = Net_Borrowings

            try:
                Other_Cash_Flows_from_Financing_Activities = cashflowQuarterly["otherCashflowsFromFinancingActivities"]["longFmt"]
            except:
                Other_Cash_Flows_from_Financing_Activities = ""
            CashItem['Other_Cash_Flows_from_Financing_Activities'] = Other_Cash_Flows_from_Financing_Activities

            try:
                Total_Cash_Flows_From_Financing_Activities = cashflowQuarterly["totalCashFromFinancingActivities"]["longFmt"]
            except:
                Total_Cash_Flows_From_Financing_Activities = ""
            CashItem['Total_Cash_Flows_From_Financing_Activities'] = Total_Cash_Flows_From_Financing_Activities

            try:
                Effect_Of_Exchange_Rate_Changes = cashflowQuarterly["effectOfExchangeRate"]["longFmt"]
            except:
                Effect_Of_Exchange_Rate_Changes = ""
            CashItem['Effect_Of_Exchange_Rate_Changes'] = Effect_Of_Exchange_Rate_Changes

            try:
                Change_In_Cash_and_Cash_Equivalents = cashflowQuarterly["changeInCash"]["longFmt"]
            except:
                Change_In_Cash_and_Cash_Equivalents = ""
            CashItem['Change_In_Cash_and_Cash_Equivalents'] = Change_In_Cash_and_Cash_Equivalents

            CashItem['Symbol'] = symbol
            CashItem['Period'] = "Quarterly"

            # print date
            # print Net_Income
            # print Depreciation
            # print Adjustments_To_Net_Income
            # print Changes_In_Accounts_Receivables
            # print Changes_In_Liabilities
            # print Changes_In_Inventories
            # print Changes_In_Other_Operating_Activities
            # print Total_Cash_Flow_From_Operating_Activities
            # print Capital_Expenditures
            # print Investments
            # print Other_Cash_flows_from_Investing_Activities
            # print Total_Cash_Flows_From_Investing_Activities
            # print Dividends_Paid
            # print Sale_Purchase_of_Stock
            # print Net_Borrowings
            # print Other_Cash_Flows_from_Financing_Activities
            # print Total_Cash_Flows_From_Financing_Activities
            # print Change_In_Cash_and_Cash_Equivalents

            yield CashItem

            # break

        print "============== Cash Flow Annual Data =============="

        cashflowAnnualData = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["cashflowStatementHistory"]["cashflowStatements"]

        for cashflowAnnual in cashflowAnnualData:

            print '---------------------'
            date = cashflowAnnual["endDate"]["fmt"]
            CashItem['Date'] = date

            try:
                Net_Income = cashflowAnnual["netIncome"]["longFmt"]
            except:
                Net_Income = ""
            CashItem['Net_Income'] = Net_Income

            try:
                Depreciation = cashflowAnnual["depreciation"]["longFmt"]
            except:
                Depreciation = ""
            CashItem['Depreciation'] = Depreciation

            try:
                Adjustments_To_Net_Income = cashflowAnnual["changeToNetincome"]["longFmt"]
            except:
                Adjustments_To_Net_Income = ""
            CashItem['Adjustments_To_Net_Income'] = Adjustments_To_Net_Income

            try:
                Changes_In_Accounts_Receivables = cashflowAnnual["changeToAccountReceivables"]["longFmt"]
            except:
                Changes_In_Accounts_Receivables = ""
            CashItem['Changes_In_Accounts_Receivables'] = Changes_In_Accounts_Receivables

            try:
                Changes_In_Liabilities = cashflowAnnual["changeToLiabilities"]["longFmt"]
            except:
                Changes_In_Liabilities = ""
            CashItem['Changes_In_Liabilities'] = Changes_In_Liabilities

            try:
                Changes_In_Inventories = cashflowAnnual["changeToInventory"]["longFmt"]
            except:
                Changes_In_Inventories = ""
            CashItem['Changes_In_Inventories'] = Changes_In_Inventories

            try:
                Changes_In_Other_Operating_Activities = cashflowAnnual["changeToOperatingActivities"]["longFmt"]
            except:
                Changes_In_Other_Operating_Activities = ""
            CashItem['Changes_In_Other_Operating_Activities'] = Changes_In_Other_Operating_Activities

            try:
                Total_Cash_Flow_From_Operating_Activities = cashflowAnnual["totalCashFromOperatingActivities"]["longFmt"]
            except:
                Total_Cash_Flow_From_Operating_Activities = ""
            CashItem['Total_Cash_Flow_From_Operating_Activities'] = Total_Cash_Flow_From_Operating_Activities

            try:
                Capital_Expenditures = cashflowAnnual["capitalExpenditures"]["longFmt"]
            except:
                Capital_Expenditures = ""
            CashItem['Capital_Expenditures'] = Capital_Expenditures

            try:
                Investments = cashflowAnnual["investments"]["longFmt"]
            except:
                Investments = ""
            CashItem['Investments'] = Investments

            try:
                Other_Cash_flows_from_Investing_Activities = cashflowAnnual["otherCashflowsFromInvestingActivities"]["longFmt"]
            except:
                Other_Cash_flows_from_Investing_Activities = ""
            CashItem['Other_Cash_flows_from_Investing_Activities'] = Other_Cash_flows_from_Investing_Activities

            try:
                Total_Cash_Flows_From_Investing_Activities = cashflowAnnual["totalCashflowsFromInvestingActivities"]["longFmt"]
            except:
                Total_Cash_Flows_From_Investing_Activities = ""
            CashItem['Total_Cash_Flows_From_Investing_Activities'] = Total_Cash_Flows_From_Investing_Activities

            try:
                Dividends_Paid = cashflowAnnual["dividendsPaid"]["longFmt"]
            except:
                Dividends_Paid = ""
            CashItem['Dividends_Paid'] = Dividends_Paid

            try:
                Sale_Purchase_of_Stock = cashflowAnnual["salePurchaseOfStock"]["longFmt"]
            except:
                Sale_Purchase_of_Stock = ""
            CashItem['Sale_Purchase_of_Stock'] = Sale_Purchase_of_Stock

            try:
                Net_Borrowings = cashflowAnnual["netBorrowings"]["longFmt"]
            except:
                Net_Borrowings = ""
            CashItem['Net_Borrowings'] = Net_Borrowings

            try:
                Other_Cash_Flows_from_Financing_Activities = cashflowAnnual["otherCashflowsFromFinancingActivities"]["longFmt"]
            except:
                Other_Cash_Flows_from_Financing_Activities = ""
            CashItem['Other_Cash_Flows_from_Financing_Activities'] = Other_Cash_Flows_from_Financing_Activities

            try:
                Total_Cash_Flows_From_Financing_Activities = cashflowAnnual["totalCashFromFinancingActivities"]["longFmt"]
            except:
                Total_Cash_Flows_From_Financing_Activities = ""
            CashItem['Total_Cash_Flows_From_Financing_Activities'] = Total_Cash_Flows_From_Financing_Activities

            try:
                Effect_Of_Exchange_Rate_Changes = cashflowAnnual["effectOfExchangeRate"]["longFmt"]
            except:
                Effect_Of_Exchange_Rate_Changes = ""
            CashItem['Effect_Of_Exchange_Rate_Changes'] = Effect_Of_Exchange_Rate_Changes
            
            try:
                Change_In_Cash_and_Cash_Equivalents = cashflowAnnual["changeInCash"]["longFmt"]
            except:
                Change_In_Cash_and_Cash_Equivalents = ""
            CashItem['Change_In_Cash_and_Cash_Equivalents'] = Change_In_Cash_and_Cash_Equivalents

            CashItem['Symbol'] = symbol
            CashItem['Period'] = "Annual"

            # print date
            # print Net_Income
            # print Depreciation
            # print Adjustments_To_Net_Income
            # print Changes_In_Accounts_Receivables
            # print Changes_In_Liabilities
            # print Changes_In_Inventories
            # print Changes_In_Other_Operating_Activities
            # print Total_Cash_Flow_From_Operating_Activities
            # print Capital_Expenditures
            # print Investments
            # print Other_Cash_flows_from_Investing_Activities
            # print Total_Cash_Flows_From_Investing_Activities
            # print Dividends_Paid
            # print Sale_Purchase_of_Stock
            # print Net_Borrowings
            # print Other_Cash_Flows_from_Financing_Activities
            # print Total_Cash_Flows_From_Financing_Activities
            # print Change_In_Cash_and_Cash_Equivalents

            yield CashItem

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
