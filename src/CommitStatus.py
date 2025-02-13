import requests
import os
from dotenv import load_dotenv

def send_commit_status(commit_sha: str, state: str, description: str, target_url: str):
    """
    Sends the status of a commit to GitHub.

    Args:
        commit_sha (str): The SHA of the commit.
        state (str): The state of the commit status. Can be one of 'error', 'failure', 'pending', or 'success'.
        description (str): A short description of the status.
        target_url (str): The URL where details about the build can be found.

    Returns:
        bool: True if the status was successfully posted, False otherwise.
    """
    
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    github_api_url = os.getenv("GITHUB_API_URL")

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
        return True
    else:
        print(f"Failed to post commit status: {response.status_code}, {response.text}")
        return False

"""
# example use:
commit_SHA = "a284bfc59fd6f157f65b71d027fcf09d8194066c"
status = "success" # I think I get this from the previous process
description = "TESTING THE THING"
target_url = "http://127.0.0.1:8000 "
send_commit_status(commit_SHA, status, description, target_url)
"""