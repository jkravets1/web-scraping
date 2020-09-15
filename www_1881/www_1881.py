from builtins import print
import json
from lxml import etree
import requests
import base64
import pycountry
from datetime import date
import re
import dateparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class Handler:
    FETCHTYPE = ""
    NICKNAME = "1881.no"
    API_BASE_URL = ""
    base_url = "https://www.1881.no"
    browser_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    session = requests.Session()

    def Execute(self, searchquery,fetch_type,action,API_BASE_URL):
        self.FETCH_TYPE = fetch_type
        self.API_BASE_URL = API_BASE_URL

        if fetch_type is None or fetch_type=="":
            pages = self.getpages(searchquery)
            if pages is not None:
                data = self.parse_pages(pages)
            else:
                data = []
            dataset = data
        else:
            data = self.fetchByField(searchquery)
            dataset = data
        return dataset


    def fetchByField(self, link):
        link2 = base64.b64decode(link).decode('utf-8')
        root = self.getContent(link2)
        res = self.parse(root, link2)
        return res


    def getpages(self,searchquery):

        try:
            linkset = []

            chrome_options = Options()  
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_options=chrome_options)

            u = "https://www.1881.no/?query={}&type=person".format(searchquery.lower())
            driver.get(u)
            
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="contact-featured__list"]')))
            html = driver.page_source
            tree = etree.HTML(html)
            driver.quit()

            users = tree.xpath('//a[@data-tooltip="Vis mer informasjon"]/@href')
            for link in users:
                linkset.append(self.base_url+link)

            return linkset
        except:
            return None


    def parse_pages(self,pages):
        rlist = []
        i = 0
        for link in pages:
            i = i + 1
            if i == 12:
                break
            print(link)
            root= self.getContent(link)
            res = self.parse(root,link)
            rlist.append(res)

        return rlist


    def getContent(self, link):
        r = self.session.get(link, headers=self.browser_header).content
        return r


    def parse(self,html_,link):

        myparser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(html_,parser=myparser)

        person = {}

        name = tree.xpath('//h2[@class="details__name"]/text()')
        name = "".join(name).strip().encode('utf-8').decode('utf-8').strip()

        person["name"] = name

        if len(name.split(" ")) == 3:
            person["givenName"] = name.split(" ")[0].strip().replace(",", "")
            person["familyName"] = name.split(" ")[-1].strip().replace(",", "")
        elif len(name.split(" ")) == 2:
            person["givenName"] = name.split(" ")[0].strip().replace(",", "")
            person["familyName"] = name.split(" ")[-1].strip().replace(",", "")
        elif len(name.split(" ")) == 1:
            person["givenName"] = name.split(" ")[0].strip().replace(",", "")
        else:
            person["givenName"] = name.split(" ")[0].strip().replace(",", "")
            person["familyName"] = name.split(" ")[-1].strip().replace(",", "")

        try:
            phone = tree.xpath('//span[@class="button-call__number"]/text()')
            phone = "".join(phone).strip().encode('utf-8').decode('utf-8')
            person['phone'] = phone
        except:
            pass

        address = []
        a = {}
       
        try:
            location = tree.xpath('//p[@class="details__address"]/a//text()')
            
            streetAddress = "".join(location[0]).strip().encode('utf-8').decode('utf-8').replace(",","")
            
            city_post = "".join(location[1]).strip().encode('utf-8').decode('utf-8')
            try:
                postal = city_post.split(' ')[0].strip()
                a["postalCode"] = postal
            except:
                pass
            try:
                city = city_post.split(' ')[-1].strip()
                a["city"] = city
            except:
                pass

            a["@type"] = "PostalAddress"
            a["country"] = "Norway"
            a["streetAddress"] = streetAddress

            address.append(a)
            person["address"] = address
        except:
            pass
      
        person["sourceURL"] = self.base_url
        person["@context"] = "http://schema.org"
        person["@type"] = "Person"

        edd = {}
        if self.FETCHTYPE == "overview":
            key_name = 'overview'
            edd[key_name] = person
            edd['_links'] = self.links(link)

        else:
            key_name = 'overview'
            edd[key_name] = person
            edd['_links'] = self.links(link)

        return edd


    def getcountry_code(self, country):
        country = country.title()
        for con in pycountry.countries:
            if country.title() == con.name:
                return con.alpha_2
        return None


    def get_page(self, url):
        page = self.session.get(url,headers=self.browser_header)
        return page


    def format_date(self,text):
        if not isinstance(text, str):
            text = text.decode("utf-8")
        try:
            dv =  dateparser.parse(text)
            dv = dv.strftime("%Y-%m-%d")
            return dv
        except Exception as e:
            print(e)


    def links(self, link):
        data = {}
        link2 = base64.b64encode(link.encode('utf-8'))
        link2 = (link2.decode('utf-8'))
        data['overview'] = {"method": "GET",
                            "url": self.API_BASE_URL + "?source=" + self.NICKNAME + "&url=" + link2 + "&fields=overview"}
        return data
