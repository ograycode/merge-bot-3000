from django.db import models
import re
import requests
import json
from datetime import datetime, timedelta

class Settings(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField()

    @staticmethod
    def get_github_username():
        return Settings.objects.get(pk='username')

    @staticmethod
    def get_github_password():
        return Settings.objects.get(pk='password')

class PullRequest(models.Model):
    comment_id = models.IntegerField()
    merge_request_date = models.DateTimeField()
    number = models.IntegerField()
    user = models.CharField(max_length=256)
    repo = models.CharField(max_length=256)
    time_pulled = models.DateTimeField()
    already_merged = models.BooleanField(default=False)
    title = models.TextField()
    message = models.TextField()

    def __unicode__(self):
        return unicode(self.user) + ' requested ' + unicode(self.repo) + ', number ' + unicode(self.number) + ', to be merged at ' + unicode(self.merge_request_date)

    def get_time_to_merge(self, message=None):
        if message is None:
            message = self.message
        answer = None
        try:
            date_to_merge = re.findall('\d\d/\d\d/\d\d\d\d', message)[0]
            time_to_merge_gmt = re.findall('\d\d:\d\d', message)[0]
            format = "%m/%d/%Y %H:%M"
            answer = datetime.strptime(date_to_merge + ' ' + time_to_merge_gmt, format)
        except Exception, e:
            answer = None

        return answer

    @staticmethod
    def save_new_merge_requests(set_read=True):
        github = GitHubApi()
        git_util = GitHubUtils()

        response = github.get_notifications()
        if response.status_code is 200:
            body = json.loads(response.text)
            for r in body:
                if r['reason'] == 'mention' and r['subject']['type'] == 'PullRequest':
                    
                    try:
                        url = r['subject']['url']

                        p = PullRequest()
                        p.title = r['subject']['title']
                        p.user = git_util.get_user(url)
                        p.repo = git_util.get_repo(url)
                        p.number = git_util.get_pull_number(url)

                        issue = github.get_issue(p.user, p.repo, p.number)
                        if issue.status_code is 200:
                            json_response = json.loads(issue.text)
                            p.message = json_response['body']
                            p.merge_request_date = p.get_time_to_merge()
                            p.comment_id = json_response['id']
                        p.time_pulled = datetime.now()
                        p.save()

                    except Exception, e:
                        pass

            if set_read:
                github.set_notifications_as_read()

    @staticmethod
    def merge_pull_requests(minutes_in_future=10):
        github = GitHubApi()
        time = timedelta(minutes=minutes_in_future)
        in_the_future = datetime.now() + time

        requests = PullRequest.objects.filter(
            merge_request_date__lte=in_the_future
        ).exclude(
            already_merged=True
        )

        for request in requests:
            response = github.merge(request.user, request.repo, request.number, "merge-bot here, merging your request")
            if response.status_code is 200:
                request.already_merged = True
                request.save()


class GitHubUtils(object):
    def get_user(self, url):
        return url.split('/')[4]

    def get_repo(self, url):
        return url.split('/')[5]

    def get_pull_number(self, url):
        return url.split('/')[-1]

class GitHubApi(object):
    """docstring for GitHubApi"""
    def __init__(self, user=None, password=None):
        super(GitHubApi, self).__init__()
        self.user = user if user is not None else Settings.get_github_username()
        self.password = password if password is not None else Settings.get_github_password()
        self.base_url = 'https://api.github.com/'

    def get_notifications(self):
        url = self.base_url + 'notifications'
        return requests.get(url, auth=self.__get_auth())

    def set_notifications_as_read(self):
        url = self.base_url + 'notifications'
        return requests.put(url, auth=self.__get_auth()) 

    def merge(self, owner, repo, number, message):
        url = self.base_url + 'repos/'+owner+'/'+repo+'/pulls/'+str(number)+'/merge'
        data = '{"commit_message":"'+message+'"}'
        return requests.put(url, data=data, auth=self.__get_auth())

    def get_issue(self, owner, repo, number):
        url = self.base_url + 'repos/'+owner+'/'+repo+'/issues/'+str(number)
        print(url)
        return requests.get(url, auth=self.__get_auth())

    def __get_auth(self):
        return (self.user, self.password)
