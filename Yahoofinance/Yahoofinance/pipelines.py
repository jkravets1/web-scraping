# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi 
from items import IncomestatementsItem,  BalancesheetItem, CashflowItem, AnalystsItem, MajorholdersItem, InsidertransactionsItem


settings = get_project_settings()

class YahoofinancePipeline(object):

    insert_Income_statement_sql = """insert into income_statement (%s) values ( %s )"""
    insert_Balance_sheet_sql = """insert into balance_sheet (%s) values ( %s )"""
    insert_Cash_flow_sql = """insert into cash_flow (%s) values ( %s )"""
    insert_analysts_sql = """insert into analysts (%s) values ( %s )"""
    insert_majorholders_sql = """insert into major_holders (%s) values ( %s )"""
    insert_insidertransactions_sql = """insert into insider_transactions (%s) values ( %s )"""
    
    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool    
 
    def __del__(self):    
        self.dbpool.close()    
 
    def process_item(self, item, spider):
    	
        if isinstance(item, IncomestatementsItem):
            self.insert_data(item,self.insert_Income_statement_sql)

        elif isinstance(item, BalancesheetItem):
            self.insert_data(item, self.insert_Balance_sheet_sql)

        elif isinstance(item, CashflowItem):
            self.insert_data(item, self.insert_Cash_flow_sql)

        elif isinstance(item, AnalystsItem):
            self.insert_data(item, self.insert_analysts_sql)

        elif isinstance(item, MajorholdersItem):
            self.insert_data(item, self.insert_majorholders_sql)

        elif isinstance(item, InsidertransactionsItem):
            self.insert_data(item, self.insert_insidertransactions_sql)

        return item    
 
    def insert_data(self, item, insert):    
        keys = item.fields.keys()    
        fields = u','.join(keys)    
        qm = u','.join([u'%s'] * len(keys))    
        sql = insert % (fields, qm)
        data = [item[k] for k in keys]
        return self.dbpool.runOperation(sql, data)