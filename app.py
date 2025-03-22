from fastapi import FastAPI
from chatbot import process_query

app = FastAPI()

@app.post("/chat")
def chat(query: str):
    response = process_query(query)
    return {"response": response}

# Run with: uvicorn app:app --reload