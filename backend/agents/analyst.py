from backend.agents.base import BaseAgent
from backend.config import Config
from backend.tools.analysis import execute_python_code

class AnalystAgent(BaseAgent):
    """
    Specialized agent for data analysis and code execution.
    """
    
    def __init__(self):
        super().__init__(
            name="Analyst",
            model_name=Config.ANALYST_MODEL,
            tools=[execute_python_code],
            system_instruction="""
            You are an Analyst Agent.
            Your goal is to analyze data, perform calculations, or generate code to solve problems.
            
            When asked to analyze something:
            1. Write Python code to solve the problem.
            2. Use `execute_python_code` to run it.
            3. Interpret the results.
            """
        )
