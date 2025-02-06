from fastapi import FastAPI, Request
import subprocess
import uvicorn
from CommitStatus import send_commit_status

app = FastAPI()


@app.post("/webhook")
async def handle(request: Request):
    data = await request.json()

    # Extract repository URL and branch info
    repo_url = data.get("repository", {}).get("clone_url")
    branch = data.get("ref").split("/")[-1]

    # here you do all the continuous integration tasks
    # for example
    # 1st clone your repository
    # 2nd compile the code
    # 3rd send commit status to github
    """
    commit_SHA = data.get("head_commit", {}).get("id")
    status = "TEST" # I think I get this from the previous process
    description = "TESTING THE THING"
    target_url = "http://127.0.0.1:8000 "
    send_commit_status(commit_SHA, status, description, target_url)
    """
    return {"message": "CI job done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
