from typing import List, Callable, Optional, Dict, Any
from google.adk import Agent as ADKAgent
from google.adk.runners import InMemoryRunner
from backend.config import Config
import os
import asyncio
import concurrent.futures

class BaseAgent:
    """
    Base class for all agents in the system.
    Uses Google ADK (Agent Development Kit) for automatic function calling.
    """
    
    def __init__(
        self, 
        name: str, 
        model_name: str,
        tools: Optional[List[Callable]] = None,
        system_instruction: Optional[str] = None
    ):
        self.name = name
        self.model_name = model_name
        self.tools = tools or []
        self.system_instruction = system_instruction or ""
        
        # Set Google API key for ADK
        if Config.GOOGLE_API_KEY:
            os.environ["GOOGLE_API_KEY"] = Config.GOOGLE_API_KEY
        
        # Initialize ADK Agent
        # ADK handles function calling automatically
        self.agent = ADKAgent(
            model=model_name,
            name=name,
            description=f"{name} agent",
            instruction=self.system_instruction,
            tools=self.tools
        )
        
        # Create runner for executing queries
        self.runner = InMemoryRunner(agent=self.agent)
        # Thread pool for running async code from sync contexts (e.g., tools)
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    async def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Executes a query against the agent with automatic function calling.
        ADK handles function calling automatically via the Runner.
        This is the async version - use this from async contexts (e.g., FastAPI).
        """
        print(f"[{self.name}] Processing: {input_text}")
        try:
            response_text = await self._run_query(input_text)
            
            return {
                "answer": response_text,
                "steps": []
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            import traceback
            traceback.print_exc()
            return {"answer": f"Error processing request: {str(e)}", "steps": []}
    
    def query_sync(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Synchronous wrapper for query(). Use this from synchronous contexts (e.g., tools).
        Runs the async query in a thread pool to avoid event loop conflicts.
        """
        print(f"[{self.name}] Processing (sync): {input_text}")
        try:
            # Check if we're in an async context
            try:
                loop = asyncio.get_running_loop()
                # We're in an async context, run in thread pool
                future = self._executor.submit(asyncio.run, self._run_query(input_text))
                response_text = future.result()
            except RuntimeError:
                # No running loop, safe to use asyncio.run directly
                response_text = asyncio.run(self._run_query(input_text))
            
            return {
                "answer": response_text,
                "steps": []
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            import traceback
            traceback.print_exc()
            return {"answer": f"Error processing request: {str(e)}", "steps": []}
    
    async def _run_query(self, input_text: str) -> str:
        """Internal async method to run the query using ADK Runner."""
        # run_debug returns a list of events
        events = await self.runner.run_debug(input_text, quiet=True)
        
        response_parts = []
        for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_parts.append(part.text)
        
        # Combine all text parts
        return "\n".join(response_parts) if response_parts else "No response generated."

    def get_tool_definitions(self) -> List[Dict]:
        """Returns JSON schema of tools for inspection."""
        return [tool.__name__ for tool in self.tools]
