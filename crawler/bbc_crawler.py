import pprint
from datetime import datetime
from crawler_preprocess.parser import returnCoolHTML
from mongo_driver.article import Article
from kafka_driver.kafka_producer import Producer
from mongo_driver.models import db

pp = pprint.PrettyPrinter(indent=4)
producer = Producer()


# Fetch articles from BBC News
def getBBCArticle():
    data = returnCoolHTML('http://feeds.bbci.co.uk/news/politics/rss.xml')

    for article in data.find_all("item"):
        url = article.find("guid").get_text()
        print(url)
        if not db['_article'].find({'url': url}).count():
            a = Article(article.find("guid").get_text())
            page = returnCoolHTML(article.find("guid").get_text())
            if page.find(class_="story-body__inner"):
                body = ""
                for paragraph in page.find(class_="story-body__inner").find_all("p"):
                    body += paragraph.get_text().strip() + " "
                a.body = body
            if page.find(class_="vxp-media__summary"):
                body = ""
                for paragraph in page.find(class_="vxp-media__summary").find_all("p"):
                    body += paragraph.get_text().strip() + " "
                a.body = body
            if page.find('h1'):
                a.title = page.find('h1').get_text()
            if page.find('div', {"class": "date"}):
                a.datePublished = datetime.fromtimestamp(float(page.find('div', {"class": "date"})["data-seconds"]))
            if page.find('li', {"class": "mini-info-list__item"}) and page.find('li', {
                "class": "mini-info-list__item"}) and page.find('li', {"class": "mini-info-list__item"}).find(
                'div').has_attr('data-seconds'):
                a.datePublished = datetime.fromtimestamp(
                    float(page.find('li', {"class": "mini-info-list__item"}).find('div')['data-seconds']))
            a.source = "BBC"
            print('Inserted 1 article in db\n')
            # producer.send_message("fakenew", json.dumps(a))
            print(a.to_map())
            out = db['_article'].insert_one(a.__dict__)


def fetchUSElectionBBC():
    for i in range(1, 3):
        print("==========================")
        print(i)
        data = returnCoolHTML(
            "https://www.bbc.co.uk/search?q=us+election&sa_f=search-product&filter=news&suggid=#page=" + str(i))
        for headline in data.find_all("h1"):
            print(headline.find("a")["href"])
        print(data.find(class_="pagination"))


if __name__ == "__main__":
    getBBCArticle()
