from backend.agents.base import BaseAgent
from backend.agents.researcher import ResearcherAgent
from backend.agents.analyst import AnalystAgent
from backend.config import Config

class OrchestratorAgent(BaseAgent):
    """
    Main agent that interfaces with the user and delegates tasks.
    """
    
    def __init__(self):
        # Initialize sub-agents
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        
        # Define delegation tools
        def ask_researcher(question: str) -> str:
            """
            Delegates a research question to the Researcher Agent.
            Use this when you need to find scientific facts, papers, or clinical trials.
            """
            result = self.researcher.query_sync(question)
            return result["answer"]

        def ask_analyst(task: str) -> str:
            """
            Delegates a data analysis or calculation task to the Analyst Agent.
            Use this when you need to calculate stats, plot data, or run code.
            """
            result = self.analyst.query_sync(task)
            return result["answer"]
            
        super().__init__(
            name="Orchestrator",
            model_name=Config.ORCHESTRATOR_MODEL,
            tools=[ask_researcher, ask_analyst],
            system_instruction="""
            You are the Treg Research Assistant Orchestrator.
            Your goal is to help bioinformaticians design experiments and understand Treg biology.
            
            You have access to specialized agents:
            - `ask_researcher`: For literature, facts, and protocols.
            - `ask_analyst`: For calculations, data analysis, or code execution.
            
            If the user asks for general advice or chat, answer directly.
            Always be professional and scientific.
            """
        )
