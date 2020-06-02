import json
import pprint

import dateutil.parser

from crawler_preprocess.parser import returnCoolHTML, returnCoolXML
from kafka_driver.kafka_producer import Producer
from mongo_driver.article import Article
from mongo_driver.models import db

pp = pprint.PrettyPrinter(indent=4)
db_name = "mydb"

producer = Producer()


# Fetch articles from Sky News
def getSkyNews():
    data = returnCoolXML('http://feeds.skynews.com/feeds/rss/politics')
    for article in data.find_all("item"):
        url = article.find("link").get_text()
        print(url)
        if not db[db_name].find({'url': url}).count():
            a = Article(article.find("link").get_text())
            page = returnCoolHTML(article.find("link").get_text())
            if page.find(class_="sdc-news-article-header__last-updated__timestamp"):
                a.datePublished = print(dateutil.parser.parse(
                    page.find(class_="sdc-news-article-header__last-updated__timestamp")['datetime']))
            # print(a.datePublished)
            if page.find(class_="sdc-news-article-header__headline "):
                a.title = page.find(class_="sdc-news-article-header__headline ")['aria-label']  # .get_text().strip()
            # print(a.title)
            body = ""
            if page.find(class_="sdc-news-story-article__intro"):
                body += page.find(class_="sdc-news-story-article__intro").get_text().strip() + " "
            if page.find(class_="sdc-news-story-article__body"):
                for paragraph in page.find(class_="sdc-news-story-article__body").find_all('p'):
                    body += paragraph.get_text().strip() + " "
                a.body = body
            a.source = "Sky News"
            producer.send_message("baohn", json.dumps(a.to_map()))
            out = db[db_name].insert_one(a.__dict__)
            print('Inserted 1 article in db\n')


# One time fetching for US Election from Sky News
def fetchUSElectionSkyNews():
    for i in range(1, 51):
        print("==========================")
        print(i)
        data = returnCoolHTML("https://news.sky.com/search?q=us+election&sortby=date&page=" + str(i))
        for headline in data.find_all("h2"):
            if headline.find("a"):
                url = headline.find("a")["href"]
                print(url)
                if not db[db_name].find({'url': url}).count():
                    a = Article(url)
                    page = returnCoolHTML(url)
                    if page.find(class_="sdc-news-article-header__last-updated__timestamp"):
                        a.datePublished = dateutil.parser.parse(
                            page.find(class_="sdc-news-article-header__last-updated__timestamp")['datetime'])
                        print("date", a.datePublished)
                    if page.find(class_="sdc-news-article-header__headline "):
                        a.title = page.find(class_="sdc-news-article-header__headline ").find(
                            "span").get_text()  # ['aria-label']#.get_text().strip()
                        print("title", a.title)
                    body = ""
                    if page.find(class_="sdc-news-story-article__intro"):
                        body += page.find(class_="sdc-news-story-article__intro").get_text().strip() + " "
                    if page.find(class_="sdc-news-story-article__body"):
                        for paragraph in page.find(class_="sdc-news-story-article__body").find_all('p'):
                            body += paragraph.get_text().strip() + " "
                        a.body = body
                    a.source = "Sky News"
                    producer.send_message("baohn", json.dumps(a.to_map()))
                    out = db[db_name].insert_one(a.__dict__)
                    print(out)


if __name__ == "__main__":
    getSkyNews()
