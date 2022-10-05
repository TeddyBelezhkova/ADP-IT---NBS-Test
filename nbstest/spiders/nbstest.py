import scrapy
from pydispatch import dispatcher
from scrapy import signals
import json
import time  #waiting time so that we don't bombard it with requests
import sqlite3

class NbsSpider(scrapy.Spider):
    name = "nbs"
    start_urls = ['https://nbs.sk/en/press/news-overview/']
    counter = 0  #create an incrementer to put things in the dictionary later on
    results = {}
        
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        for article in response.css("div.archive-results > a.archive-results__item > a::attr('href')"):
            # print(response.css("div.nbs-content").get()) ---> getting results only from this tag, but it does NOT have the tags to the articles (though they exist in the dev tool)!!!
            time.sleep(2)
            yield scrapy.Request(url=article.get(), callback=self.parseInnerPage)


        # --------Going to next pages----------
        # Ultimatelly, I would use this for checking the pages, but there are no actual links in the pagination tag!

        # nextPage = response.css("ul.pagination::attr('href')").get()
        # if nextPage is not None:
        #     time.sleep(2)
        #     response.follow(nextPage, self.parse)



    def parseInnerPage(self, response):

        article_headline = print(response.css("h1::text").get())
        article_text = print(response.css("div.kt-inside-inner-col > p::text").get())
        # articleText = articleText.replace(u"\xa0", "")
        # articleText = articleText.strip()

        self.results[self.counter] = {
            "articleHeadline": article_headline,
            "articleText": article_text
        }

        self.counter = self.counter + 1

    def spider_closed(self, spider):
        # second param is the instance of the spider about to be closed
        with open('results.json', 'w') as fp:
            json.dump(self.results, fp)


### -------- Attempt to create a table with SQLite3 to be filled with the data from the json file --------------------------
    
    conn = sqlite3.connect('nbsarticles_db.db')
    cursor = conn.cursor()
    cursor.executescript("""
            CREATE TABLE [IF NOT EXISTS] articles (
                article_id INTEGER PRIMARY KEY,
                headline TEXT,
                article_body TEXT 
            )
        """)