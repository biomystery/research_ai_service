from typing import List, Callable, Optional, Dict, Any
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from backend.config import Config

class BaseAgent:
    """
    Base class for all agents in the system.
    Wraps Google ADK Agent patterns.
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
        self.system_instruction = system_instruction
        
        # Initialize Gemini Model
        # We assume the environment variable GOOGLE_API_KEY is set, 
        # or we can pass it if the library supports it.
        self.model = Gemini(
            model=self.model_name
        )
        
        # Initialize Agent
        self.agent = Agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_instruction
        )
        
        # Initialize Runner
        self.runner = InMemoryRunner(agent=self.agent)

    def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Executes a query against the agent.
        """
        print(f"[{self.name}] Processing: {input_text}")
        try:
            # Execute the agent using the runner
            response = self.runner.run(input_text)
            
            # Extract the answer. Assuming response is the final text or has a text attribute.
            # Adjust this based on actual ADK response structure if needed.
            answer = str(response)
            
            return {
                "answer": answer,
                "steps": [] # Steps capture might require different ADK configuration
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return {"answer": f"Error processing request: {str(e)}", "steps": []}

    def get_tool_definitions(self) -> List[Dict]:
        """Returns JSON schema of tools for inspection."""
        return [tool.__name__ for tool in self.tools]
