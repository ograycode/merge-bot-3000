"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import datetime
from pull_requests.models import PullRequest, GitHubUtils


class PullRequestTests(TestCase):
    def test_get_time_to_merge_success(self):
        time = 'merge on 12/15/2013 at 12:00'
        p = PullRequest()
        date = p.get_time_to_merge(time)
        expected_date = datetime(2013, 12, 15, 12, 00)
        self.assertEqual(date, expected_date)

    def test_get_time_to_merge_fail(self):
        time = 'abc'
        p = PullRequest()
        date = p.get_time_to_merge(time)
        self.assertEqual(date, None)

class TestGitHubUtils(TestCase):
    url = 'https://api.github.com/repos/ograycode/ograycode.github.io/pulls/2'
    g = GitHubUtils()

    def test_get_user(self):
        self.assertEqual(self.g.get_user(self.url), 'ograycode')

    def test_get_repo(self):
        self.assertEqual(self.g.get_repo(self.url), 'ograycode.github.io')

    def test_get_pull_number(self):
        self.assertEqual(self.g.get_pull_number(self.url), '1')