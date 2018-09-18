"""
scrape the time and dates of public holidays with Selenium.

Difference with Scrapy is that Selenium does not allow to reference text nodes;
the same action is performed with the alternative to execute js script (similar to the browser's web console)

(uses python 3.7 - difference is in the use of `print()``)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.set_headless(True)
path_to_chromedriver = "..../chromedriver"  # if not already in PATH
driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=chrome_options)

fileDictionary = {}
for year in range(2004,2019):
        url = 'https://www.timeanddate.com/holidays/greece/' + str(year)
        driver.get(url)

        tr_list = driver.find_elements_by_xpath("//tr[contains(.,'Public holiday')]")
        holidaysDict = {}
        for holiday_table_row in tr_list:
            calDate = driver.execute_script('return arguments[0].firstChild.textContent;', holiday_table_row)
            holName = driver.execute_script('return arguments[0].childNodes[2].textContent;', holiday_table_row)
            holidaysDict[holName] = calDate

        fileDictionary[year] = holidaysDict


print('------------------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------------------')
print(fileDictionary)
