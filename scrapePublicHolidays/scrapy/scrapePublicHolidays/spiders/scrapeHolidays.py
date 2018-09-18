import scrapy, re
from scrapy_splash import SplashRequest
r"""
Description:: used to build a json file w/ the Public Holidays listed in the baseUrl website for the years given in the range.
                  the dictionary lists the holidays by year: and w/ the holidayName as the key for the holidayDate

HowToRun:: the website is js-enabled, you will need:

- an open Splash instance
- run the command: `scrapy crawl getHolidays -o holidaysFile.json` to produce the file
"""


class ScrapeHolidays(scrapy.Spider):
    name = 'getHolidays'
    holidays = {}

    def start_requests(self):
        baseUrl = 'https://www.timeanddate.com/holidays/greece/'
        for year in range(2004,2020):
            url = baseUrl + str(year)
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        holidaysDict, holidays = {}, {}
        year = re.findall('\d+$', response.url)[0]
        for holiday in response.xpath('//tr[contains(., "Public holiday")]'):
            holidayName, holidayDate = holiday.xpath('.//a/text()').extract()[0], holiday.xpath('.//text()').extract()[0]
            holidaysDict[holidayName] = holidayDate
        holidays[str(year)] = holidaysDict
        yield holidays
