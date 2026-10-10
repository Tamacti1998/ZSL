from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def initial():
    return "Hello, World!"