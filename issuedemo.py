from urllib import request, parse
import requests
import json
import csv

# Base URL being accessed
url = 'https://api.github.com/search/repositories'

# Dictionary of query parameters (if any)
print("请输入关键字：")
q = input()
parms = {
#    'q' : 'Hello-World',
    'q': q
}
# Extra headers
headers = {
    "Authorization": "token 4b9a001ae9e2a5ea2994f5ad38b381d2a052c84c" 
}

# Encode the query string
querystring = parse.urlencode(parms)

# Make a GET request and read the response
resp = requests.get(url+'?' + querystring, headers=headers)
# data = resp.json
data = json.loads(resp.text)
# print(data)

# 清除干扰的符号
def clean(value):
    if type(value) == str:
        return "\""+value.replace(",", ".").replace("\n", "  ").replace("\r", "  ")+"\""
    else:
        return value

# 表头
file_name = "output.csv"
with open(file_name,'a') as f:
    w = csv.writer(f)
    csv_line = ["id", "title", "url", 
                "repository_url", "comments_url", "events_url",
                "events_url", "html_url", 
                "node_id", "number", "labels", "state", 
                "locked", "assignee", "assignees", "milestone", 
                "comments", "created_at", "updated_at", "closed_at", 
                "author_association", "body", 
                "user.login'", "user.id", "user.node_id", "user.avatar_url",
                "user.gravatar_id", "user.url", "user.html_url",
                "user.followers_url", "user.following_url", "user.gists_url" ,
                "user.starred_url", "user.subscriptions_url", "user.organizations_url",
                "user.repos_url", "user.events_url", "user.received_events_url" ,
                "user.type", "user.site_admin",
                "pull_request"]
    w.writerow(csv_line)

# issue信息的封装
class IssuesInfo:
    def __init__(self, info_dict):
        self.url = info_dict['url']
        self.repository_url = info_dict['repository_url']
        self.labels_url = info_dict['labels_url']
        self.comments_url = info_dict['comments_url']
        self.events_url = info_dict['events_url']
        self.html_url = info_dict['html_url']
        self.id = info_dict['id']
        self.node_id = info_dict['node_id']
        self.number = info_dict['number']
        self.title = info_dict['title'] + "  "
        self.user = info_dict['user']
        self.labels = info_dict['labels']
        self.state = info_dict['state']
        self.locked = info_dict['locked']
        self.assignee = info_dict['assignee']
        self.assignees = info_dict['assignees']
        self.milestone = info_dict['milestone']
        self.comments = info_dict['comments']
        self.created_at = info_dict['created_at']
        self.updated_at = info_dict['updated_at']
        self.closed_at = info_dict['closed_at']
        self.author_association = info_dict['author_association']
        self.body = info_dict['body']
        try:
            self.pull_request = "" if not info_dict['pull_request'] else info_dict['pull_request']
        except:
            self.pull_request = ""
    
    def write_csv(self):
        with open(file_name,'a') as f:
            w = csv.writer(f)
            csv_line = [self.id, clean(self.title), self.url, 
                        self.repository_url, self.comments_url, self.events_url,
                        self.events_url, self.html_url, 
                        self.node_id, self.number, self.labels, self.state, 
                        self.locked, self.assignee, self.assignees, self.milestone, 
                        clean(self.comments), self.created_at, self.updated_at, self.closed_at, 
                        self.author_association, clean(self.body), 
                        self.user['login'], self.user['id'], self.user['node_id'], self.user['avatar_url'],
                        self.user['gravatar_id'], self.user['url'], self.user['html_url'],
                        self.user['followers_url'], self.user['following_url'], self.user['gists_url'], 
                        self.user['starred_url'], self.user['subscriptions_url'], self.user['organizations_url'], 
                        self.user['repos_url'], self.user['events_url'], self.user['received_events_url'], 
                        self.user['type'], self.user['site_admin'],
                        self.pull_request]
            w.writerow(csv_line)


for i in data['items']:
    i_url = str(i['issues_url']).replace("{/number}","")
    # print(i_url)

    i_resp = requests.get(i_url, headers=headers)
    i_data = json.loads(i_resp.text)
    for j_dict in i_data:
        info = IssuesInfo(j_dict)
        info.write_csv()
        