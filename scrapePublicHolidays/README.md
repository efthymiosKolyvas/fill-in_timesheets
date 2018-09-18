# Scrape calendar data

## Project Description & Dependencies

The calendar days for the public holidays in Greece (stationary and not), over a range of years, have been scraped from [timeanddate](https://www.timeanddate.com/holidays/greece).  
The project has used two tools, for reasons of comparison in the implementation:

- Scrapy with Splash (to render the js-enabled webpage)
- Selenium (with the Chrome driver, under python 3.7)

The '.json' file ('dictHolidays.json') has been built by the Scrapy tool.


## Description of files

1. __Scrapy and Splash__

A small spider has been written (placed in the directory scrapePublicHolidays/spiders), 'wrapped' in the Scrapy framework. Loads different webpages (corresponding to calendar data from different years) and parses the content via XPath to identify cells corresponding to the tag 'Public holiday'. This information is placed in a dictionary (written to file by Scrapy) to be read by the `buildTimesheets.py` module in the parent directory.  


2. __Selenium__

Performs the same actions as Scrapy does. The only difference is that Selenium does not return text nodes; this means that js code has been used (`execute_script()`) to perform minimal text selection.  
The example has been built for reasons of comparison with Scrapy and for operation across different platforms.
