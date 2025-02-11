from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import subprocess
import uvicorn
from datetime import datetime
from .Database import Database
from .CommitStatus import send_commit_status
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_FILE = "builds.db"
db = Database(DB_FILE)


# Endpoint to build history
@app.get("/builds")
def list_builds(request: Request):
    builds = db.fetch("SELECT id, timestamp FROM builds ORDER BY timestamp DESC")
    b = [{"id": b[0], "timestamp": datetime.fromisoformat(b[1]).strftime("%Y-%m-%d %H:%M:%S")} for b in builds]
    return templates.TemplateResponse("build_history.html", {"request": request, "builds": b})

# Endpoint to specific build
@app.get("/builds/{id}")
def get_build(request: Request, id: str):
    build = db.fetch("SELECT * FROM builds WHERE id = ?", (id,))
    if build:
        build_details = {
            "id": build[0][0],
            "commit_id": build[0][1],
            "timestamp": datetime.fromisoformat(build[0][2]).strftime("%Y-%m-%d %H:%M:%S"),
            "log": build[0][3]
        }
        return templates.TemplateResponse("build.html", {"request": request, "build": build_details})
    return {"error": "Build not found"}


@app.post("/webhook")
async def handle(request: Request):
    data = await request.json()

    # Extract repository URL and branch info
    repo_url = data.get("repository", {}).get("clone_url")
    branch = data.get("ref").split("/")[-1]
    commit_sha = data.get("after")

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_repo(repo_url, branch, commit_sha, temp_dir)
        
        #add compilation here

        test_success, test_output = run_tests(temp_dir, commit_sha)
        test_status = "success" if test_success else "failure"

    return {"message": "CI job done"}

def clone_repo(repo_url, branch, commit_sha, dir):
    clone_cmd = f"git clone {repo_url} {dir}"
    checkout_cmd = f"cd {dir} && git checkout {branch} && git reset --hard {commit_sha}"
    subprocess.run(clone_cmd, shell=True, check=True, capture_output=True, text=True)
    subprocess.run(checkout_cmd, shell=True, check=True, capture_output=True, text=True)

def run_tests(temp_dir, commit_sha):
    test_cmd = f"cd {temp_dir} && python -m unittest discover tests"
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    return (result.returncode == 0, f"Commit {commit_sha}\n" + result.stdout + result.stderr)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
