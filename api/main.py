from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from orchestrator.graph import graph
import os

app = FastAPI(title="Agentic Support System")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the chat UI at root
@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse("static/index.html")

# Main chat endpoint — matches the UI's POST /chat call
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    if not message:
        return {"response": "Please ask a question."}

    try:
        result = graph.invoke({"query": message})
        return {
            "response": result.get("response", "I couldn't find an answer."),
            "intent": result.get("intent", "unknown")
        }
    except Exception as e:
        return {"response": f"Something went wrong: {str(e)}"}

# Keep the old /query endpoint so nothing breaks
@app.post("/query")
async def query(q: str):
    result = graph.invoke({"query": q})
    return {
        "intent": result["intent"],
        "response": result["response"]
    }

# Health check — required for Render to know the app is alive
@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    print("App starting up...")
    print(f"FAQ data path exists: {os.path.exists('data/docs/faq.txt')}")
    print("Agentic Support System is ready.")