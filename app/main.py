from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def home():
    return {"message":"This is my url shortening service"}

@app.get("/health")
def health():
    return {"status":"healthy"}
@app.get("/about")
def about():
    return {"project":"url shortener"}

@app.get("/hello/{name}")
def hello(name : str):
    return f"hello {name}"