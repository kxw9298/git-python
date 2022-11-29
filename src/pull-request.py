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
    repo_name = target.get("repo_name")
    branch_name = target.get("branch_name")
    file_path = target.get("file_path")
    url = f"{github_url}/repos/{org}/{repo_name}/contents/{file_path}"
    r = requests.get(
        url,
        params={"ref": branch_name},
        headers=headers
    )
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()
    print(file_content)
    return {
        "file_contents": file_content
    }


target_create_branch = {
    "repo_name": "git-python",
    "branch_name": "test"}

target_read_file_and_update = {
    "repo_name": "git-python",
    "branch_name": "test",
    "file_path": "src/sample/application.properties"
}

# create_branch(target_create_branch)
read_github_file_and_update_content(target_read_file_and_update)
