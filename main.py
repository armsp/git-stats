import os
#import ssl
import json
import logging
from datetime import datetime
from urllib import request, parse

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(message)s')
logging.debug(os.environ['GITHUB_REPOSITORY'])

query = '''
query {
  viewer{
    repositories(orderBy: {field: STARGAZERS, direction: DESC}){
      totalCount
    }
    followers{
      totalCount
    }
    issues_sum:issues{
      totalCount
    }
    issues_open:issues(states: OPEN){
      totalCount
    }
    issues_closed:issues(states: CLOSED){
      totalCount
    }
    pr_sum:pullRequests{
      totalCount
    }
    pr_open:pullRequests(states: OPEN){
      totalCount
    }
    pr_closed:pullRequests(states: CLOSED){
      totalCount
    }
    pr_merged:pullRequests(states: MERGED){
      totalCount
    }
    repositories(orderBy: {field: STARGAZERS, direction: DESC}){
      nodes{
        name
        stargazers{
          totalCount
        }
        watchers{
          totalCount
        }
        forkCount
      }
    }
  }
}
'''
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE
url = 'https://api.github.com/graphql'
github_token = f"Bearer {os.environ['GITHUB_TOKEN']}"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'content-type': 'application/json', "Authorization": github_token}

data = {'query': query}
post_data = json.dumps(data).encode('utf-8')

req = request.Request(url, headers=header, data=post_data)

try:
  response = request.urlopen(req)
except Exception as e:
  logging.error("Request Failed", exc_info=True)
else:
  logging.debug(response.getcode())
  logging.debug(response.info())

if response.getcode() == 200:
  response_dict = json.load(response)

  fork_count = sum([node['forkCount'] for node in response_dict['data']['viewer']['repositories']['nodes']])
  star_count = sum([node['stargazers']['totalCount'] for node in response_dict['data']['viewer']['repositories']['nodes']])
  watchers_count = sum([node['watchers']['totalCount'] for node in response_dict['data']['viewer']['repositories']['nodes']])

  namespace = {
    'username': 'armsp',
    'pr': response_dict['data']['viewer']['pr_merged']['totalCount'],
    'followers': response_dict['data']['viewer']['followers']['totalCount'],
    'stars': star_count,
    'open_issues': response_dict['data']['viewer']['issues_open']['totalCount'],
    'closed_issues': response_dict['data']['viewer']['issues_closed']['totalCount'],
    'watchers': watchers_count,
    'forks': fork_count,
    'repositories': response_dict['data']['viewer']['repositories']['totalCount'],
    'current_time': datetime.now(),
    'commit_sha': os.environ['GITHUB_SHA']
    }
  #print(namespace)

  logging.debug(os.environ['GITHUB_SHA'])

  # #update values
  # May have to use GITHUB_WORKSPACE default environment variable
  with open('template.html') as f:
    template_html = f.read()

  formatted_html = template_html.format(**namespace)

  with open('index.html', 'w+') as f:
    f.write(formatted_html)

logging.debug("Contents updated to index.html file")