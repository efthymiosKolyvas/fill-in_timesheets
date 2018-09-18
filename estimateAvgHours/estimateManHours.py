r"""
calculate avg. man hours per day to distribute the man effort (in hours) over a specific Calendar duration and for specific user exceptions

"""
import re, json, subprocess, calendar, os


class ManHoursBuilder(object):
    def __init__(self):
        self.month, self.year = 0, 1999

    def sumWorkDays(self, userArgs={}):
        """
        use a python Calendar iterator over the days of (month, year) to build the lines of the latex table one day at a time.
        the bulk production (for the entire month) uses predefined values for actionType & hoursLogged
        exceptions are handled separately via the userArgs
        """
        workdays = 0
        holidayList = self.locateHolidays()
        for day in calendar.Calendar().itermonthdays2(self.year, self.month):
            personalAbsence = (day[0] in userArgs) and (userArgs[day[0]][0] == 'OA')
            # isWorkday if:: not weekend AND not personalAbsence AND not holiday AND not month padding (by the Python iterator)
            isWorkday = (day[1]<5) and not(personalAbsence) and (day[0] not in holidayList) and day[0]
            if isWorkday: workdays += 1
        print 'this month has __{0:d}__ workdays'.format(workdays)
        return workdays

    def locateHolidays(self):
        """
        - load file w/ holidays and reshape it as a dictionary
        - locate public holidays for the given year & month
        """
        holiDict, keepDates = {}, []
        month = self.month - 1                  # self.month is from int(user-input)
        monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        with open('dictHolidays.json', 'r') as f:
            data = json.load(f)
            for dicct in data:
                holiDict[dicct.keys()[0]] = dicct.values()[0] # format is: {"year": {"Celebration": "Mon \d+"}}
        for datePair in (item.split() for item in holiDict[str(self.year)].values()):
            if re.search(monthNames[month], datePair[0]):
                keepDates.append(int(datePair[1]))
        return keepDates

    def locateExceptions(self, absenceDates):
        returnDict = {}
        with open('exceptions.json', 'r') as f:
            exceptDict = json.load(f)
        if str(self.year) in exceptDict.keys():
            exceptionPart = exceptDict[str(self.year)]
            if self.month in (int(months) for months in exceptionPart.keys()):
                monthIndex = exceptionPart['{0:02d}'.format(self.month)]
                for entry in monthIndex.keys():
                    returnDict[int(entry)] = [str(monthIndex[entry][0]), float(monthIndex[entry][1])] # the rest items in the list are devoted to comments/ justifications of exceptions
        for absence in range(absenceDates[0], absenceDates[1]):
            if absence not in returnDict.keys():
                returnDict[absence] = ['OA', 0.0]
        return returnDict
    
    def classInterface(self, absenceDates=(1,15), month=1, year=2000):
        """
        interface for the entire Class.
        userArgs are expected to be in the form of a dictionary w/ the day as the key and the parameters in a list:
        {int(day) : [str(actionType), hoursLogged]}
        """
        self.month, self.year = month, year
        userExceptions = self.locateExceptions(absenceDates) # format is: {3:['DI', 10], 21:['OT', 12]}
        return self.sumWorkDays(userArgs=userExceptions)




if __name__ == "__main__":
    hours4Division = 253
    totalDays, year = 0, 2009
    absenceDates = (1,1)
    for month in range(11,13):
        print 'MONTH:: {0:d}/{1:d}'.format(month, year)
        workdays = ManHoursBuilder().classInterface(absenceDates=absenceDates, month=month, year=year)
        totalDays += workdays
    print '--------------------------------------\n TOTAL Work DAYS for the period are: {0:d}\n --------------------------------------\n'.format(totalDays)
    print '--------------------------------------\n AVG. HOURS per day: {0:4.1f}\n --------------------------------------\n'.format(hours4Division/float(totalDays))

        
