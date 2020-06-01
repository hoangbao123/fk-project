from datetime import datetime
from mongo_driver.article import Article
from mongo_driver.models import db
from crawler_preprocess.parser import returnCoolHTML


def fetchUSElectionIndependent():
    for i in range(280, 631):
        print("==========================")
        print(i)
        data = returnCoolHTML("https://www.independent.co.uk/search/site/us%2520election?page=" + str(i))
        for headline in data.find_all("h2"):
            if headline.find("a"):
                url = headline.find("a")["href"]
                print(url)
                if not db['_past_article'].find({'url': url}).count():
                    a = Article(url)
                    page = returnCoolHTML(url)
                    if page.find('time') and page.find('time').has_attr('data-microtimes'):
                        a.datePublished = datetime.fromtimestamp(
                            float(eval(page.find('time')['data-microtimes'])['published'][0:10]))
                        print(a.datePublished)
                    if page.find('h1') and len(str(page.find('h1'))) <= 200:  # , {"class":"headline article-width"}):
                        a.title = page.find('h1').get_text().strip()
                        print(a.title)
                    if page.find(class_="text-wrapper"):
                        body = ""
                        for paragraph in page.find(class_="text-wrapper").find_all('p'):
                            if paragraph.parent.name == "div":
                                body += paragraph.get_text().strip() + " "
                        a.body = body
                    a.source = "The Independent"
                    out = db['_past_article'].insert_one(a.__dict__)
                    print(out)

