from fastapi import FastAPI
app = FastAPI()
@app.get("/home")
def home():
    return "Hello this is home"
@app.get("/health")
def health():
    return {"status":"healthy"}
@app.get("/about")
def about():
    return {"project":"url shortener"}

@app.get("/hello/{name}")
def hello(name : str):
    return f"hello {name}"