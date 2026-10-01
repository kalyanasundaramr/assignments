from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Simple Calculator API"}


@app.get("/calculate")
def calculate(a: float, b: float, operation: str):

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        if b == 0:
            return {"error": "Cannot divide by zero"}
        result = a / b

    else:
        return {"error": "Invalid operation"}

    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }
