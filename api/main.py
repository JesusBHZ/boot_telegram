from fastapi import FastAPI

app = FastAPI()

@app.get("/keep-alive")
def keep_alive():
    return {"message": "API está activa"}
