from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Import the agent
# Note: In a real deployment, we'd handle the import more gracefully or use dependency injection
try:
    from rag_agent import TregAgent
except ImportError:
    # Mock for environments where llama-index is not installed (like this agent's runner)
    class TregAgent:
        def query(self, q):
            return {
                "answer": "This is a mock response because llama-index is not installed in this environment. Please install dependencies.",
                "sources": []
            }

app = FastAPI(title="Treg Research Assistant API")

class QueryRequest(BaseModel):
    question: str

class Source(BaseModel):
    source: str
    title: str
    url: str
    id: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

# Global agent instance
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    try:
        agent = TregAgent()
        print("TregAgent initialized.")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        # We don't crash here to allow the server to start even if OpenAI key is missing, 
        # but requests will fail or return mock data.

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        result = agent.query(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
