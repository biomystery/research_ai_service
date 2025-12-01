# Setup Guide - Treg Research Assistant

## Prerequisites
- Python 3.9+
- Node.js 16+
- Google API Key (Gemini)

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the **project root** (`/Users/fcheng/projects/capstone_project/.env`):

```ini
GOOGLE_API_KEY="your_actual_google_api_key_here"
EMAIL="your_email@example.com"
PROJECT_ID="your_google_cloud_project_id"
LOCATION="us-central1"
ORCHESTRATOR_MODEL="gemini-1.5-pro-001"
RESEARCHER_MODEL="gemini-1.5-flash-001"
ANALYST_MODEL="gemini-1.5-flash-001"
DATA_STORE_ID="treg-data-store"
RETMAX="20"
```

**Important:** Replace `your_actual_google_api_key_here` with your real Gemini API key.

### 3. Fetch Data (Optional)
```bash
cd /Users/fcheng/projects/capstone_project
python -m backend.data_ingestion
```

### 4. Start the Backend Server
**Always run from the project root:**
```bash
cd /Users/fcheng/projects/capstone_project
python -m backend.api_server
```

The server will start on `http://localhost:8000`

**API Endpoints:**
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `POST /chat` - Main chat endpoint

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Frontend
```bash
npm run dev
```

The frontend will typically run on `http://localhost:5173`

## Troubleshooting

### "Mock response: Agent dependencies not found"
This means the backend couldn't import the agents. Make sure:
1. You're running the server from the **project root** using `python -m backend.api_server`
2. Your `.env` file has a valid `GOOGLE_API_KEY`

### "ModuleNotFoundError: No module named 'backend.agents'"
You're running the server from the wrong directory. Always run from:
```bash
cd /Users/fcheng/projects/capstone_project
python -m backend.api_server
```

### Port 8000 already in use
Kill the existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

## Architecture

- **Backend:** FastAPI + Google Generative AI SDK
- **Frontend:** React + Vite + TailwindCSS
- **Agents:**
  - `OrchestratorAgent` (Gemini 1.5 Pro) - Main coordinator
  - `ResearcherAgent` (Gemini 1.5 Flash) - Literature search
  - `AnalystAgent` (Gemini 1.5 Flash) - Data analysis
