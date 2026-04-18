from fastapi import FastAPI
from fastapi.responses import FileResponse
from orchestrator.graph import graph

app = FastAPI()

@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse("api/index.html")

@app.post("/query")
def query(q: str):
    result = graph.invoke({"query": q})
    return {
        "intent": result["intent"],
        "response": result["response"]
    }

@app.on_event("startup")
def startup_event():
    # rebuild the vector store from data/docs/
    pass