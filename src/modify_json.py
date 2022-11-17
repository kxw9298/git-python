import json
import datetime;
import requests
import json
import base64
import os

def github_read_file(username, repository_name, branch, file_path, token):
    headers = {}

        
    url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    print(data)
    sha = data['sha']
    # r.raise_for_status()
    # data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return (file_content, sha)

def push_to_github(base64content, sha, username, repository_name, branch, file_path, token):
    url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
    message = json.dumps({"message":"update",
                        "branch": branch,
                        "content": base64content.decode("utf-8") ,
                        "sha": sha
                        })

    resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

    print(resp)

token = os.getenv('GITHUB_TOKEN')
file_path = "src/sample/data.json"
username = "kxw9298"
repository_name = "git-python"
branch="main"

resp = github_read_file(username, repository_name, branch, file_path, token)
file_content = resp[0]
sha = resp[1]
data = json.loads(file_content)
with open('./data.json', 'w') as f:
    data['time'] = str(datetime.datetime.now())
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()     # remove remaining part

base64content=base64.b64encode(open('./data.json',"rb").read())
push_to_github(base64content, sha, username, repository_name, branch, file_path, token)
    

