import configparser
import os
from jira import JIRA

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration.ini'))

jiraAddress = config['JIRA']['jiraAddress']
userName = config['JIRA']['userName']
userAPIToken = config['JIRA']['userAPIToken']

options = {
    'server': jiraAddress
}

jira = JIRA(options, basic_auth=(userName, userAPIToken))

ticketClosedStatuses = "Done, Closed, \"Won't Do\",Duplicate"
ticketOpenStatuses = "\"To Do\", Backlog, \"In Progress\", \"TODO QA\", \"Waiting for Code Review\""


# projectsStatistics = {}


def generateStatistics(filterProject, ticketStatuses, ticketPriority, ticketDate, dayBefore):
    projectsStatistics = {'newBugs': {}, 'notClosedBugs': {}, 'notClosedBugsPriority': {},
                          'notClosedBugsStatus': {},
                          'ticketsInQA': {}, 'ticketsInQAPriority': {}}
    projectsStatistics['newBugs'] = getNewBugs(filterProject, ticketDate, dayBefore)
    projectsStatistics['notClosedBugs'] = getAllBugs(filterProject, ticketClosedStatuses, ticketDate)
    projectsStatistics['notClosedBugsPriority'] = getBugsByPriority(filterProject, ticketPriority, ticketDate)
    projectsStatistics['notClosedBugsStatus'] = getBugsByStatus(filterProject, ticketStatuses, ticketDate)
    projectsStatistics['ticketsInQA'] = getTicketsByPriority(filterProject, ticketDate)
    projectsStatistics['ticketsInQAPriority'] = getTicketsByStatus(filterProject, ticketPriority, ticketDate)

    return projectsStatistics


def getNewBugs(filterProject, ticketDate, dayBefore):
    jiraFilter = "project in (" + filterProject + ") AND type = Bug AND createdDate >= '" \
                 + dayBefore + "' AND createdDate <= '" + ticketDate + "'"
    jiraResult = jira.search_issues(jiraFilter, maxResults=1)
    # print(jiraResult)
    return jiraResult.total


def getAllBugs(filterProject, ticketClosedStatuses, ticketDate):
    jiraFilter = "project in (" + filterProject + ") AND type = Bug AND status was not in (" \
                 + ticketClosedStatuses + ") on ('" + ticketDate + " 06:00')"
    jiraResult = jira.search_issues(jiraFilter, maxResults=1)
    return jiraResult.total


def getBugsByPriority(filterProject, ticketPriority, ticketDate):
    projectsStatistics = {}
    for filterPriority in ticketPriority:
        jiraFilter = "project in (" + filterProject + ") AND type in (Bug) AND status was not in (" \
                     + ticketClosedStatuses + ") on ('" + ticketDate + " 06:00') " + "AND priority = '" + filterPriority + "'"
        jiraResult = jira.search_issues(jiraFilter, maxResults=1)
        projectsStatistics[filterPriority] = jiraResult.total
    return projectsStatistics


def getBugsByStatus(filterProject, ticketStatuses, ticketDate):
    projectsStatistics = {}
    for filterStatus in ticketStatuses:
        jiraFilter = "project in (" + filterProject + ") AND type in (Bug) AND status was '" + filterStatus + "'" \
                     + " on ('" + ticketDate + " 06:00')"
        jiraResult = jira.search_issues(jiraFilter, maxResults=1)
        projectsStatistics[filterStatus] = jiraResult.total
    return projectsStatistics


def getTicketsByPriority(filterProject, ticketDate):
    projectsStatistics = {}
    for filterStatus in ("Ready for testing", "In testing"):
        jiraFilter = "project in (" + filterProject + ") AND type !=Bug AND status was '" + filterStatus + "' on ('" \
                     + ticketDate + " 06:00')"
        jiraResult = jira.search_issues(jiraFilter, maxResults=1)
        projectsStatistics[filterStatus] = jiraResult.total
    return projectsStatistics


def getTicketsByStatus(filterProject, ticketPriority, ticketDate):
    projectsStatistics = {}
    for filterStatus in ("Ready for testing", "In testing"):
        projectsStatistics[filterStatus] = {}
        for filterPriority in ticketPriority:
            jiraFilter = "project in (" + filterProject \
                         + ") AND type !=Bug AND status was in ('" + filterStatus + "') on ('" + ticketDate + " 06:00') AND priority = '" \
                         + filterPriority + "'"
            jiraResult = jira.search_issues(jiraFilter, maxResults=1)
            projectsStatistics[filterStatus][filterPriority] = jiraResult.total
    return projectsStatistics
