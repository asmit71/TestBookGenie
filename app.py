from flask import Flask, render_template, url_for, request, redirect
#from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
#from scraper_api import ScraperAPIClient

app = Flask(__name__, template_folder='templates', static_folder="static")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index', methods = ['POST', 'GET'])
def home():
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/search/', methods=["POST", "GET"])
def search():
    return render_template("search.html")

@app.route('/result', methods=["GET",'POST'])
def result():
    ibn = request.form['ISBN']
    return render_template("results.html", ISBN = ibn)

@app.route('/book', methods=["GET",'POST'])
def book():
    ibn = request.form['ISBN']
    isbn = ibn

    url = "https://openlibrary.org/isbn/"+isbn+".json"
    
    response = urlopen(url)
    data_json = json.loads(response.read())

    data_json_str = json.dumps(data_json, indent=2)

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


    from scraper_api import ScraperAPIClient
    client = ScraperAPIClient('95a43ead4493ef31bbf4704a4bfaf81a')
    vBooks = client.get(url = valoreBooks).text
    amaz = client.get(url = amazon).text
    eB = client.get(url = ebay).text
    aBooks = client.get(url = abebooks).text
  
    start_urls =[client.scrapyGet(url = 'http://httpbin.org/ip')]
    def parse(self, response):
    # ...your parsing logic here
        yield scrapy.Request(client.scrapyGet(url = 'http://httpbin.org/ip'), self.parse)


    soup = BeautifulSoup(vBooks, 'lxml')

    first = soup.find_all('span', class_ = 'commaFormat')

    x = 1
    v_used = ""
    v_new = ""
    v_alternate = ""
    for points in first:
        if x == 1:
            v_new = str(points.text)
          
        elif x == 2:
            v_used = str(points.text)
          
        elif x == 3:
            v_alternate = str(points.text)
        x = x + 1

    soupAmazon = BeautifulSoup(amaz, 'lxml')

    amaz_first = soupAmazon.find_all('span', class_ = 'a-offscreen')

    a_rent = ""
    a_buy = ""

    x = 1
    for points in amaz_first:
       
        if x == 1:
            a_rent = points.text
        if x == 2:
            a_buy = points.text
        x = x + 1

   
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

    

    prices_list = {"ValoreBooks":str(float(v_used[1:])+3.95),"Amazon":a_rent[1:],"Ebay":ebay_price[1:],"AbeBooks":a_price[4:]}

    vb = prices_list["ValoreBooks"]
    amz = prices_list["Amazon"]
    eb = prices_list["Ebay"]
    ab = prices_list["AbeBooks"]
    return render_template("results.html", Valbook = vb, Amazon  = amz, ebay = eb, abebook = ab)

  

if __name__ == "__main__":
    app.run(debug=True)



