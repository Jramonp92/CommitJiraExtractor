# GitHub-Jira Integration Script

This script is a simple integration between GitHub and Jira. The script extracts the ticket number from commit messages for a specific repository and branch within a specified date range. Then it searches the Jira issues for the extracted ticket numbers and returns their summary and status.

## Github Action

This repository also contains a workflow to run the script in a github action via dispatcher, just adding the date range.

## Prerequisites
Python 3.6 or higher
requests, re, argparse, logging, jira modules. You can install them by running:
pip install requests re argparse logging jira

## Usage

python github_jira_checker.py --Repo <Repository name> --Branch_name <Branch name> --Github_token <Github token> --Start_date <Start Date> --End_date <End Date> --Jira_url <URL Jira> --Jira_username <Jira Username> --Jira_token <Jira token>

## Parameters

--Repo: Name of the repository.
--Branch_name: Name of the branch to check.
--Github_token: Github token.
--Start_date: Start date in YYYY-MM-DD format.
--End_date: End date in YYYY-MM-DD format.
--Jira_url: URL of the Jira instance.
--Jira_username: Username to authenticate to the Jira instance.
--Jira_token: Token to authenticate to the Jira instance.

## Example

python github_jira_integration.py --Repo my-repo --Branch_name develop --Github_token abc123 --Start_date 2022-01-01 --End_date 2022-01-31 --Jira_url https://my-jira-instance.com --Jira_username jdoe --Jira_token xyz789

## License
This project is licensed under the MIT License - see the LICENSE file for details.