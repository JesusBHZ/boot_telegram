from fastapi import FastAPI

app = FastAPI()

@app.get("/keep-alive")
def keep_alive():
    return {"message": "API está activa"}

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
