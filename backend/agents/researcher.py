from backend.agents.base import BaseAgent
from backend.config import Config
from backend.tools.retrieval import search_pubmed, search_clinical_trials

class ResearcherAgent(BaseAgent):
    """
    Specialized agent for gathering scientific information.
    """
    
    def __init__(self):
        super().__init__(
            name="Researcher",
            model_name=Config.RESEARCHER_MODEL,
            tools=[search_pubmed, search_clinical_trials],
            system_instruction="""
            You are a Researcher Agent specialized in Treg cell therapy.
            Your goal is to find accurate scientific information using the provided tools.
            
            When asked to research a topic:
            1. Use `search_pubmed` to find literature.
            2. Use `search_clinical_trials` to find relevant studies.
            3. Synthesize the findings into a concise summary.
            4. Always cite your sources (PMID or NCT ID).
            """
        )
