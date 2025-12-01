from typing import List, Callable, Optional, Dict, Any
import google.generativeai as genai
from backend.config import Config

class BaseAgent:
    """
    Base class for all agents in the system.
    Uses Google Generative AI SDK.
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
        
        # Configure Gemini API
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Initialize the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        # Convert tools to Gemini function declarations if provided
        tool_declarations = []
        if self.tools:
            for tool in self.tools:
                # Extract function metadata for Gemini
                tool_declarations.append(self._convert_tool_to_declaration(tool))
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            system_instruction=self.system_instruction
        )
        
        # Start a chat session
        self.chat = self.model.start_chat(history=[])

    def _convert_tool_to_declaration(self, tool: Callable) -> Dict:
        """Convert a Python function to a Gemini tool declaration."""
        # Basic conversion - you may need to enhance this based on your tools
        return {
            "name": tool.__name__,
            "description": tool.__doc__ or f"Function {tool.__name__}",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

    def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Executes a query against the agent.
        """
        print(f"[{self.name}] Processing: {input_text}")
        try:
            # Send message to the model
            response = self.chat.send_message(input_text)
            
            # Extract the answer
            answer = response.text
            
            return {
                "answer": answer,
                "steps": []
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            import traceback
            traceback.print_exc()
            return {"answer": f"Error processing request: {str(e)}", "steps": []}

    def get_tool_definitions(self) -> List[Dict]:
        """Returns JSON schema of tools for inspection."""
        return [tool.__name__ for tool in self.tools]
