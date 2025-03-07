from fastapi import FastAPI
from system_stats import get_system_stats

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server Health Monitor API is running!"}

@app.get("/system")
def system_info():
    return get_system_stats()
