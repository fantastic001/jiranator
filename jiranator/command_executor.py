from asyncore import read
from copy import copy
from distutils.util import convert_path
from email.policy import default
import os
from typing import Callable
from xml.etree.ElementTree import ElementTree
import pandas

from pandas.core.arrays.categorical import contains
from datetime import datetime, timedelta
import matplotlib.pyplot as plt 
import jira 

# create jira client from configuration file given in environment variable
# JIRA_CONFIG_FILE
config = open(os.environ.get('JIRA_CONFIG_FILE', 'config.json'))
jira_client = jira.JIRA.from_json(config)


class CommandExecutor:
    def jql(self, jql: str, max_results: int = 1000):
        """
        Executes a JQL query and returns the results as a pandas DataFrame.
        """
        issues = jira_client.search_issues(jql, maxResults=max_results)
        return pandas.DataFrame([self._issue_to_dict(issue) for issue in issues])
    
    def _issue_to_dict(self, issue):
        """
        Converts a JIRA issue to a dictionary.
        """
        d = copy(issue.raw['fields'])
        d['key'] = issue.key
        d['id'] = issue.id
        d['url'] = issue.permalink()
        d['project'] = issue.fields.project.name
        d['issuetype'] = issue.fields.issuetype.name
        d['status'] = issue.fields.status.name
        d['reporter'] = issue.fields.reporter.displayName
        d['assignee'] = issue.fields.assignee.displayName
        d['created'] = issue.fields.created
        d['updated'] = issue.fields.updated
        d['resolved'] = issue.fields.resolutiondate
        d['description'] = issue.fields.description
        d['summary'] = issue.fields.summary
        d['priority'] = issue.fields.priority.name
        d['labels'] = issue.fields.labels
        return d
    
    def get_description(self, key: str):
        """
        Returns the description of an issue.
        """
        issue = jira_client.issue(key)
        return issue.fields.description.replace('\r\n', '\n')
    def get_summary(self, key: str):
        """
        Returns the summary of an issue.
        """
        issue = jira_client.issue(key)
        return issue.fields.summary
    def get_status(self, key: str):
        """
        Returns the status of an issue.
        """
        issue = jira_client.issue(key)
        return issue.fields.status.name 
    def get_assignee(self, key: str):
        """
        Returns the assignee of an issue.
        """
        issue = jira_client.issue(key)
        return issue.fields.assignee.displayName
    def get_reporter(self, key: str):
        """
        Returns the reporter of an issue.
        """
        issue = jira_client.issue(key)
        return issue.fields.reporter.displayName


