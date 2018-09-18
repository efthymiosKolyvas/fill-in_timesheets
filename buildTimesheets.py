"""
fill Latex templates to produce timesheets in PDF (DVI)
------------------------------------------------------------------------------------------

template fileName: "latexTemplate"
parameters in fileName: "parametersJSON.json"
irregular workdays in fileName: "exceptions.json"   (these are workdays devoted to something less common - for example: Dissemination, Testing)
public holidays fileName: "dictHolidays.json"         (has been scraped from 'https://www.timeanddate.com/holidays/greece/'


see 'howToUse.md' file for further instructions

"""
import re, json, subprocess, calendar, os


class ManHoursBuilder(object):
    def __init__(self):
        self.month, self.year, self.monthHours = 0, 1999, 0.0

    def filterDays(self,actionType='RE', hoursPerDay=8.0,userArgs={}):
        """
        use a python Calendar iterator over the days of (month, year) to build the lines of the latex table one day at a time.
        the bulk production (for the entire month) uses predefined values for actionType & hoursPerDay
        exceptions are handled separately via the userArgs
        """
        calTable, hoursSum = [], 0.0
        holidaysList = self.locateHolidays()
        for day in calendar.Calendar().itermonthdays2(self.year, self.month):
            if day[0]:        # the iterator returns days from previous/ next months to produce complete weeks
                if (day[0] in holidaysList):
                    line = str(day[0]) + ' & ' + 'PH & - & 0.0\\'
                elif (day[1]>=5):
                    line = str(day[0]) + ' & ' + 'WE & - & 0.0\\'
                elif (userArgs and (day[0] in userArgs)):
                    if (userArgs[day[0]][0]=='OA'):
                        line = str(day[0]) + ' & ' + 'OA & - & 0.0\\'
                    else:
                        line = str(day[0]) + ' & ' + '- & ' + userArgs[day[0]][0] + ' & ' + '{0:3.1f}'.format(userArgs[day[0]][1]) + '\\'
                        hoursSum +=float(userArgs[day[0]][1])
                else:
                    line = str(day[0]) + ' & ' + '- & ' + actionType + ' & ' + '{0:3.1f}'.format(hoursPerDay) + '\\'
                    hoursSum +=float(hoursPerDay)
                calTable.append(line)
        self.monthHours = hoursSum
        return calTable

    def padTable(self, calTable):
        """
        simply pad the table-lines by filterDays with the preamble and ending, that latex requires
        """
        preamble = "\\begin{tabular}{lccr} \n Cal. Day & Reas. for Absence & Action Type & \\textbf{Hours} \\\ \n \\hline \n \\hline\\\ \n"
        ending = '\\hline\\\ \n \\textbf{Total:} & & & ' + '\\textbf{' + '{0:3.1f}'.format(self.monthHours) + '}\\\ \n \\hline \n\\end{tabular}\n'
        return preamble + ''.join(line.encode('string-escape')+'\n' for line in calTable) + ending

    def locateHolidays(self):
        """
        - load file w/ holidays and reshape it as a dictionary
        - locate public holidays for the given year & month
        """
        holiDict, keepDates = {}, []
        month = self.month - 1                  # self.month is given by the user
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
        print returnDict
        return returnDict

    def classInterface(self, absenceDates=(1,15), month=1, year=2000, hoursPerDay=6.0, actionType='RE'):
        """
        interface for the entire Class.
        userArgs are expected to be in the form of a dictionary w/ the day as the key and the parameters in a list:
        {int(day) : [str(actionType), hoursPerDay]}
        """
        self.month, self.year = month, year
        userExceptions = self.locateExceptions(absenceDates) # format is: {3:['DI', 10], 21:['OT', 12]}
        return self.padTable(self.filterDays(actionType=actionType, hoursPerDay=hoursPerDay, userArgs=userExceptions))


class LogLatex(object):
    """
    fill-in the latex template with the body table (from the above class) and print the result to a file (pdf)
    """
    def __init__(self):
        self.month, self.year = 1, 1999
        self.monthsList = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        self.personnelName = 'PAPADOPOULOS'

    def fillInLatexTemplate(self, paramFile='', bodyContent='', latexFile=''):
        """
        use a json file to store the parameters (keys are w/o the '$' signs)
        use a latex file to store the table (json has restrictions on type of data stored -- newlines)
        use a latex template; parameters are identified by '$' signs
        locate parameters in the template and if in the parameter file, substitute w/ correct value
        """
        with open(paramFile, 'r') as f1:
            parsDict = json.load(f1)
            parsDict['dateMMYYYY'] = '{0:s} {1:s}'.format(self.monthsList[self.month-1], str(self.year))
            self.personnelName, = re.findall('\w+$', parsDict['personnelName'])
        with open(latexFile, 'r') as f3:
            textForReview = f3.read()
        paramsForSub = re.findall('\$\w+\$', textForReview)
        for param in paramsForSub:
            unpadParam = re.sub('\$', '', param)
            if unpadParam in parsDict.keys():
                textForReview = re.sub(re.escape(param), parsDict[unpadParam], textForReview)
        textForReview = re.sub('\$body\$', bodyContent.encode('string-escape'), textForReview)
        return textForReview

    def producePDF(self, completeFile):
        try:
            os.makedirs('producedFiles/')
        except OSError as err:
            if err.errno==17:
                print 'directory exists, overwriting files'
            else:
                raise
        fileName = 'producedFiles/' + '{0:s}{1:02d}{2:04d}.tex'.format(self.personnelName, self.month, self.year)
        with open(fileName, 'w') as f:
            f.write(completeFile)
            print '--tex-- file written'
        bashCommand = 'pdflatex -output-directory=producedFiles/ -interaction=batchmode ' +  fileName
        print bashCommand
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if not(error):
            print '--pdf-- file produced\n'
            print output
        else:
            print error

    def classInterface(self, month, year, paramFile, bodyContent, latexFile):
        self.month, self.year = month, year
        finalText = self.fillInLatexTemplate(paramFile, bodyContent, latexFile)
        self.producePDF(finalText)



if __name__ == "__main__":
    totalHours = 0.0
    year = 2018
    absenceDates = (1, 1)
    hoursPerDay=6.0
    for month in range(12,13):
        print 'printing timesheet for {0:d}/{1:d}'.format(month, year)
        builder = ManHoursBuilder()
        latexBody = builder.classInterface(absenceDates=absenceDates, month=month, year=year, hoursPerDay=hoursPerDay, actionType='RE')
        totalHours += builder.monthHours
        latexLogger = LogLatex()
        latexLogger.classInterface(month=month, year=year, paramFile='parametersJSON.json', bodyContent=latexBody, latexFile='latexTemplate.tex')
    print '--------------------------------------\n TOTAL Man Hours for the period are: {0:f}\n --------------------------------------\n'.format(totalHours)
