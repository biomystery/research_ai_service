# Fixes Applied - December 1, 2025

## Summary
Fixed the Treg Research Assistant to properly execute function calls instead of generating code snippets, and added markdown rendering to the frontend.

## Issues Resolved

### 1. ✅ Agent Generating Code Instead of Executing Functions
**Problem:** The agent was returning code snippets like:
```python
from agents import ask_researcher
query = "Are there any active Phase 2 clinical trials..."
response = ask_researcher(query)
print(response)
```

**Root Cause:** The `BaseAgent` class wasn't properly implementing Gemini's function calling API.

**Solution:** Completely rewrote `backend/agents/base.py` to:
- Use `genai.protos.Tool` and `genai.protos.FunctionDeclaration` for proper tool registration
- Implement automatic function execution loop that:
  1. Detects when Gemini wants to call a function
  2. Executes the function with the provided arguments
  3. Sends the result back to Gemini
  4. Continues until Gemini provides a final text answer
- Added `inspect` module to automatically extract function signatures and parameters

### 2. ✅ Frontend Not Rendering Markdown
**Problem:** Agent responses with markdown formatting (headers, lists, code blocks) were displayed as plain text.

**Solution:** Updated `frontend/src/App.jsx`:
- Installed `react-markdown` and `remark-gfm` packages
- Added conditional rendering: user messages as plain text, assistant messages as markdown
- Added Tailwind prose classes for proper markdown styling
- Fixed API request to use `model_type` instead of `model_config` (Pydantic v2 compatibility)

### 3. ✅ Model Configuration Updates
**Changed models from:**
- `gemini-1.5-pro-001` → `gemini-2.0-flash-exp`
- `gemini-1.5-flash-001` → `gemini-2.0-flash-exp`

**Files updated:**
- `backend/config.py`
- `.env`
- `frontend/src/App.jsx` (UI labels)

### 4. ✅ Import Path Fixes
**Fixed:**
- `backend/data_ingestion.py`: Changed `from config import Config` → `from backend.config import Config`
- `backend/agents/researcher.py`: Removed non-existent `from google.adk.tools import google_search`

## Files Modified

1. **backend/agents/base.py** - Complete rewrite with function calling support
2. **backend/config.py** - Updated model names to gemini-2.0-flash-exp
3. **backend/data_ingestion.py** - Fixed import path
4. **backend/agents/researcher.py** - Removed google.adk import
5. **backend/api_server.py** - Added root route, improved error messages
6. **frontend/src/App.jsx** - Added markdown rendering
7. **.env** - Updated model configurations

## How Function Calling Now Works

```python
# 1. User asks: "Find Phase 2 trials for Tregs"
# 2. Orchestrator receives the query
# 3. Gemini decides to call: ask_researcher("Find Phase 2 trials for Tregs")
# 4. BaseAgent detects function_call in response
# 5. BaseAgent executes: self.researcher.query("Find Phase 2 trials...")
# 6. BaseAgent sends result back to Gemini
# 7. Gemini synthesizes final answer with the data
# 8. User receives formatted markdown response
```

## Testing

To test the fixes:

1. **Start Backend:**
   ```bash
   cd /Users/fcheng/projects/capstone_project
   python -m backend.api_server
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Query:**
   Ask: "Are there any active Phase 2 clinical trials using ex vivo expanded Tregs?"
   
   Expected: The agent should call `ask_researcher`, get actual results from PubMed/ClinicalTrials, and return a formatted markdown response with citations.

## Note on google.adk

The `google.adk` package referenced in some code comments doesn't exist as a public pip package. The current implementation uses:
- `google-generativeai` (official Google Generative AI Python SDK)
- Direct Gemini API function calling via `genai.protos.Tool`

This approach is production-ready and doesn't require any unreleased or internal Google packages.
