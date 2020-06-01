from crawler.independent_crawler import fetchUSElectionIndependent
from crawler.guardian_crawler import getGuardianNews,db_name
from crawler.sky_crawler import getSkyNews, fetchUSElectionSkyNews
from crawler.bbc_crawler import fetchUSElectionBBC

if __name__ == "__main__":
    # getGuardianNews()
    # fetchUSElectionSkyNews()
    fetchUSElectionBBC()