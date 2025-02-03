from fastapi import FastAPI, Request
import subprocess
import uvicorn

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

    return {"message": "CI job done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
