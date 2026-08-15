from fastapi import FastAPI, Depends,Request, HTTPException
from sqlalchemy.orm import Session
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .schemas import URLRequest
from .crud import create_url,get_url,increment_clicks,get_url_by_orginal
from .utils.db import engine, Base, get_db
from .utils.hash import generate_short_code
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone
import redis
app = FastAPI()
@app.get("/redis-test")
def redis_test():
    redis_client.set("msg","redis is working")
    value=redis_client.get("msg")
    return {
        "message":value
    }
Base.metadata.create_all(bind=engine)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
redis_client=redis.Redis(host="localhost",port=6379,decode_responses=True)
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
@limiter.limit("5/minute")
def shorten(
    request: Request,
    body:URLRequest,
    db: Session = Depends(get_db )
):
    existing=get_url_by_orginal(db,str(body.url))
    if existing:
        return {
            "short_code":existing.short_code,
            "original_url":existing.original_url
        }
    short_code = generate_short_code(
        str(body.url)
    )
    expires_at=(datetime.now(timezone.utc) + timedelta(days=body.expires_in))
    
    url = create_url(
        db,
        str(body.url),
        short_code,
        expires_at
    )
    return {
        "short_code": url.short_code,
        "original_url": url.original_url
    }
@app.get("/{short_url}")
def redirect_to_url(short_url:str,db:Session=Depends(get_db)):
    url=get_url(db,short_url)
    if not url:
        raise HTTPException(status_code=404,detail="URL Not Found")
    if datetime.utcnow()>url.expires_at:
        raise HTTPException(status_code=410,detail="Link has expired")
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
        "created_at":url.created_at,
        "expires_at":url.expires_at
        }



    