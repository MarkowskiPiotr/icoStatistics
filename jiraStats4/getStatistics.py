import configparser
import getopt
import os
import sys
import csv
from datetime import date, timedelta, datetime

import getFiltersResults
import sendEmail

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration.ini'))

defaultNoOfDays = int(config['LOGS']['defaultNoOfDays'])
defaultLogsLocation = config['LOGS']['defaultLogsLocation']

argv = sys.argv[1:]

if len(argv) > 0:
    try:
        opts, args = getopt.getopt(argv, 'd:')
        if len(opts) > 1:
            print('usage: getStatistics.py -d <number_of_days>')
        else:
            ticketDatesRange = int(opts[0][1])
    except getopt.GetoptError:
        print('usage: getStatistics.py -d <number_of_days>')
        sys.exit(2)
else:
    ticketDatesRange = defaultNoOfDays

ticketProjects = ['CORINT', 'IGW4000', 'IGW5KINT', "'MLGTINT', 'MLGTFON'", "'MLLTINT', 'MLLTFON'",
                      'SPYDINT', 'I488271INT']
ticketStatuses = ['To do', 'Ready for Work', 'In Progress', 'On Hold', 'Ready for testing', 'In Testing', 'Feedback']
ticketPriority = ['Blocker', 'High', 'Normal', 'Low', 'Not set']

projectsStatisticsHeader = ['project', 'date', 'new bugs', 'total open bugs', 'priority', '', '', '', '', '', 'Status', '', '', '', '', '', '','','Tickets waiting for tests','', '', '', '', '', '', 'Tickets currently being tested', '', '', '', '', '']
projectsStatisticsCSV=[]
projectsStatisticsCSV.append(projectsStatisticsHeader)
temp=['', '', '', '']
for tPriority in ticketPriority:
    temp.append(tPriority)
temp.append('')
for tStatus in ticketStatuses:
    temp.append(tStatus)
temp.append('')
temp.append('Total')
for tPriority in ticketPriority:
    temp.append(tPriority)
temp.append('')
temp.append('Total')
for tPriority in ticketPriority:
    temp.append(tPriority)
projectsStatisticsCSV.append(temp)

todayDate = date.today()

currentTime = datetime.now().strftime("%H_%M")

firstDate = todayDate - timedelta(days=ticketDatesRange - 1)

filterDates = []

for datesIterator in range(ticketDatesRange):
    statsDate = firstDate + timedelta(days=datesIterator)
    if statsDate.weekday() < 5:
        filterDates.append(statsDate)

for filterProject in ticketProjects:
    for filterDateIterator in (filterDates):
        temp = []
        temp.append(filterProject)
        temp.append(filterDateIterator.strftime( '%Y/%m/%d'))
        previousDay = filterDateIterator - timedelta(days=1)
        stats = getFiltersResults.generateStatistics(filterProject,ticketStatuses,ticketPriority,filterDateIterator.strftime( '%Y/%m/%d'), previousDay.strftime( '%Y/%m/%d'))
        for statsIterator in stats:
            temp.append(statsIterator)
        projectsStatisticsCSV.append(temp)

fileName = str(todayDate) + "_" + currentTime + "_statsCSV.csv"
dirPath = defaultLogsLocation
resultFile = open(os.path.join(dirPath, fileName), "x")

with resultFile as f:
    write = csv.writer(f)
    write.writerows(projectsStatisticsCSV)
f.close()