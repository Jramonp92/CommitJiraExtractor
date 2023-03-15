import requests
import re
import argparse
from jira import JIRA
#TODO Add a logger

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Owner", help="Owner of the repository")
    parser.add_argument("--Repo", help="Repository name")
    parser.add_argument("--branch_name", help="Name of the branch to check")
    parser.add_argument("--Github_token", help="Github token")
    parser.add_argument("--Start_date", help="Start Date")
    parser.add_argument("--End_date", help="End Date")
    parser.add_argument("--Jira_url", help="URL Jira")
    parser.add_argument("--Jira_username", help="Jira Username")
    parser.add_argument("--Jira_token", help="Jira token")
    args = parser.parse_args()
    return args

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
    'server': Jira_url,
    'verify': False
    }

    jira = JIRA(options, basic_auth=(Jira_username, Jira_token))

    for ticket in tickets:
        try:
            issue = jira.issue(ticket)
            status = issue.fields.status.nameAUTO
            name = issue.fields.summary
            print(f"Ticket {ticket}: {name} - {status}")
        except Exception as e:
            print(f"I can't find the status of the ticket {ticket}: due to {e}")

def main():
    args = parse_arguments()

    tickets = ticket_number_extractor(args.Owner, args.Repo, args.Github_token, args.branch_name, args.Start_date, args.End_date)
    print(tickets)
    if(not tickets):
        jira_status(tickets)

if __name__== "__main__":
    main() 