import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import subprocess
import uvicorn
import logging
import uuid
from datetime import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Database import Database
from src.CommitStatus import send_commit_status
import tempfile

"""
Continuous Integration Server
This module defines a FastAPI application that handles GitHub webhook events to perform continuous integration tasks.
It clones the repository, compiles the project, runs tests, and updates the build status in the database.

Functions:
    handle(request: Request) -> dict:
        Handles incoming webhook requests from GitHub, processes the repository, and updates the build status.

Dependencies:
    - FastAPI
    - logging
    - tempfile
    - datetime
    - uuid
    - sqlite3 (for database operations)
    - Custom functions: clone_repo, compile_project, run_tests, send_commit_status
"""

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_FILE = "builds.db"
db = Database(DB_FILE)
logging.basicConfig(level=logging.INFO)


# Endpoint to build history
@app.get("/builds")
    """
    Handles the request to list all builds in the system.
    Args:
        request (Request): The request object containing request details.
    Returns:
        TemplateResponse: A response object that renders the build history template with the list of builds.
    The function fetches the build records from the database, formats the timestamp for each build,
    and returns a TemplateResponse with the formatted build data.
    """
    builds = db.fetch("SELECT id, timestamp FROM builds ORDER BY timestamp DESC")
    b = [{"id": b[0], "timestamp": datetime.fromisoformat(b[1]).strftime("%Y-%m-%d %H:%M:%S")} for b in builds]
    return templates.TemplateResponse("build_history.html", {"request": request, "builds": b})

# Endpoint to specific build
@app.get("/builds/{id}")
def get_build(request: Request, id: str):
    """
    Retrieve build details from the database based on the provided build ID.

    Args:
        request (Request): The request object.
        id (str): The ID of the build to retrieve.

    Returns:
        TemplateResponse: A response object containing the build details rendered in the "build.html" template if the build is found.
        dict: A dictionary containing an error message if the build is not found.
    """
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

# Endpoint to handle webhook
@app.post("/webhook")
async def handle(request: Request):
    """
    Continuous Integration Server
    This module defines a FastAPI application that handles GitHub webhook events to perform continuous integration tasks.
    It clones the repository, compiles the project, runs tests, and updates the build status in the database.
    Functions:
        handle(request: Request) -> dict:
            Handles incoming webhook requests from GitHub, processes the repository, and updates the build status.
    Dependencies:
        - FastAPI
        - logging
        - tempfile
        - datetime
        - uuid
        - sqlite3 (for database operations)
        - Custom functions: clone_repo, compile_project, run_tests, send_commit_status
    """
    data = await request.json()
    logging.info(f"Received webhook data: {data}")

    # Extract repository URL and branch info
    repo_url = data.get("repository", {}).get("clone_url")
    branch = data.get("ref").split("/")[-1]
    commit_sha = data.get("after")

    logging.info(f"Cloning repository {repo_url} at branch {branch} with commit {commit_sha}")

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_repo(repo_url, branch, commit_sha, temp_dir)
        
        success, log = compile_project(temp_dir)

        test_success, test_output = run_tests(temp_dir, commit_sha)
        test_status = "success" if test_success else "failure"


    commit_id = data.get("after")
    timestamp = datetime.now().isoformat()
    build_id = str(uuid.uuid4())

    logging.info(f"Webhook received for repo: {repo_url}, branch: {branch}, commit: {commit_sha}")

    # Insert build details into the database
    db.execute("""
            INSERT INTO builds (id, commit_id, timestamp, log)
            VALUES (?, ?, ?, ?)
        """, (build_id, commit_id, timestamp, log))

    logging.info(f"Build {build_id} {'succeeded' if success else 'failed'} for commit {commit_id} at {timestamp}")

    # Send commit status to GitHub
    target_url = "http://127.0.0.1:8010"
    send_commit_status(commit_sha, test_status, "TEST", target_url)

    return {"message": "CI job done"}

def clone_repo(repo_url, branch, commit_sha, dir):
    """
    Clones a git repository and checks out a specific branch and commit.
    Args:
        repo_url (str): The URL of the repository to clone.
        branch (str): The branch to checkout.
        commit_sha (str): The specific commit SHA to reset to.
        dir (str): The directory where the repository will be cloned.
    Raises:
        subprocess.CalledProcessError: If the git commands fail.
    """
    clone_cmd = f"git clone {repo_url} {dir}"
    checkout_cmd = f"cd {dir} && git checkout {branch} && git reset --hard {commit_sha}"
    subprocess.run(clone_cmd, shell=True, check=True, capture_output=True, text=True)
    subprocess.run(checkout_cmd, shell=True, check=True, capture_output=True, text=True)
        
def compile_project(dir):
    """
    Compiles all Python files in the specified directory.
    This function changes the current working directory to the specified directory
    and runs the Python compileall module to compile all Python files in that directory.
    Args:
        dir (str): The directory containing the Python files to compile.
    Returns:
        tuple: A tuple containing a boolean and a string. The boolean is True if the 
               compilation succeeded, and False otherwise. The string contains the 
               standard output if the compilation succeeded, or the standard error 
               if the compilation failed.
    Raises:
        None
    """
    compile_cmd = f"cd {dir} && python -m compileall ."
    
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Compilation failed: {result.stderr}")
        return False, f"Compilation failed: {result.stderr}"
    
    logging.info(f"Compilation succeeded: {result.stdout}")
    return True, result.stdout

def run_tests(temp_dir, commit_sha):
    """
    Runs unit tests in the specified temporary directory and returns the result.
    Args:
        temp_dir (str): The path to the temporary directory where the tests are located.
        commit_sha (str): The SHA of the commit being tested.
    Returns:
        tuple: A tuple containing a boolean indicating if the tests passed (True if all tests passed, False otherwise),
               and a string with the commit SHA and the combined stdout and stderr output from the test command.
    """
    test_cmd = f"cd {temp_dir} && python -m unittest discover tests"
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    return (result.returncode == 0, f"Commit {commit_sha}\n" + result.stdout + result.stderr)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
