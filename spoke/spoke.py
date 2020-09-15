from builtins import print
import json
from lxml import etree
import requests
import base64
import pycountry
from datetime import date
import re
import dateparser


class Handler:
    FETCHTYPE = ""
    NICKNAME = "spoke.com"
    API_BASE_URL = ""
    base_url = "http://www.spoke.com"

    browser_header = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
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

            params = (
                ('q', searchquery),
                ('type', 'person'),
            )

            response = requests.get('http://www.spoke.com/search', headers=self.browser_header, params=params, verify=False)
            tree = etree.HTML(response.content)
            links = tree.xpath('//div[@class="sr-title sr-title-large"]/a/@href')

            for link in links:
                linkset.append(self.base_url+link)

            u = "http://www.spoke.com/search?page=2&q=john&type=person"
            response = requests.get(u, headers=self.browser_header, verify=False)
            tree = etree.HTML(response.content)
            links = tree.xpath('//div[@class="sr-title sr-title-large"]/a/@href')

            for link in links:
                linkset.append(self.base_url+link)
            
            return linkset

        except:
            return None


    def parse_pages(self,pages):
        rlist = []

        for link in pages:
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

        name = tree.xpath('//h1[@itemprop="name"]/text()')
        name = "".join(name).strip().encode('utf-8').decode('utf-8').strip()
        if "Jr." in name:
            person["honorificSuffix"] = "Jr."
        elif "Mr." in name:
            person["honorificPrefix"] = "Mr."

        name = name.split(',')[0]

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
            additionalName = []
            aliases = tree.xpath('//h3[@class="aliases"]/text()')[0].split(',')
            for a in aliases:
                additionalName.append(a.replace('\n', '').strip())
            if len(additionalName) > 0:
                person["additionalName"] = additionalName
        except:
            pass

        try:
            image = tree.xpath('//img[@class="img-profile"]/@src')[0]
            person['image'] = image
        except:
            pass
        try:
            job_ = tree.xpath('//span[@tooltip="job"]/following-sibling::text()')[0]
            job = job_.split(',')[0].strip()
            person["jobTitle"] = job
        except:
            pass

        address = []
        a = {}
        a["@type"] = "PostalAddress"
        a["country"] = "USA"
       
        try:
            county = tree.xpath('//span[@itemprop="addressLocality"]/text()')
            county = "".join(county).strip().encode('utf-8').decode('utf-8')
            if county != '':
                a["addressLocality"] = county
        except:
            county = ''

        try:
            region = tree.xpath('//span[@itemprop="addressRegion"]/text()')
            region = "".join(region).strip().encode('utf-8').decode('utf-8')
            if region != '':
                a["addressRegion"] = region
        except:
            region = ''

        address.append(a)

        if region != '':
            person["address"] = address
        else:
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
