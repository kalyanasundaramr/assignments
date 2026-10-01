from fastapi import FastAPI

app = FastAPI()

# Define a simple home route endpoint that returns a welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}

# Define a route endpoint that takes name parameter and returns a personalized greeting message
@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}! Welcome to the FastAPI application."}
