# Treg Research Assistant

A RAG-powered "Concierge Agent" for Treg cell therapy research, built for the Kaggle Agents Intensive Capstone.

## Overview
This agent assists bioinformaticians by:
- Retrieving relevant literature from PubMed.
- Finding clinical trials from ClinicalTrials.gov.
- Answering questions about experiment design (e.g., flow cytometry panels, cytokine cocktails).

## Quick Start

### Backend
1.  `cd backend`
2.  `pip install -r requirements.txt`
3.  `export GOOGLE_API_KEY="your-key"`
4.  `python data_ingestion.py` (Fetch data)
5.  `python api_server.py` (Start server)

### Frontend
1.  `cd frontend`
2.  `npm install`
3.  `npm run dev`

## Tech Stack
- **Backend**: Python, FastAPI, LlamaIndex, ChromaDB.
- **AI Engine**: Google Gemini (via `llama-index-llms-gemini`).
- **Frontend**: React, Vite, TailwindCSS.
- **Data**: PubMed E-utilities, ClinicalTrials.gov API.
