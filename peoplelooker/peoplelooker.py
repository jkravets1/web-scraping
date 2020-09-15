from builtins import print
import json, re
from lxml import etree
import requests
import base64
import pycountry
from datetime import date


class Handler:

    FETCHTYPE = ""
    NICKNAME = "peoplelooker.com"
    API_BASE_URL = ""
    base_url = "https://www.peoplelooker.com"
    browser_header = {
        'authority': 'www.beenverified.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
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
            overview_param = query.split("q=?")[0].strip()
            query = query.split("q=?")[-1].strip()


        if len(query.split(" ")) == 3:
            first_name = query.split(" ")[0]
            last_name = query.split(" ")[-1]
        elif len(query.split(" ")) == 2:
            first_name = query.split(" ")[0]
            last_name = query.split(" ")[-1]
        elif len(query.split(" ")) == 1:
            first_name = query.split(" ")[0]
            last_name = ""
        else:
            first_name = query.split(" ")[0]
            last_name = query.split(" ")[-1]

        returndata = []

        try:
            u = 'https://www.beenverified.com/hk/teaser/'
            print(first_name)
            print(last_name)

            params = (
                ('exporttype', 'jsonp'),
                ('rc', '100'),
                ('fn', first_name),
                ('ln', last_name),
                ('state', ''),
                ('city', ''),
                ('age', ''),
                ('mn', ''),
                ('callback', 'parseResults')
            )

            r = requests.get(u, headers=self.browser_header, params=params)
            json_txt = re.search('parseResults\((.*?)\)\;', r.text, re.I|re.M|re.S).group(1)
            json_data = json.loads(json_txt)
            users = json_data["response"]["Records"]["Record"]

            cnt = 0

            for row in users:

                person = {}
                address = {}

                person["givenName"] = row["Names"]["Name"][0]["First"]
                person["familyName"] = row["Names"]["Name"][0]["Last"]
                mid_name = row["Names"]["Name"][0]["Middle"]
                try:
                    if mid_name == '':
                        name = "{} {}".format(person["givenName"], person["familyName"])
                    else:
                        name = "{} {} {}".format(person["givenName"], mid_name, person["familyName"])
                except:
                    name = ""

                if name == "":
                    continue
                cnt += 1

                person["name"] = name

                address = []
                locations = row["Addresses"]["Address"]

                for l in locations:
                    a = {}
                    a["@type"] = "PostalAddress"
                    a["addressLocality"] = l["City"]
                    a["addressRegion"] = l["State"]
                    a["country"] = "USA"

                    address.append(a)

                if len(address) > 0:
                    person["address"] = address
                else:
                    pass
                try:
                    year = row["DOBs"]["Item"]["DOB"]["Year"]
                    month = row["DOBs"]["Item"]["DOB"]["Month"]
                    day = row["DOBs"]["Item"]["DOB"]["Day"]
                    birthDate = "{}-{}-{}".format(year, month, day)
                    person["birthDate"] = birthDate
                except:
                    pass

                link = self.base_url

                person["sourceURL"] = link
                person["@context"] = "http://schema.org"
                person["@type"] = "Person"

                param = row["bvid"]

                link = link +"/"+param+"q=?"+query

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
