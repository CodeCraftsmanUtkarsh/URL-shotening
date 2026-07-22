from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .schemas import URLRequest
from .crud import create_url,get_url,increment_clicks
from .utils.db import engine, Base, get_db
from .utils.hash import generate_short_code
from fastapi.responses import RedirectResponse
app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "This is my URL shortening service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "project": "URL Shortener"
    }


# Path Parameter
@app.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"Hello {name}"
    }


# Query Parameter
@app.get("/search")
def search(q: str):
    return {
        "search": q
    }


@app.post("/shorten")
def shorten(
    request: URLRequest,
    db: Session = Depends(get_db)
):
    # Generate short code
    short_code = generate_short_code(
        str(request.url)
    )

    # Store in database
    url = create_url(
        db,
        str(request.url),
        short_code
    )

    # Return response
    return {
        "short_code": url.short_code,
        "original_url": url.original_url
    }
@app.get("/{short_url}")
def redirect_to_url(short_url:str,db:Session=Depends(get_db)):
    url=get_url(db,short_url)
    if not url:
        return {"error":"URL not found"}
    increment_clicks(db,url)
    return RedirectResponse(url=url.original_url)
@app.get("/stats/{short_url}")
def get_stats(short_url:str,db:Session=Depends(get_db)):
    url=get_url(db,short_url)
    if not url:
        return {"error":"url not found"}
    return {
        "original_url":url.original_url,
        "short_url":url.short_code,
        "clicks":url.clicks,
        "created_at":url.created_at
        }