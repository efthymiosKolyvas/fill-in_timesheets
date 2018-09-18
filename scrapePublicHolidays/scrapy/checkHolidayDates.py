import json, re
"""
reshapeHolidays():: reshape the list of dictionaries exported by the spider to a dictionary of dictionaries
locateHolidays():: find the date of holiday, for a given year & month
"""

def reshapeHolidays():
    myDict = {}
    with open('dictHolidays.json', 'r') as f:
        data = json.load(f)
        for dicct in data:
            myDict[dicct.keys()[0]] = dicct.values()[0]
    return myDict
        
def locateHolidays(holiDict, year, month):
    keepDate = []
    month -= 1                  # month is expected as human input integer
    strNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for datePair in (item.split() for item in holiDict[str(year)].values()):
        if re.search(strNames[month], datePair[0]):
            keepDate.append(int(datePair[1]))
    return keepDate


if __name__ == "__main__":
    print reshapeHolidays()['2018']
    print locateHolidays(reshapeHolidays(), 2018, 1)
