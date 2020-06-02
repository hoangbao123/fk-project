from crawler.independent_crawler import fetchUSElectionIndependent, getIndependentNews
from crawler.guardian_crawler import getGuardianNews,db_name
from crawler.sky_crawler import getSkyNews, fetchUSElectionSkyNews
from crawler.bbc_crawler import fetchUSElectionBBC, getBBCArticle
from crawler.indian_crawler import get_cnn_news
from concurrent.futures import ThreadPoolExecutor

main_pool = ThreadPoolExecutor(max_workers=5)

if __name__ == "__main__":
    main_pool.submit(get_cnn_news)
    main_pool.submit(getBBCArticle)
    main_pool.submit(getSkyNews)
    main_pool.submit(getIndependentNews)
    main_pool.submit(getGuardianNews)
    # get_cnn_news()
    # getBBCArticle()
    # getGuardianNews()
    # getSkyNews()
    # getIndependentNews()
    # getGuardianNews()
    # fetchUSElectionSkyNews()
    # fetchUSElectionBBC()
