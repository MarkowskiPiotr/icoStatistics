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
ticketOpenStatuses = "\"To Do\", Backlog, \"In Progress\", \"TODO QA\", \"Waiting for Code Review\", \"In Testing\", " \
                     "\"Ready for testing\", \"Feedback\", \"On Hold\" ,\"Ready for work\""


def getMonthlyStatistics(filterProject, ticketDate):
    jiraFilter = \
        "project in (" + filterProject + ") AND type = bug AND status was in (" + ticketOpenStatuses + ")  on ('" \
        + ticketDate + " 06:00')"
    jiraResult = jira.search_issues(jiraFilter, maxResults=0)

    return jiraResult.total
