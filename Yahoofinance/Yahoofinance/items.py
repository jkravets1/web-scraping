# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IncomestatementsItem(scrapy.Item):

    Symbol = scrapy.Field()
    Period = scrapy.Field()
    Date = scrapy.Field()
    Total_Revenue = scrapy.Field()
    Cost_of_Revenue = scrapy.Field()
    Gross_Profit = scrapy.Field()
    Research_Development = scrapy.Field()
    Selling_General_and_Administrative = scrapy.Field()
    Non_Recurring = scrapy.Field()
    Others = scrapy.Field()
    Total_Operating_Expenses = scrapy.Field()
    Operating_Income_or_Loss = scrapy.Field()
    Total_Other_IncomeExpenses_Net = scrapy.Field()
    Earnings_Before_Interest_and_Taxes = scrapy.Field()
    Interest_Expense = scrapy.Field()
    Income_Before_Tax = scrapy.Field()
    Income_Tax_Expense = scrapy.Field()
    Minority_Interest = scrapy.Field()
    Net_Income_From_Continuing_Ops = scrapy.Field()
    Discontinued_Operations = scrapy.Field()
    Extraordinary_Items = scrapy.Field()
    Effect_Of_Accounting_Changes = scrapy.Field()
    Other_Items = scrapy.Field()
    Net_Income = scrapy.Field()
    Preferred_Stock_And_Other_Adjustments = scrapy.Field()
    Net_Income_Applicable_To_Common_Shares = scrapy.Field()

class BalancesheetItem(scrapy.Item):

    Symbol = scrapy.Field()
    Period = scrapy.Field()    
    Date = scrapy.Field()
    Cash_And_Cash_Equivalents = scrapy.Field()
    Short_Term_Investments = scrapy.Field()
    Net_Receivables = scrapy.Field()
    Inventory = scrapy.Field()
    Other_Current_Assets = scrapy.Field()
    Total_Current_Assets = scrapy.Field()
    Long_Term_Investments = scrapy.Field()
    Property_Plant_and_Equipment = scrapy.Field()
    Goodwill = scrapy.Field()
    Intangible_Assets = scrapy.Field()
    Accumulated_Amortization = scrapy.Field()
    Other_Assets = scrapy.Field()
    Deferred_Long_Term_Asset_Charges = scrapy.Field()
    Total_Assets = scrapy.Field()
    Accounts_Payable = scrapy.Field()
    ShortCurrent_Long_Term_Debt = scrapy.Field()
    Other_Current_Liabilities = scrapy.Field()
    Total_Current_Liabilities = scrapy.Field()
    Long_Term_Debt = scrapy.Field()
    Other_Liabilities = scrapy.Field()
    Deferred_Long_Term_Liability_Charges = scrapy.Field()
    Minority_Interest = scrapy.Field()
    Negative_Goodwill = scrapy.Field()
    Total_Liabilities = scrapy.Field()
    Misc_Stocks_Options_Warrants = scrapy.Field()
    Redeemable_Preferred_Stock = scrapy.Field()
    Preferred_Stock = scrapy.Field()
    Common_Stock = scrapy.Field()
    Retained_Earnings = scrapy.Field()
    Treasury_Stock = scrapy.Field()
    Capital_Surplus = scrapy.Field()
    Other_Stockholder_Equity = scrapy.Field()
    Total_Stockholder_Equity = scrapy.Field()
    Net_Tangible_Assets = scrapy.Field()

class CashflowItem(scrapy.Item):

    Symbol = scrapy.Field()
    Period = scrapy.Field()    
    Date = scrapy.Field()
    Net_Income = scrapy.Field()
    Depreciation = scrapy.Field()
    Adjustments_To_Net_Income = scrapy.Field()
    Changes_In_Accounts_Receivables = scrapy.Field()
    Changes_In_Liabilities = scrapy.Field()
    Changes_In_Inventories = scrapy.Field()
    Changes_In_Other_Operating_Activities = scrapy.Field()
    Total_Cash_Flow_From_Operating_Activities = scrapy.Field()
    Capital_Expenditures = scrapy.Field()
    Investments = scrapy.Field()
    Other_Cash_flows_from_Investing_Activities = scrapy.Field()
    Total_Cash_Flows_From_Investing_Activities = scrapy.Field()
    Dividends_Paid = scrapy.Field()
    Sale_Purchase_of_Stock = scrapy.Field()
    Net_Borrowings = scrapy.Field()
    Other_Cash_Flows_from_Financing_Activities = scrapy.Field()
    Total_Cash_Flows_From_Financing_Activities = scrapy.Field()
    Effect_Of_Exchange_Rate_Changes = scrapy.Field()
    Change_In_Cash_and_Cash_Equivalents = scrapy.Field()


