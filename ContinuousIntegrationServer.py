from fastapi import FastAPI, Request
import subprocess
import uvicorn
import tempfile

app = FastAPI()


@app.post("/webhook")
async def handle(request: Request):
    data = await request.json()

    # Extract repository URL and branch info
    repo_url = data.get("repository", {}).get("clone_url")
    branch = data.get("ref").split("/")[-1]
    commit_sha = data.get("after")

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_repo(repo_url, branch, commit_sha, temp_dir)

    # here you do all the continuous integration tasks
    # for example
    # 1st clone your repository
    # 2nd compile the code

    return {"message": "CI job done"}

def clone_repo(repo_url, branch, commit_sha, dir):
    clone_cmd = f"git clone {repo_url} {dir}"
    checkout_cmd = f"cd {dir} && git checkout {branch} && git reset --hard {commit_sha}"
    subprocess.run(clone_cmd, shell=True, check=True, capture_output=True, text=True)
    subprocess.run(checkout_cmd, shell=True, check=True, capture_output=True, text=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
