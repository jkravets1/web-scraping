# -*- coding: utf-8 -*-
import re, time
import csv, json
from datetime import datetime, timedelta
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from math import cos, asin, sqrt
import os.path

class Handler:

  def __init__(self):

    self.R = 6371000 #radius of the Earth in m
    standartdate = datetime.now()
    date = standartdate.strftime('%Y%m%d')
    self.filename = '{}.csv'.format(date)
    self.Fields = ['City', 'Lat', 'Lng', 'Date', 'PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']
    self.today = datetime.today().strftime('%Y-%m-%d')
    self.fieldnames = ['Zip', 'City', 'State', 'Latitude', 'Longitude', 'Date', 'PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']

  def main(self, driver, logger):
    """
    Main function
    """ 

    url = "https://aqicn.org/city/all#USA"
    driver.get(url)

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//a[@id="USA"]')))

    html = driver.page_source
    tree = etree.HTML(html)
    try:
      links = tree.xpath('//a[contains(@href, "http://aqicn.org/city/usa/")]/@href')
    except:
      links = 0
    print("* links: ",len(links))
    for i, link in enumerate(links):
      logger.info('*INFO Processing url: {}, {}'.format(i+1, link))
      self.__getDetailInfo(driver, link, logger)
      # if i > 10:
        # break

    driver.quit()

    sample_data = self.get_sample()    
    with open("us-zip-code-latitude-and-longitude.csv", encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        print('-----------------')
        value = min(sample_data, key=lambda d: self.distance(float(row["Latitude"]), float(row["Longitude"]), float(d["Lat"]), float(d["Lng"])))
        # value = sorted(sample_data, key= lambda d: self.distance(float(d["Lng"]), float(d["Lat"]), float(row["Longitude"]), float(row["Latitude"])))[0]
        buf = value.copy()
        del buf['City']
        del buf['Lat']
        del buf['Lng']
        
        buf['Zip'] = row['Zip']
        buf['City'] = row['City']
        buf['State'] = row['State']
        buf['Latitude'] = row['Latitude']
        buf['Longitude'] = row['Longitude']
        
        file_exists = os.path.isfile("all/{}".format(self.filename))
        
        print('*INFO: ', buf)
        with open("all/{}".format(self.filename), "a") as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
          if not file_exists:
            writer.writeheader()
          writer.writerow(buf)

  def __getDetailInfo(self, driver, url, logger):
    buf = {}
    driver.get(url)
    try:
      WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//td[@class="aqiwgt-table-aqiinfo"]')))
    except:
      return  
    time.sleep(1)
    html = driver.page_source
    tree = etree.HTML(html)

    try:
      _date = re.search("try\{checkWidgetUpdateTime\((.*?)\,\'", html, re.M|re.S|re.I).group(1)
      date = datetime.fromtimestamp(int(_date)).strftime('%Y-%m-%d')
    except:
      date = ''
    print("* date: ",date)
    
    if date != self.today:
      return

    try:
      city = re.search('\"city\"\:\{\"name\"\:\"(.*?)\"', html, re.M|re.S|re.I).group(1)
    except:
      city = ''
    
    try:
      geo = re.search('\"geo\"\:\[\"(.*?)\"\,\"(.*?)\"\]', html, re.M|re.S|re.I)
      lat = geo.group(1)
      lng = geo.group(2)
    except:
      lat = ''
      lng = ''

    try:
      cur_pm25 = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_pm25"]/text()')[0].strip()
    except:
      cur_pm25 = ''

    if cur_pm25 == '-':
      cur_pm25 = ''

    try:
      cur_pm10 = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_pm10"]/text()')[0].strip()
    except:
      cur_pm10 = ''

    if cur_pm10 == '-':
      cur_pm10 = ''

    try:
      cur_o3 = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_o3"]/text()')[0].strip()
    except:
      cur_o3 = ''

    if cur_o3 == '-':
      cur_o3 = ''

    try:
      cur_no2 = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_no2"]/text()')[0].strip()
    except:
      cur_no2 = ''

    if cur_no2 == '-':
      cur_no2 = ''

    try:
      cur_so2 = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_so2"]/text()')[0].strip()
    except:
      cur_so2 = ''

    if cur_so2 == '-':
      cur_so2 = ''      

    try:
      cur_co = tree.xpath('//div[@id="citydivmain"]//td[@id="cur_co"]/text()')[0].strip()
    except:
      cur_co = ''
    
    if cur_co == '-':
      cur_co = ''

    if cur_pm25=='' and cur_pm10=='' and cur_o3=='' and cur_no2=='' and cur_so2=='' and cur_co=='':
      print(' ----- Blank! ----- ')
      return
    # print("* date: ",date)
    # print("* city: ",city)
    # print("* lat, lng: ", lat, lng)
    # print("* cur_pm25: ",cur_pm25)
    # print("* cur_pm10: ",cur_pm10)
    # print("* cur_o3: ",cur_o3)
    # print("* cur_no2: ",cur_no2)
    # print("* cur_so2: ",cur_so2)
    # print("* cur_co: ",cur_co)

    buf['City'] = city
    buf['Lat'] = lat
    buf['Lng'] = lng
    buf['Date'] = date
    buf['PM2.5'] = cur_pm25
    buf['PM10'] = cur_pm10
    buf['O3'] = cur_o3
    buf['NO2'] = cur_no2
    buf['SO2'] = cur_so2
    buf['CO'] = cur_co

    file_exists = os.path.isfile("sample_data/{}".format(self.filename))
    
    print('*INFO: ', buf)
    with open("sample_data/{}".format(self.filename), "a") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.Fields)
      if not file_exists:
        writer.writeheader()
      writer.writerow(buf)

  # def distance(self, lon1, lat1, lon2, lat2):
  #   x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
  #   y = (lat2 - lat1)
  #   return self.R * sqrt( x*x + y*y )

  def distance(self, lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))
    
  def get_sample(self):
    result = []
    with open('sample_data/{}'.format(self.filename), encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row['Lat'] == '' or row['Lng'] == '':
          continue
        result.append(row)

    return result  

class MockLogger:
  @staticmethod
  def info(message):
    print(message)

  
def log_scraping_start(company, logger):
  start_time = datetime.now()
  logger.info('* Starting: {}'.format(company))
  logger.info('* Processing starting at: {} ------------------------------'.format(start_time))
  return start_time


def log_scraping_end(logger):
  end_time = datetime.now()
  logger.info('* Processing ended at: {} ------------------------------'.format(end_time))
  return end_time


if __name__ == "__main__":
  
  print_logger = MockLogger()

  log_scraping_start("Aqicn", print_logger)

  driver = webdriver.Chrome()
  
  C = Handler()
  cont = C.main(driver, print_logger)

  log_scraping_end(print_logger)