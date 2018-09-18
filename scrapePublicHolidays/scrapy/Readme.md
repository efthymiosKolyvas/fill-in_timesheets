# Scraping Public Holidays

## Project Description

Use a simple Scrapy crawler to build a dictionary of Public Holidays for a range of years for a particular country from the ['time and date' webpage](https://www.timeanddate.com/holidays/).

## Dependencies

The website uses js to render the table of holidays and celebrations. The crawler uses `Splash` to render the website.

Uses:

- [Scrapy](https://scrapy.org/)
- [Splash](https://github.com/scrapinghub/splash) and
- [Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash)

Instructions for the XPath expression by the [Scrapy tutorial/ selectors](https://docs.scrapy.org/en/latest/topics/selectors.html#topics-selectors)
