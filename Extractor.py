import requests
import re
from jira import JIRA


##Add args parser#
OWNER = "Jramonp92"
REPO = "CommitJiraExtractor"
YOUR_ACCESS_TOKEN = "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"
BRANCH_NAME = "main"
DATE_INIT = "2022-03-01"
DATE_FINISH = "2023-05-05"
JIRA_BASE_URL = ""
JIRA_USERNAME = ""
JIRA_TOKEN = ""


def ticket_number_extractor(Owner, Repo, Token, branch, init, finish):
    ticket_numbers = []
    headers = {"Authorization": f"Token{Token}"}
    url = f"https://api.github.com/repos/{Owner}/{Repo}/commits?sha={branch}&since={init}T00:00:00Z&until={finish}T23:59:59Z"

    response = requests.get(url, headers=headers)
    commits = response.json()

    if(commits):
        for commit in commits:
            match = re.search(r"(?i)^[A-Z]+-\d+", commit["commit"]["message"])
            if match:
                ticket_numbers.append(match.group())
    else:
        print("No commits for these dates")

    return ticket_numbers

def jira_status(tickets):
    options = {
    'server': JIRA_BASE_URL,
    'verify': False
    }

    jira = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))

    for ticket in tickets:
        try:
            issue = jira.issue(ticket)
            status = issue.fields.status.nameAUTO
            name = issue.fields.summary
            print(f"Ticket {ticket}: {name} - {status}")
        except Exception as e:
            print(f"I can't find the status of the ticket {ticket}: due to {e}")

def main():
    tickets = ticket_number_extractor(OWNER, REPO, YOUR_ACCESS_TOKEN, BRANCH_NAME, DATE_INIT, DATE_FINISH)
    if(tickets):
        jira_status(tickets)

if __name__== "__main__":
    main()