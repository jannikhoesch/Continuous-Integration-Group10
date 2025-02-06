from fastapi import FastAPI, Request
import subprocess
import uvicorn
import sqlite3
import uuid
from datetime import datetime

app = FastAPI()
DB_FILE = "builds.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS builds (
            id TEXT PRIMARY KEY,
            commit_id TEXT,
            timestamp TEXT,
            log TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# Endpoint to build history
@app.get("/builds")
def list_builds():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, commit_id, timestamp FROM builds ORDER BY timestamp DESC")
    builds = c.fetchall()
    conn.close()

    return [{"id": b[0], "commit_id": b[1], "timestamp": b[2]} for b in builds]


# Endpoint to specific build
@app.get("/builds/{id}")
def get_build(id: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM builds WHERE id = ?", (id,))
    build = c.fetchone()
    conn.close()

    if build:
        return {
            "id": build[0],
            "commit_id": build[1],
            "timestamp": build[2],
            "log": build[3]
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

    # Insert build details into the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
            INSERT INTO builds (id, commit_id, timestamp, log)
            VALUES (?, ?, ?, ?)
        """, (build_id, commit_id, timestamp, "Build started"))
    conn.commit()
    conn.close()

    #print("Webhook received for repo:", repo_url, ", branch:", branch)

    # here you do all the continuous integration tasks
    # for example
    # 1st clone your repository
    # 2nd compile the code

    return {"message": "CI job done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
