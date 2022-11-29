import requests
import json
import base64
import os

github_url = "https://api.github.com"
org = "kxw9298"
github_token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f"Token {github_token}"}


def create_branch(target):
    repo_name = target.get("repo_name")
    branch_name = target.get("branch_name")
    url = f"{github_url}/repos/{org}/{repo_name}/git/refs"
    branches = requests.get(f"{url}/heads", headers=headers).json()
    branch, sha = branches[-1]['ref'], branches[-1]['object']['sha']
    payload = {"ref": f"refs/heads/{branch_name}",
               "sha": sha}
    r = requests.post(url, json=payload, headers=headers)
    print(r.content)


def read_github_file_and_update_content(target):
    print("")
    username = target.get("username")
    repo = target.get("repo")
    newbranch = target.get("newbranch")
    token = target.get("token")
    headers = {'Authorization': "Token " + token}


target_create_branch = {
    "repo_name": "git-python",
    "branch_name": "test"}


create_branch(target_create_branch)
