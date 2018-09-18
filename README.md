# Fill-in timesheets 

## Project Description

The main structure of the document is given by a Latex template. The template describes the location of the elements (tables, text, signatures, etc.) in the page and provides the static (persistent) content of the document. Text that is expected to change appears as a parameter and substituted during the build phase.  

The Latex template forms a monthly table (timesheet), recording the:

1. Calendar Day (day of the month)
2. Reason for absence (if any, like for example 'Public holiday')
3. Type of activity (according to the definitions given in the final document/ template)
4. Hours per day, that the identified personnel was involved in

The table is filled-in row-by-row, constructed by data from (a) a python calendar iterator, (b) information stored in a '.json' file (scraped data from the ['time and date' webpage](https://www.timeanddate.com/holidays/)), (c) user-supplied data in the form of a `exceptions.json` file and (d) an additional parameters' file (`parametersJSON.json`) for parameters that vary less frequently (project name).  

A 'row prototype' is used as the default value for each row of the table, unless an exception is identified in the 'json' file `exceptions.json`.  
Once the table is formed, it is substituted in the original Latex template (parametrized by the variable 'body'). All of the parameters in the template are located by a Regular Expression (re) search for the token '$'.  


### Dependencies

Requires:  
- Python 2.7
- Pdflatex
- the function `producePDF()`compiles and stores the file to disk (interaction with the filesystem assumes Ubuntu)  

### Description of files:

 - `dictHolidays.json`: a list of dictionaries produced by the 'Scraping Public Holidays' project. "Year" is the key to a dictionary of {"Celebration": "Month Calendar-Day"} pairs.
 - `exceptions.json`: a dictionary of dictionaries (uses "Year", "Month" & "Cal. Day" as the key). A list with ["Type of Action", "Man Hours" & "justification/ comment"] items corresponds to each calendar day
 - `parametersJSON.json`: a simple dictionary the Latex parameters
 - `latexTemplate`: the Latex template


## Code structure

The project is divided in two Classes: (a) the 'Builder' of the `ManHoursTable` and  (b) the 'Logger'/ Creator of the Latex document. The `main function` produces the timesheets one per month, for a range of months (including a range of "1"). The month-index (1,2, etc.) refers also to the month of the year: 1-Jan, 2-Feb, etc..

The user-defined parameters (provided via the _main function_) are:

- year
- month(s) of the year (access via the `range()`)  
- absence days (a range of calendar days to be logged as absence)
- the Man-Hours to log for each workday

### Contents

Each of the two Classes uses a `classInterface` module for interaction.  

- The `ManHoursBuilder` uses:
  - `filterDays`: builds the table line by line, assessing conditions for whether we refer to a workday or not; the sum of hours logged in the month is given as a Class variable [type: float]  
    __Returns:__ (a) the latex table (without the preamble) [type: string]
  - `locateExceptions`: reads the user-defined 'exceptions' file and produces a dictionary of lists with items the reason of exception ('non-prototype') for each exception-day;  
    __Returns:__ a dictionary of lists, using the calendar day as the key and the 'Action Type' or 'Absence' and the Man Hours to log as the first and second elements of the list respectively.
  - `locateHolidays`: reformats the 'badly' shaped json file produced by the Scrapy-Project: `scrapePublicHolidays` and produces a list of dates for the Public Holidays of the given year and month in Greece;  
    __Returns:__ a list of calendar dates in the month/year of reference
  - `padTable`: appends the required text to the Man-Hours table to build a 'proper' Latex table (takes care of the encoding for the escape characters)  
    __Returns:__ a string: the table formatted in Latex
- The `LogLatex` uses:
  - `fillInLatexTemplate`: locates the parameters in the latex template and makes the substitution;  
    __Returns:__ a string: the Latex text to be written to the '.tex' file
  - `producePDF`: creates a directory (if needed) to place the latex files; compile the '.tex' file to produce the '.pdf'  
    __Returns:__ void (prints a success or error message)

