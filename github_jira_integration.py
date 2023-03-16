import requests
import re
import argparse
import logging
from jira import JIRA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Repo", help="Repository name")
    parser.add_argument("--Branch_name", help="Name of the branch to check")
    parser.add_argument("--Github_token", help="Github token")
    parser.add_argument("--Start_date", help="Start Date")
    parser.add_argument("--End_date", help="End Date")
    parser.add_argument("--Jira_url", help="URL Jira")
    parser.add_argument("--Jira_username", help="Jira Username")
    parser.add_argument("--Jira_token", help="Jira token")
    args = parser.parse_args()
    return args

def ticket_number_extractor(Repo, Token, branch, init, finish):
    ticket_numbers = []
    headers = {"Authorization": f"Token{Token}"}
    url = f"https://api.github.com/repos/{Repo}/commits?sha={branch}&since={init}T00:00:00Z&until={finish}T23:59:59Z"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commits = response.json()
        if(commits):
            for commit in commits:
                match = re.search(r"(?i)^[A-Z]+-\d+", commit["commit"]["message"])
                if match:
                    ticket_numbers.append(match.group())
                else:
                    url = commit['url'].replace('api.','').replace('commits','commit').replace('repos/','')
                    logger.info(f"No Jira ticket found in commit message for {url}")
        else:
            logger.info("No commits for these dates.")
    except requests.exceptions.HTTPError as http_error:
        logger.exception(f"Unable to get commits from {url} due to {http_error}")
    except Exception as e:
        logger.exception(f"An error occurred while getting commits from {url} due to {e}")
        
    return ticket_numbers

def jira_status(tickets, Jira_url, Jira_username, Jira_token):
    options = {
        'server': Jira_url,
        'verify': False
    }
    jira = JIRA(options, basic_auth=(Jira_username, Jira_token))
    issues = jira.search_issues(f"issuekey in ({','.join(tickets)})")
    
    for issue in issues:
        try:
            logger.info(f"Ticket {issue.key}: {issue.fields.summary} - {issue.fields.status.name}")
        except Exception as e:
            logger.exception(f"I can't find the status of the ticket {issue} due to {e}")

def main():
    args = parse_arguments()
    tickets = ticket_number_extractor(args.Repo, args.Github_token, args.Branch_name, args.Start_date, args.End_date)
    logger.info(tickets)
    
    if(tickets):
        jira_status(tickets, args.Jira_url, args.Jira_username, args.Jira_token)

if __name__== "__main__":
    main()