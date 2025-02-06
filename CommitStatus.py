import requests

def send_commit_status(commit_sha: str, state: str, description: str, target_url: str):
    """
    Send commit status to GitHub using the Commit Status API.
    """

    github_api_url = "https://api.github.com/repos/jannikhoesch/Continuous-Integration-Group10/statuses"
    with open('GithubToken.txt', 'r') as file:
        file.readline()
        github_token = file.readline() # found on the second line
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "state": state,
        "target_url": target_url,  # The URL where details about the build can be found
        "description": description,
        "context": "ci/your-ci-tool"  # You can name it according to your CI tool
    }

    # Send the commit status to GitHub
    response = requests.post(f"{github_api_url}/{commit_sha}", json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Successfully posted commit status: {state}")
    else:
        print(f"Failed to post commit status: {response.status_code}, {response.text}")

commit_SHA = "a284bfc59fd6f157f65b71d027fcf09d8194066c"
status = "success" # I think I get this from the previous process
description = "TESTING THE THING"
target_url = "http://127.0.0.1:8000 "
send_commit_status(commit_SHA, status, description, target_url)