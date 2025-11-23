# Implementation Plan - Treg Research Assistant

# Goal Description
Build a "Concierge Agent" for Treg cell therapy research. The agent will assist bioinformaticians and immunologists by retrieving relevant literature and clinical trial data to suggest experiment designs (e.g., flow cytometry panels, cytokine cocktails). It uses a RAG (Retrieval-Augmented Generation) architecture to ground answers in real scientific data.

## User Review Required
> [!IMPORTANT]
> **API Keys**: This project requires access to Google Gemini API. Please ensure you have a valid `GOOGLE_API_KEY`.
> **Data Scope**: We will limit the initial scrape to a specific set of keywords (e.g., "Treg", "Regulatory T cell", "FoxP3") to keep the vector store manageable for a 2-week timeline.

## Proposed Changes

### Backend / Data Pipeline
#### [NEW] `data_ingestion.py`
- **Purpose**: Fetch abstracts from PubMed (using `Bio.Entrez`) and study details from ClinicalTrials.gov API.
- **Logic**:
    - Search for "Treg therapy", "CAR-Treg", "IL-2 mutein".
    - Clean and chunk text.
    - Save as JSON/CSV for indexing.

#### [NEW] `backend/config.py`
- **Purpose**: Central configuration for model selection and API keys.
- **Variables**: `MODEL_NAME` (default: "gemini-1.5-pro"), `EMBEDDING_MODEL`, `PROJECT_ID`.

#### [NEW] `backend/agents/base.py`
- **Purpose**: Base class for all agents, implementing tool registration and memory handling patterns from "Lessons Learned".

#### [NEW] `backend/agents/orchestrator.py`
- **Purpose**: Main entry point. Uses `gemini-1.5-pro` to plan and delegate.

#### [NEW] `backend/agents/researcher.py`
- **Purpose**: Specialized agent for RAG. Uses `gemini-1.5-flash`.

#### [MODIFY] `backend/api_server.py`
- **Update**: Initialize Orchestrator with config. Add endpoint to list available models.

### Frontend
#### [MODIFY] `frontend/src/App.jsx`
- **Update**: Add a "Settings" modal or dropdown to select the Model (Pro vs Flash).

## Verification Plan

### Automated Tests
- **Unit Tests**: Test data parsers (PubMed XML parsing) and API endpoints.
- **RAG Evaluation (Ragas)**:
    - **Faithfulness**: Does the answer come from the retrieved context?
    - **Answer Relevance**: Does the answer address the user's query?

### Manual Verification
- **Golden Query Set**: Run a set of 5-10 domain-specific questions (e.g., "List markers for activated Tregs") and verify accuracy against known literature.
- **UI Walkthrough**: Verify chat flow, citation clicking, and responsiveness.
