import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.utils.db import Base,get_db
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
engine=create_engine(SQLALCHEMY_TEST_URL,connect_args={"check_same_thread":False})
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db]=override_get_db
