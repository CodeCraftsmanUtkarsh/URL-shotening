from sqlalchemy.orm import Session
from .utils.models import URL
def create_url(db:Session,original_url:str,short_code:str):
    new_url=URL(
        original_url=original_url,
        short_code=short_code
        )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url
def get_url(db:Session,short_code:str):
    return db.query(URL).filter(URL.short_code==short_code).first()
def increment_clicks(db:Session,url:URL):
    url.clicks+=1
    db.commit()
def get_url_by_orginal(db:Session,original_url:str):
    return db.query(URL).filter(URL.original_url==original_url).first()