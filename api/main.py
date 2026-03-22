from fastapi import FastAPI
from orchestrator.graph import graph

app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/query")
def query(q: str):
    result = graph.invoke({"query": q})
    return {
        "intent": result["intent"],
        "response": result["response"]
    }