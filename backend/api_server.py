from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os

# Import the Orchestrator
try:
    from backend.agents.orchestrator import OrchestratorAgent
except ImportError as e:
    import traceback
    traceback.print_exc()
    print(f"ImportError details: {e}")
    # Mock for environments where dependencies are missing
    class OrchestratorAgent:
        def __init__(self): pass
        def query(self, q, session_id=None):
            return {
                "answer": "Mock response: Agent dependencies not found.",
                "steps": []
            }

app = FastAPI(title="Treg Research Assistant API")

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"
    model_type: Optional[str] = "pro" # pro or flash

class Step(BaseModel):
    action: str
    observation: str

class QueryResponse(BaseModel):
    answer: str
    steps: List[Any]

# Global agent instance
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    try:
        # In a real app, we might instantiate per request or use a pool
        agent = OrchestratorAgent()
        print("OrchestratorAgent initialized.")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Note: In a real implementation, we'd pass model_config to the agent
        # to dynamically switch models if supported by the BaseAgent logic.
        result = agent.query(request.question, session_id=request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Treg Research Assistant API is running", "docs_url": "/docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
