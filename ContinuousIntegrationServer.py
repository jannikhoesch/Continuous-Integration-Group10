from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import subprocess
import uvicorn
import uuid
from datetime import datetime
from Database import Database

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_FILE = "builds.db"
db = Database(DB_FILE)


# Endpoint to build history
@app.get("/builds")
def list_builds(request: Request):
    builds = db.execute("SELECT id, timestamp FROM builds ORDER BY timestamp DESC")
    b = [{"id": b[0], "timestamp": datetime.fromisoformat(b[1]).strftime("%Y-%m-%d %H:%M:%S")} for b in builds]
    return templates.TemplateResponse("build_history.html", {"request": request, "builds": b})

# Endpoint to specific build
@app.get("/builds/{id}")
def get_build(request: Request, id: str):
    build = db.execute("SELECT * FROM builds WHERE id = ?", (id,))
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
    print(data)

    # here you do all the continuous integration tasks
    # for example
    # 1st clone your repository
    # 2nd compile the code

    return {"message": "CI job done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
