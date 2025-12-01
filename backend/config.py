import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Project Settings
    PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
    LOCATION = os.getenv("LOCATION", "us-central1")
    
    # Model Selection
    # Default to Gemini 2.0 Flash for Orchestrator (better reasoning)
    ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemini-2.0-flash-exp")
    
    # Default to Gemini 2.0 Flash for Sub-agents (faster/cheaper)
    RESEARCHER_MODEL = os.getenv("RESEARCHER_MODEL", "gemini-2.0-flash-exp")
    ANALYST_MODEL = os.getenv("ANALYST_MODEL", "gemini-2.0-flash-exp")
    
    # Vertex AI Search
    DATA_STORE_ID = os.getenv("DATA_STORE_ID", "treg-data-store")

    # External APIs
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    EMAIL = os.getenv("EMAIL", "your.email@example.com")
    RETMAX = int(os.getenv("RETMAX", "20"))
    
    @staticmethod
    def get_model_config(agent_type: str):
        if agent_type == "orchestrator":
            return Config.ORCHESTRATOR_MODEL
        elif agent_type == "researcher":
            return Config.RESEARCHER_MODEL
        elif agent_type == "analyst":
            return Config.ANALYST_MODEL
        return Config.ORCHESTRATOR_MODEL