class AnalystsItem(scrapy.Item):

    Symbol = scrapy.Field()
    Date = scrapy.Field()
    Earnings_Estimate_No_of_Analysts = scrapy.Field()
    Earnings_Estimate_Avg_Estimate = scrapy.Field()
    Earnings_Estimate_Low_Estimate = scrapy.Field()
    Earnings_Estimate_High_Estimate = scrapy.Field()
    Earnings_Estimate_Year_Ago_EPS = scrapy.Field()
    Revenue_Estimate_No_of_Analysts = scrapy.Field()
    Revenue_Estimate_Avg_Estimate = scrapy.Field()
    Revenue_Estimate_Low_Estimate = scrapy.Field()
    Revenue_Estimate_High_Estimate = scrapy.Field()
    Revenue_Estimate_Year_Ago_EPS = scrapy.Field()    
    Revenue_Estimate_Sales_Growth = scrapy.Field()
    Earnings_History_Date = scrapy.Field()
    EPS_Est = scrapy.Field()    
    EPS_Actual = scrapy.Field()    
    Difference = scrapy.Field()    
    Surprise = scrapy.Field()
    Current_Estimate = scrapy.Field()
    Days_7_Ago = scrapy.Field()
    Days_30_Ago = scrapy.Field()
    Days_60_Ago = scrapy.Field()
    Days_90_Ago = scrapy.Field()
    Up_Last_7_Days = scrapy.Field()
    Up_Last_30_Days = scrapy.Field()
    Down_Last_30_Days = scrapy.Field()
    Down_Last_90_Days = scrapy.Field()


class MajorholdersItem(scrapy.Item):

	Symbol = scrapy.Field()
	Percent_of_Shares_Held_by_All_Insider = scrapy.Field()
	Percent_of_Shares_Held_by_Institutions = scrapy.Field()
	Percent_of_Float_Held_by_Institutions = scrapy.Field()
	Number_of_Institutions_Holding_Shares = scrapy.Field()

class InsidertransactionsItem(scrapy.Item):

	Symbol = scrapy.Field()
	Name = scrapy.Field()
	Relation = scrapy.Field()
	Transaction = scrapy.Field()
	Type = scrapy.Field()
	Value = scrapy.Field()
	Date = scrapy.Field()
	Shares = scrapy.Field()

# CREATE TABLE balance_sheet (
#     Symbol VARCHAR(100),
#     Period VARCHAR(100),    
#     Date VARCHAR(100),
#     Cash_And_Cash_Equivalents VARCHAR(100),
#     Short_Term_Investments VARCHAR(100),
#     Net_Receivables VARCHAR(100),
#     Inventory VARCHAR(100),
#     Other_Current_Assets VARCHAR(100),
#     Total_Current_Assets VARCHAR(100),
#     Long_Term_Investments VARCHAR(100),
#     Property_Plant_and_Equipment VARCHAR(100),
#     Goodwill VARCHAR(100),
#     Intangible_Assets VARCHAR(100),
#     Accumulated_Amortization VARCHAR(100),
#     Other_Assets VARCHAR(100),
#     Deferred_Long_Term_Asset_Charges VARCHAR(100),
#     Total_Assets VARCHAR(100),
#     Accounts_Payable VARCHAR(100),
#     ShortCurrent_Long_Term_Debt VARCHAR(100),
#     Other_Current_Liabilities VARCHAR(100),
#     Total_Current_Liabilities VARCHAR(100),
#     Long_Term_Debt VARCHAR(100),
#     Other_Liabilities VARCHAR(100),
#     Deferred_Long_Term_Liability_Charges VARCHAR(100),
#     Minority_Interest VARCHAR(100),
#     Negative_Goodwill VARCHAR(100),
#     Total_Liabilities VARCHAR(100),
#     Misc_Stocks_Options_Warrants VARCHAR(100),
#     Redeemable_Preferred_Stock VARCHAR(100),
#     Preferred_Stock VARCHAR(100),
#     Common_Stock VARCHAR(100),
#     Retained_Earnings VARCHAR(100),
#     Treasury_Stock VARCHAR(100),
#     Capital_Surplus VARCHAR(100),
#     Other_Stockholder_Equity VARCHAR(100),
#     Total_Stockholder_Equity VARCHAR(100),
#     Net_Tangible_Assets VARCHAR(100)
# );