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


def read_github_file(target):
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

def replace_text_in_file_content(target):
    file_contents = target.get("file_contents")
    text_to_search = target.get("text_to_search")
    text_to_replace = target.get("text_to_replace")

    file_contents = file_contents.replace(text_to_search, text_to_replace)
    print(file_contents)
    return {
        "file_contents": file_contents
    }


target_create_branch = {
    "repo_name": "git-python",
    "branch_name": "test"}

target_read_file = {
    "repo_name": "git-python",
    "branch_name": "test",
    "file_path": "src/sample/application.properties"
}

# create_branch(target_create_branch)
output = read_github_file(target_read_file)
target_replace_text_in_file_content = {
    "file_contents": output.get('file_contents'),
   "text_to_search": "10.0.0.0",
   "text_to_replace": "10.0.0.2"
}
replace_text_in_file_content(target_replace_text_in_file_content)