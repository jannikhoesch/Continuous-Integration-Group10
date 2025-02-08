from fastapi import FastAPI, Request
import subprocess
import uvicorn
import tempfile
import os

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
        environment = get_environment(temp_dir)
        
        #add compilation here

        test_success, test_output = run_tests(environment, temp_dir, commit_sha)
        test_status = "success" if test_success else "failure"
        print(test_status)
        print(test_output)

    return {"message": "CI job done"}

def clone_repo(repo_url, branch, commit_sha, dir):
    clone_cmd = f"git clone {repo_url} {dir}"
    checkout_cmd = f"cd {dir} && git checkout {branch} && git reset --hard {commit_sha}"
    subprocess.run(clone_cmd, shell=True, check=True, capture_output=True, text=True)
    subprocess.run(checkout_cmd, shell=True, check=True, capture_output=True, text=True)

def get_environment(temp_dir):
    # Detect build system and compile
    if os.path.exists(f"{temp_dir}/Makefile"):
        return "Make"
    elif os.path.exists(f"{temp_dir}/setup.py"):
        return "Python"
    elif os.path.exists(f"{temp_dir}/pom.xml"):
        return "Maven"
    else:
        return False, "No recognized build system found (Makefile, setup.py, pom.xml)."

def run_tests(environment, temp_dir, commit_sha):
    if environment == "Python":
        test_cmd = f"cd {temp_dir} && python -m unittest discover tests"
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    return (result.returncode == 0, f"Commit {commit_sha}\n" + result.stdout + result.stderr)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
