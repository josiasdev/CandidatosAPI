from fastapi import FastAPI

# Placeholder for valid Python code
print("Hello, World!")
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}