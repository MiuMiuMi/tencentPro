from urllib import request, parse
import requests
import json

# Base URL being accessed
url = 'https://api.github.com/search/repositories'

# Dictionary of query parameters (if any)
parms = {
   'q' : 'tetris+language:assembly',
   'sort' : 'stars',
   'order' : 'desc'
}

# Encode the query string
querystring = parse.urlencode(parms)

# Make a GET request and read the response
resp = requests.get(url+'?' + querystring)
# data = resp.json
data = json.loads(resp.text)
print(data)
print ("data['total_count']is ::::::::::::::: ", data['total_count'])
print(data['items'])