from typing import List, Callable, Optional, Dict, Any
import google.generativeai as genai
from backend.config import Config
import inspect
import json

class BaseAgent:
    """
    Base class for all agents in the system.
    Uses Google Generative AI SDK with function calling support.
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
        
        # Convert tools to Gemini function declarations
        tool_declarations = []
        self.tool_map = {}  # Map function names to actual functions
        
        if self.tools:
            for tool in self.tools:
                declaration = self._convert_tool_to_declaration(tool)
                tool_declarations.append(declaration)
                self.tool_map[tool.__name__] = tool
        
        # Initialize model with tools if available
        if tool_declarations:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                system_instruction=self.system_instruction,
                tools=tool_declarations
            )
        else:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                system_instruction=self.system_instruction
            )
        
        # Start a chat session
        self.chat = self.model.start_chat(history=[])

    def _convert_tool_to_declaration(self, tool: Callable) -> genai.protos.Tool:
        """Convert a Python function to a Gemini tool declaration."""
        sig = inspect.signature(tool)
        parameters = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # Default to string
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
            
            parameters[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }
            
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        function_declaration = genai.protos.FunctionDeclaration(
            name=tool.__name__,
            description=tool.__doc__ or f"Function {tool.__name__}",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    name: genai.protos.Schema(type=self._get_gemini_type(prop["type"]))
                    for name, prop in parameters.items()
                },
                required=required
            )
        )
        
        return genai.protos.Tool(function_declarations=[function_declaration])

    def _get_gemini_type(self, type_str: str):
        """Convert string type to Gemini Type enum."""
        type_mapping = {
            "string": genai.protos.Type.STRING,
            "integer": genai.protos.Type.INTEGER,
            "number": genai.protos.Type.NUMBER,
            "boolean": genai.protos.Type.BOOLEAN,
            "object": genai.protos.Type.OBJECT,
            "array": genai.protos.Type.ARRAY
        }
        return type_mapping.get(type_str, genai.protos.Type.STRING)

    def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        """
        Executes a query against the agent with automatic function calling.
        """
        print(f"[{self.name}] Processing: {input_text}")
        try:
            response = self.chat.send_message(input_text)
            
            # Handle function calls iteratively
            max_iterations = 5
            iteration = 0
            
            while iteration < max_iterations:
                # Check if the model wants to call a function
                if response.candidates[0].content.parts:
                    part = response.candidates[0].content.parts[0]
                    
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = dict(function_call.args)
                        
                        print(f"[{self.name}] Calling function: {function_name} with args: {function_args}")
                        
                        # Execute the function
                        if function_name in self.tool_map:
                            function_result = self.tool_map[function_name](**function_args)
                            
                            # Send the function result back to the model
                            response = self.chat.send_message(
                                genai.protos.Content(
                                    parts=[genai.protos.Part(
                                        function_response=genai.protos.FunctionResponse(
                                            name=function_name,
                                            response={"result": function_result}
                                        )
                                    )]
                                )
                            )
                            iteration += 1
                        else:
                            print(f"[{self.name}] Warning: Function {function_name} not found")
                            break
                    else:
                        # No more function calls, we have the final answer
                        break
                else:
                    break
            
            # Extract the final text answer - check if text is available
            try:
                answer = response.text
            except ValueError:
                # If response.text fails, try to get text from parts
                answer = "I processed your request but couldn't generate a final response."
                if response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text') and part.text:
                            answer = part.text
                            break
            
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
