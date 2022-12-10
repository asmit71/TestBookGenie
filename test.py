from bs4 import BeautifulSoup

import time
from urllib.request import urlopen
import json
# store the URL in url as 
# parameter for urlopen

# isbn = "9780321543257"
isbn = "9780321885173"

url = "https://openlibrary.org/isbn/"+isbn+".json"
  
# store the response of URL
response = urlopen(url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())

# formats the data_json to be readable
data_json_str = json.dumps(data_json, indent=2)

#print(data_json_str)

title = data_json["title"]

title = title.replace("(", "")
title = title.replace(")", "")
title = title.replace("TM", "")
title = title.replace(" ", "-")
title = title.lower()

valoreBooks = "https://www.valorebooks.com/textbooks/"+title+"/"+isbn

amazon = "https://www.amazon.com/s?i=stripbooks&rh=p_66%3A"+isbn+"&s=relevanceexprank&Adv-Srch-Books-Submit.x=43&Adv-Srch-Books-Submit.y=10&unfiltered=1&ref=sr_adv_b"

ebay = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="+isbn+"&LH_PrefLoc=2&_oac=1&_sop=15"

abebooks = "https://www.abebooks.com/servlet/SearchResults?cm_sp=SearchF-_-merch-_-&isbn="+isbn+"&an=&tn="

print("Valorebook's link is: "+valoreBooks)
print("Amazon's link is: "+amazon)
print("Ebay's link is: "+ebay)
print("Abebooks' link is: "+abebooks)

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('95a43ead4493ef31bbf4704a4bfaf81a')
vBooks = client.get(url = valoreBooks).text
amaz = client.get(url = amazon).text
eB = client.get(url = ebay).text
aBooks = client.get(url = abebooks).text
#print(vBooks)
#print(amaz)
#print(eB)
#print(aBooks)
#print(bib)
# Scrapy users can simply replace the urls in their start_urls and parse function
# Note for Scrapy, you should not use DOWNLOAD_DELAY and
# RANDOMIZE_DOWNLOAD_DELAY, these will lower your concurrency and are not
# needed with our API
# ...other scrapy setup code
start_urls =[client.scrapyGet(url = 'http://httpbin.org/ip')]
def parse(self, response):
  # ...your parsing logic here
  yield scrapy.Request(client.scrapyGet(url = 'http://httpbin.org/ip'), self.parse)


# ValoreBooks webscrapping is here
#
#
soup = BeautifulSoup(vBooks, 'lxml')

first = soup.find_all('span', class_ = 'commaFormat')

#print(first)
#print(type(first))

x = 1
v_used = ""
v_new = ""
v_alternate = ""
for points in first:
    if x == 1:
        v_new = str(points.text)
        #new = new.replace("$", "")
        #new = float(new)+3.95
    elif x == 2:
        v_used = str(points.text)
        #used = used.replace("$", "")
        #used = float(used) + 3.95
    elif x == 3:
        v_alternate = str(points.text)
        #alternate = alternate.replace("$", "")
        #alternate = float(alternate)+3.95
    x = x + 1

print("The used book from ValoreBooks costs "+str(v_used)+" & 3.95 for shipping")
print("The new book from ValoreBooks costs "+str(v_new)+" & 3.95 for shipping")
print("The alternate book from ValoreBooks costs "+str(v_alternate)+" & 3.95 for shipping")


# Amazon webscrapping is here
#
#
soupAmazon = BeautifulSoup(amaz, 'lxml')

amaz_first = soupAmazon.find_all('span', class_ = 'a-offscreen')

a_rent = ""
a_buy = ""

x = 1
for points in amaz_first:
    #print("A price for book is: "+points.text)
    if x == 1:
        a_rent = points.text
    if x == 2:
        a_buy = points.text
    x = x + 1

print("Renting a book from Amazon costs: "+a_rent)
print("Buying a book from Amazon costs: "+a_buy)

# Ebay webscrapping is here
#
#
soupEbay = BeautifulSoup(eB, 'lxml')

eb_first = soupEbay.find_all('span', class_ = 's-item__price')

ebay_price = ""

x = 1
for points in eb_first:
    #print("A price for book is: "+points.text)
    if x == 2:
        ebay_price = points.text
    x = x + 1

print("Best price for Ebay is: "+ebay_price)

# AbeBooks webscrapping is here
#
#
soupAbeBooks = BeautifulSoup(aBooks, 'lxml')

ab_first = soupAbeBooks.find_all('p', class_ = 'item-price')

a_price = ""

x = 1
for points in ab_first:
    #print("A price for book is: "+points.text)
    if x == 1:
        a_price = points.text
    x = x + 1

print("Price for AbeBooks is: "+a_price)

prices_list = {"ValoreBooks":str(float(v_used[1:])+3.95),"Amazon":a_rent[1:],"Ebay":ebay_price[1:],"AbeBooks":a_price[4:]}

print("ValoreBooks price is: "+prices_list["ValoreBooks"])
print("Amazon price is: "+prices_list["Amazon"])
print("Ebay price is: "+prices_list["Ebay"])
print("AbeBooks price is: "+prices_list["AbeBooks"])