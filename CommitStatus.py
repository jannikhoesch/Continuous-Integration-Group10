import requests

def send_commit_status(commit_sha: str, state: str, description: str, target_url: str,
                       github_token: str, github_api_url):
    """
    Send commit status to GitHub using the Commit Status API.
    """
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