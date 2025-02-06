from fastapi import FastAPI, Request
import subprocess
import uvicorn
import uuid
from datetime import datetime
from Database import Database

app = FastAPI()
DB_FILE = "builds.db"
db = Database(DB_FILE)


# Endpoint to build history
@app.get("/builds")
def list_builds():
    builds = db.execute("SELECT id FROM builds ORDER BY timestamp DESC")
    return [f"http://0.0.0.0:8010/builds/{b[0]}" for b in builds]


# Endpoint to specific build
@app.get("/builds/{id}")
def get_build(id: str):
    build = db.execute("SELECT * FROM builds WHERE id = ?", (id,))
    if build:
        return {
            "id": build[0][0],
            "commit_id": build[0][1],
            "timestamp": build[0][2],
            "log": build[0][3]
        }
    return {"error": "Build not found"}


@app.post("/webhook")
async def handle(request: Request):
    data = await request.json()
    print(data)

    # Extract repository URL and branch info
    repo_url = data.get("repository", {}).get("clone_url")
    branch = data.get("ref").split("/")[-1]

    commit_id = data.get("after")
    timestamp = datetime.now().isoformat()
    build_id = str(uuid.uuid4())

    print("Webhook received for repo:", repo_url, ", branch:", branch)


    # Insert build details into the database
    db.execute("""
            INSERT INTO builds (id, commit_id, timestamp, log)
            VALUES (?, ?, ?, ?)
        """, (build_id, commit_id, timestamp, "Build started"))


    # here you do all the continuous integration tasks
    # for example
    # 1st clone your repository
    # 2nd compile the code

    return {"message": "CI job done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
