# ADP-IT---NBS-Test

## Editor used for the project:
+ Sublime Text 3


## Step by Step

Started with creating the virtual environment and the project. I checked scrapy's official documentation so that I could use it.

```
C:\Users\bojid\My Python Stuff\ADP Test Web Scraping>pip install virtualenv
C:\Users\bojid\My Python Stuff\ADP Test Web Scraping>.\env\Scripts\activate
(env) C:\Users\bojid\My Python Stuff\ADP Test Web Scraping>pip install Scrapy
(env) C:\Users\bojid\My Python Stuff\ADP Test Web Scraping>scrapy startproject nbstest
(env) C:\Users\bojid\My Python Stuff\ADP Test Web Scraping>cd nbstest
```

Then I moved to writing the spider, and my first attempts returned only part of the html that was visible on the browser.
My spider ended up as the variation of nbstest.py

After relentless attempts and numerous google searches, I found out that the page is not static but loads JavaScript parts upon opening in the browser. So, I installed PlayWright in order to get to the html in the JS. I tried creating a very simple spider just to check if it works ok:

```python
import scrapy

class NbsSpider(scrapy.Spider):
	name = "pwnbs"

	def start_requests(self):
		yield scrapy.Request('https://nbs.sk/en/press/news-overview/', meta={'playwright': True})

	def parse(self, response):
		yield {
			'text': response.text
		}
```

It did NOT work ok. I mostly got the 'NotImplementedError'. Ultimatelly, I found this issue on GitHub github.com/scrapy-plugins/scrapy-playwright/issues/7 .

As to SQLite3, I researched it, installed it and tried to get it going. However, my json result file was empty due to the setback from above, so the conversion to sqlite did not happen either.
