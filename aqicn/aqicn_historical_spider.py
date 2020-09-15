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
import os.path

class Handler:

  def __init__(self):

    standartdate = datetime.now()
    date = standartdate.strftime('%Y-%m-%d')
    filename = 'aqicn_data{}.csv'.format(date)
    self.fieldnames = [
      'City',
      'Lat',
      'Lng',
      'Date',
      'PM2.5',
      'PM10',
      'O3',
      'NO2',
      'SO2',
      'CO'
    ]

    self.url_buffer = []
    with open("logger.json", "r") as f:
      self.url_buffer = json.load(f)

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
      if link not in self.url_buffer:       
        self.url_buffer.append(link)
        self.__getDetailInfo(driver, link, logger)

        with open("logger.json", "w") as f:
          f.write(json.dumps(self.url_buffer))


      # break

    # u = "http://aqicn.org/city/usa/delaware/killens/"
    # self.__getDetailInfo(driver, u, logger)

  def __getDetailInfo(self, driver, url, logger):

    try:
      driver.get(url)
      try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//td[@class="aqiwgt-table-aqiinfo"]')))
      except:
        return  

      time.sleep(5)
      element = driver.find_element_by_xpath('//div[@id="h1header5"]')
      actions = ActionChains(driver)
      actions.move_to_element(element).perform()
      try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//tr[@class="year-divider"]')))
      except:
        return
      time.sleep(10)

      driver.execute_script("window.scrollBy(0, 300);")

      elements = driver.find_elements_by_xpath('//center[@class="yearly-aqi"]/ul/li')
      print(len(elements))
      buf = {}
      for ele in elements:
        ele.click()
        time.sleep(5)
        # print('*INFO: label - ', ele.text)
        label = ele.text

        html = driver.page_source
        tree = etree.HTML(html)
        tags = tree.xpath('//div[@class="historical-yearly-data"]/table/tbody/tr[@style="display: table-row;" and not(@class)]')
        # print('* tags length - ', len(tags))
        for t in tags:
          _date = int(t.xpath('@key')[0])+1
          
          data_tags = t.xpath('./td[@class="squares"]/svg/text')
          # print('*INFO: date length - ',len(data_tags))
          for i, d in enumerate(data_tags):
            date = str(_date)+str(i+1).zfill(2)
            value = d.xpath('text()')[0]

            if date not in buf:
              buf[date] = {}
            buf[date][label] = value

            print('*INFO: label, date, value - ',label, date, d.xpath('text()')[0])
          
        try:
          city = re.search('\"city\"\:\{\"name\"\:\"(.*?)\"', html, re.M|re.S|re.I).group(1)
        except:
          city = ''
        # print(city)
        try:
          geo = re.search('\"geo\"\:\[\"(.*?)\"\,\"(.*?)\"\]', html, re.M|re.S|re.I)
          lat = geo.group(1)
          lng = geo.group(2)
        except:
          lat = ''
          lng = ''
        # print(lat, lng)      
        # break

        # test
        # with open("history.json", "r") as f:
        #   buf = json.load(f)

      for key, value in buf.items():
        value['City'] = city
        value['Lat'] = lat
        value['Lng'] = lng
        value['Date'] = key
        
        print('*INFO: ', key, value)
        
        file_exists = os.path.isfile("data/{}.csv".format(key))

        with open("data/{}.csv".format(key), "a") as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
          if not file_exists:
            writer.writeheader()
          writer.writerow(value)
          
    except:
      with open("error.txt", "a") as f:
        f.write(url)
        
    # return
    # time.sleep(500)

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

  # chrome_options = Options()  
  # chrome_options.add_argument("--headless")
  # chrome_options.add_argument("--window-size=1400,1080")
  # driver = webdriver.Chrome(chrome_options=chrome_options)

  # chrome_options.add_argument('--no-sandbox')
  # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'/usr/local/bin/chromedriver')

  driver = webdriver.Chrome()
  
  C = Handler()
  cont = C.main(driver, print_logger)

  driver.quit()

  log_scraping_end(print_logger)

