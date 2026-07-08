from fastapi import FastAPI
app = FastAPI()
@app.get("/health-check")
def home():
    