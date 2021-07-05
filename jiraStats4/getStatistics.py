import configparser
import getopt
import json
import os
import sys
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

# ticketProjects = ["'MLGTINT', 'MLGTFON'"]
# ticketProjects = ['CAMINT', 'CORINT', 'IGW4000', "'MLGTINT', 'MLGTFON'", "'MLLTINT', 'MLLTFON'", 'I520XTQA', 'SPYDINT', 'I488271INT' ]
ticketProjects = ['CAMINT', 'CORINT', 'IGW4000', "'MLGTINT', 'MLGTFON'", "'MLLTINT', 'MLLTFON'", "'I520XTQA', 'I520XTW'",
                  'SPYDINT', 'I488271INT']
ticketStatuses = ['To do', 'Ready for Work', 'In Progress', 'On Hold', 'Ready for testing', 'In Testing', 'Feedback']
ticketPriority = ['Blocker', 'High', 'Normal', 'Low', 'Not set']

projectsStatistics = {}
todayDate = date.today()

currentTime = datetime.now().strftime("%H_%M")

firstDate = todayDate - timedelta(days=ticketDatesRange - 1)

filterDates = []

for datesIterator in range(ticketDatesRange):
    filterDates.append(firstDate + timedelta(days=datesIterator))

for filterProject in ticketProjects:
    projectsStatistics[filterProject] = {}
    for filterDateIterator in (filterDates):
        # jsonProjectsStats[str(filterDateIterator)][filterProject]={}
        previousDay = filterDateIterator - timedelta(days=1)
        projectsStatistics[filterProject][str(filterDateIterator)] = getFiltersResults.generateStatistics(filterProject,
                                                                                                          ticketStatuses,
                                                                                                          ticketPriority,
                                                                                                          filterDateIterator.strftime(
                                                                                                              '%Y/%m/%d'),
                                                                                                          previousDay.strftime(
                                                                                                              '%Y/%m/%d'))

jsonResults = json.dumps(projectsStatistics, sort_keys=False, indent=4)
fileName = str(todayDate) + "_" + currentTime + "_results.json"
dirPath = defaultLogsLocation
resultFile = open(os.path.join(dirPath, fileName), "x")
resultFile.write(jsonResults)
resultFile.close()

sendEmail.sendEmail(jsonResults)
