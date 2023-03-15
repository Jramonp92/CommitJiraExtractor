#first Commit as a test 

import requests
import re


OWNER = "Jramonp92"
REPO = "CommitJiraExtractor"
YOUR_ACCESS_TOKEN = "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"
BRANCH = "main"

def github_ticket_extractor(Owner, Repo, Token, branch):
    ticket_numbers = []
    headers = {"Authorization": f"Bearer {Token}"}
    url = f"https://api.github.com/repos/{Owner}/{Repo}/commits?sha={branch}"

    response = requests.get(url, headers=headers)
    commits = response.json()

    for commit in commits:
        match = re.search(r"(?i)^[A-Z]+-\d+", commit["commit"]["message"])
        if match:
            ticket_numbers.append(match.group())

    return ticket_numbers

print(github_ticket_extractor(OWNER, REPO, YOUR_ACCESS_TOKEN, BRANCH))