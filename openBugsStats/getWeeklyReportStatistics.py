import configparser
import csv
import os
import sys
from datetime import date, timedelta, datetime
import getopt

import getFiltersResults

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration.ini'))

defaultNoOfDays = int(config['LOGS']['defaultNoOfDays'])
defaultLogsLocation = config['LOGS']['defaultLogsLocation']

argv = sys.argv[1:]

if len(argv) > 0:
    try:
        opts, args = getopt.getopt(argv, 'd:')
        if len(opts) > 1:
            print('usage: getWeeklyReportStatistics.py -d <number_of_days>')
        else:
            ticketDatesRange = int(opts[0][1])
    except getopt.GetoptError:
        print('usage: getWeeklyReportStatistics.py -d <number_of_days>')
        sys.exit(2)
else:
    ticketDatesRange = defaultNoOfDays

# ticketProjects = ['IA']
ticketProjects = ['CAMINT', 'CORINT', 'IGW4000', 'IGW5KINT', "'MLGTINT', 'MLGTFON'", "'MLLTINT', 'MLLTFON'",
                   "'I520XTQA', 'I520XTW'", 'I488271INT', 'IA']


todayDate = date.today()
currentTime = datetime.now().strftime("%H_%M")

monthlyProjectsStatistics = []
firstDate = todayDate - timedelta(days=ticketDatesRange)

filterDates = ['']
for datesIterator in range(ticketDatesRange + 1):
    filterDates.append((firstDate + timedelta(days=datesIterator)).strftime('%Y/%m/%d'))

openBugs = []
openBugs.append(filterDates)

for filterProject in ticketProjects:
    monthlyProjectsStatistics = [filterProject]
    for filterDateIterator in (filterDates[1:]):
        monthlyProjectsStatistics.append(getFiltersResults.getMonthlyStatistics(filterProject, filterDateIterator))
    openBugs.append(monthlyProjectsStatistics)

fileName = defaultLogsLocation + str(todayDate) + "_" + currentTime + "_monthlyOpenTicketsStats.csv"

fileName = str(todayDate) + "_" + currentTime + "_monthlyOpenTicketsStats.csv"
dirPath = defaultLogsLocation
resultFile = open(os.path.join(dirPath, fileName), "x")



with resultFile as f:
    write = csv.writer(f)
    write.writerows(openBugs)
f.close()
