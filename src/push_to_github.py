import requests
import json
import base64

def push_to_github(filename_to, filename_from, repo, branch, token):
    url="https://api.github.com/repos/"+repo+"/contents/"+filename_to

    base64content=base64.b64encode(open(filename_from,"rb").read())
    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    print(data)
    sha = data['sha']
    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message":"update",
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")

token = "ghp_xxxxxx"
filename_from="README.md"
filename_to="src/README.md"
repo = "kxw9298/git-python"
branch="main"

push_to_github(filename_to, filename_from, repo, branch, token)