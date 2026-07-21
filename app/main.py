from fastapi import FastAPI
from schemas import URLRequest
from utils.models import URL
from utils.db import engine,Base
app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message":"This is my url shortening service"}
@app.get("/health")
def health():
    return {"status":"healthy"}
@app.get("/about")
def about():
    return {"project":"url shortener"}
#path param
@app.get("/hello/{name}")
def hello(name : str):
    return f"hello {name}"
#query param
@app.get("/search")
def search(q:str):
    return {"search":q} 

@app.post("/shorten")
def shorten(request: URLRequest):
    return {
        "received_url": request.url
    }