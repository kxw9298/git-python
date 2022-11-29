import requests
import json
import base64
import os

def create_branch(username, repo, newbranch, token):
    headers = {'Authorization': "Token " + token}
    url = "https://api.github.com/repos/"+username+"/"+repo+"/git/refs/heads"
    branches = requests.get(url, headers=headers).json()
    branch, sha = branches[-1]['ref'], branches[-1]['object']['sha']
    res = requests.post('https://api.github.com/repos/'+username+'/'+repo+'/git/refs', json={
        "ref": "refs/heads/"+newbranch,
        "sha": sha
    }, headers=headers)
    print(res.content)


token = os.getenv('GITHUB_TOKEN')
username = "kxw9298"
repo = "git-python"
newbranch="test"

create_branch(username, repo, newbranch, token)