import json
from backend.data_ingestion import fetch_pubmed_abstracts, fetch_clinical_trials

def search_pubmed(query: str) -> str:
    """
    Searches PubMed for medical abstracts related to the query.
    
    Args:
        query: The search keywords (e.g., "Treg cell therapy").
        
    Returns:
        A JSON string containing a list of articles with titles and abstracts.
    """
    results = fetch_pubmed_abstracts(query, max_results=5)
    return json.dumps(results, indent=2)

def search_clinical_trials(query: str) -> str:
    """
    Searches ClinicalTrials.gov for active studies.
    
    Args:
        query: The search keywords.
        
    Returns:
        A JSON string containing a list of clinical trials.
    """
    results = fetch_clinical_trials(query, max_results=5)
    return json.dumps(results, indent=2)
