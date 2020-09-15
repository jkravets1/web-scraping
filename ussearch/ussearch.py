from builtins import print
import json
from lxml import etree
import requests
import base64
import pycountry
from datetime import date


class Handler:

    FETCHTYPE = ""
    NICKNAME = "ussearch.com"
    API_BASE_URL = ""
    base_url = "https://www.ussearch.com"
    browser_header = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    session = requests.Session()


    def Execute(self, query, fetch_type, action, API_BASE_URL):

        self.FETCHTYPE = fetch_type
        self.API_BASE_URL = API_BASE_URL

        if fetch_type is None or fetch_type == "":
            data = self.parse(query)
        else:
            link2 = base64.b64decode(query).decode('utf-8')
            param = link2.split('/')[-1]
            data = self.parse(param)

        return data


    def parse(self, query):

        if self.FETCHTYPE == "overview":
            overview_param = query.split("?")[0].strip()
            query = query.split("?")[-1].strip()

        returndata = []

        first_name = query.split(' ')[0]
        last_name = query.split(' ')[1]

        u = 'https://www.ussearch.com/search/people/{}/~/{}'.format(first_name, last_name)

        try:
            r = requests.get(u, headers=self.browser_header)
            tree = etree.HTML(r.content)

            cnt = 0
            users = tree.xpath('//tr[contains(@class, "uss-teaser-results-matches")]')

            for row in users:

                person = {}
                address = {}

                name = row.xpath('.//a[@class="uss-first-name-result"]/text()')
                name = "".join(name).strip().encode('utf-8').decode('utf-8').strip()
                if name == "":
                    continue
                cnt += 1

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

                additionalName = []
                additionalNames = row.xpath('.//span[@class="aliases"]/text()')
                for a in additionalNames:
                    additionalName.append(a)
                if len(additionalName) > 0:
                    person['additionalName'] = additionalName

                address = []
                locations = row.xpath('.//td[@class="memberTeaserCityState"]/span/text()')
                for l in locations:
                    if l != '':
                        r = l.split(',')[-1].strip()
                        localty = l.split(',')[0].strip()
                        a = {}
                        a["@type"] = "PostalAddress"
                        a["addressLocality"] = localty
                        a["addressRegion"] = r
                        a["country"] = "USA"

                        address.append(a)

                if len(address) > 0:
                    person["address"] = address
                else:
                    pass

                worksFor = []
                works = row.xpath('.//td[@class="memberTeaserCompanies"]/span/text()')
                for w in works:
                    if w != '':
                        a = {}
                        a["@type"] = "Organization"
                        a["name"] = w

                        worksFor.append(a)

                if len(worksFor) > 0:
                    person["worksFor"] = worksFor
                else:
                    pass
        
                alumniOf = []
                studies = row.xpath('.//td[@class="memberTeaserEducation"]/span/text()')
                for s in studies:
                    if s != '':
                        a = {}
                        a["@type"] = "CollegeOrUniversity"
                        a["name"] = s

                        alumniOf.append(a)

                if len(alumniOf) > 0:
                    person["alumniOf"] = alumniOf
                else:
                    pass


                link = self.base_url

                param = row.xpath('.//a[@class="uss-js-more-link"]/@href')
                param = "".join(param).strip().encode('utf-8').decode('utf-8').strip()
                param = param.split('/')[-1]

                person["sourceURL"] = link
                person["@context"] = "http://schema.org"
                person["@type"] = "Person"

                link = link +"/"+param+"?"+query

                edd = {}
                if self.FETCHTYPE == "overview":

                    if param == overview_param:
                        key_name = 'overview'
                        edd[key_name] = person
                        edd['_links'] = self.links(link)

                        returndata.append(edd)

                else:
                    key_name = 'overview'
                    edd[key_name] = person
                    edd['_links'] = self.links(link)

                    returndata.append(edd)

                if cnt > 10:
                    break
        except:
            pass        

        return returndata


    def getcountry_code(self, country):
        country = country.title()
        for con in pycountry.countries:
            if country.title() == con.name:
                return con.alpha_2
        return None


    def get_page(self, url):
        page = self.session.get(url,headers=self.browser_header)
        return page


    def links(self, link):
        data = {}
        link2 = base64.b64encode(link.encode('utf-8'))
        link2 = (link2.decode('utf-8'))
        data['overview'] = {"method": "GET",
                            "url": self.API_BASE_URL + "?source=" + self.NICKNAME + "&url=" + link2 + "&fields=overview"}
        return data
