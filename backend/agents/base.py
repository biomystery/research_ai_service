from typing import List, Callable, Optional, Dict, Any
import vertexai
from vertexai.preview import reasoning_engines
from backend.config import Config

class BaseAgent:
    """
    Base class for all agents in the system.
    Wraps Vertex AI Reasoning Engine patterns.
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
        
        # Initialize Vertex AI
        vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
        
        # Create the underlying LangChain/Reasoning Engine agent
        # Note: In a real ADK deployment, we might use reasoning_engines.LangchainAgent
        # or a custom defined class. For this capstone, we'll use the high-level abstraction.
        self.agent = reasoning_engines.LangchainAgent(
            model=self.model_name,
            tools=self.tools,
            system_instruction=self.system_instruction,
            agent_executor_kwargs={"return_intermediate_steps": True}
        )

    def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Executes a query against the agent.
        """
        print(f"[{self.name}] Processing: {input_text}")
        try:
            response = self.agent.query(input=input_text)
            return {
                "answer": response.get("output", "No output generated."),
                "steps": response.get("intermediate_steps", [])
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return {"answer": f"Error processing request: {str(e)}", "steps": []}

    def get_tool_definitions(self) -> List[Dict]:
        """Returns JSON schema of tools for inspection."""
        # This is a placeholder if we need to expose tool schemas to the UI
        return [tool.__name__ for tool in self.tools]
