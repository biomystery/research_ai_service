# Google ADK Migration Plan

## Current Status (Dec 1, 2024)

### ✅ Immediate Bug Fixed
The error `Could not convert 'part.function_call' to text` has been fixed by adding proper error handling in `backend/agents/base.py`.

### Current Implementation
- Using `google-generativeai` SDK with manual function calling implementation
- Custom `BaseAgent` class that handles tool execution
- Works, but not using the official Google ADK framework

## Migration to Google ADK

### Why Migrate?
1. **Official Framework**: Google ADK (`google-adk`) is the official agent development kit
2. **Better Abstractions**: Built-in `Agent` class with automatic tool handling
3. **Multi-Agent Support**: Native support for agent orchestration
4. **Deployment Ready**: Designed for Vertex AI Agent Engine deployment

### Installation
```bash
pip install google-adk
```
✅ Already installed

### Key Differences

#### Current Approach (google-generativeai)
```python
from google.generativeai import GenerativeModel

model = GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    tools=[tool1, tool2]
)
# Manual function calling loop required
```

#### Google ADK Approach
```python
from google.adk.agents.llm_agent import Agent

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='my_agent',
    description="Agent description",
    instruction="System instruction",
    tools=[tool1, tool2]
)
# Automatic function calling handled by ADK
```

### Migration Steps

#### 1. Update BaseAgent to use ADK
**File:** `backend/agents/base.py`

```python
from google.adk.agents.llm_agent import Agent as ADKAgent
from typing import List, Callable, Optional, Dict, Any

class BaseAgent:
    def __init__(
        self,
        name: str,
        model_name: str,
        tools: Optional[List[Callable]] = None,
        system_instruction: Optional[str] = None
    ):
        self.name = name
        self.agent = ADKAgent(
            model=model_name,
            name=name,
            description=f"{name} agent",
            instruction=system_instruction or "",
            tools=tools or []
        )
    
    def query(self, input_text: str, session_id: str = None) -> Dict[str, Any]:
        # ADK handles function calling automatically
        response = self.agent.run(input_text)
        return {
            "answer": response.text,
            "steps": []
        }
```

#### 2. Update Tool Definitions
ADK tools should return simple types or dicts. Current tools already compatible:

```python
def search_pubmed(query: str) -> str:
    """Searches PubMed for medical abstracts."""
    results = fetch_pubmed_abstracts(query, max_results=5)
    return json.dumps(results, indent=2)
```

#### 3. Update Orchestrator Pattern
**File:** `backend/agents/orchestrator.py`

```python
from google.adk.agents.llm_agent import Agent
from backend.agents.researcher import ResearcherAgent
from backend.agents.analyst import AnalystAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        
        # Define delegation tools
        def ask_researcher(question: str) -> str:
            """Delegates research questions to the Researcher Agent."""
            result = self.researcher.query(question)
            return result["answer"]
        
        def ask_analyst(task: str) -> str:
            """Delegates analysis tasks to the Analyst Agent."""
            result = self.analyst.query(task)
            return result["answer"]
        
        super().__init__(
            name="Orchestrator",
            model_name=Config.ORCHESTRATOR_MODEL,
            tools=[ask_researcher, ask_analyst],
            system_instruction="""
            You are the Treg Research Assistant Orchestrator.
            Delegate to specialized agents as needed.
            """
        )
```

### Testing the Migration

1. **Backup current working code**:
   ```bash
   git add -A
   git commit -m "Working version before ADK migration"
   ```

2. **Create a test branch**:
   ```bash
   git checkout -b feature/adk-migration
   ```

3. **Implement changes incrementally**:
   - Start with BaseAgent
   - Test with simple queries
   - Update sub-agents
   - Test orchestration

4. **Validate**:
   ```bash
   python -m backend.api_server
   # Test with: "Find Phase 2 trials for Tregs"
   ```

### Benefits After Migration

1. **Cleaner Code**: Less boilerplate for function calling
2. **Better Error Handling**: ADK handles edge cases
3. **Deployment**: Easy integration with Vertex AI Agent Engine
4. **Observability**: Built-in logging and tracing
5. **Evaluation**: ADK includes evaluation framework

### Current Workaround (Temporary)

The current implementation with `google-generativeai` + manual function calling works fine for development. The bug fix applied ensures stable operation.

**Recommendation**: 
- ✅ Use current implementation for capstone submission (deadline: Dec 1, 11:59 AM PT)
- 🔄 Migrate to ADK post-submission for production deployment

## References

- [Google ADK Documentation](https://google.github.io/adk-docs)
- [Python Quickstart](https://google.github.io/adk-docs/get-started/python/)
- [Agent API Reference](https://google.github.io/adk-docs/api/python/agents/)
- [Tools Documentation](https://google.github.io/adk-docs/tools/)
