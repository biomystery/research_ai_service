import os
import json
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict

# Configuration
from config import Config

def fetch_url_content(url: str) -> bytes:
    """Helper to fetch URL content using urllib."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_pubmed_abstracts(query: str, max_results: int = Config.RETMAX) -> List[Dict]:
    """
    Fetches abstracts from PubMed using the E-utilities API (via urllib).
    """
    print(f"Fetching PubMed abstracts for query: {query}")
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # 1. ESearh to get IDs
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
        "email": Config.EMAIL
    })
    search_url = f"{base_url}/esearch.fcgi?{params}"
    
    content = fetch_url_content(search_url)
    if not content:
        return []
        
    try:
        data = json.loads(content)
        id_list = data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        print(f"Error parsing PubMed search results: {e}")
        return []

    if not id_list:
        print("No results found.")
        return []

    # 2. EFetch to get details
    ids_str = ",".join(id_list)
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml",
        "email": Config.EMAIL
    })
    fetch_url = f"{base_url}/efetch.fcgi?{params}"
    
    content = fetch_url_content(fetch_url)
    if not content:
        return []

    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"Error parsing PubMed details: {e}")
        return []

    articles = []
    for article in root.findall(".//PubmedArticle"):
        try:
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No Title"
            
            abstract_elem = article.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available."
            
            pmid_elem = article.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else "Unknown"
            
            # Extract Journal
            journal_elem = article.find(".//Journal/Title")
            journal = journal_elem.text if journal_elem is not None else "Unknown Journal"

            # Extract Publication Date
            pub_date_elem = article.find(".//PubDate")
            pub_date = "Unknown Date"
            if pub_date_elem is not None:
                year = pub_date_elem.find("Year")
                medline_date = pub_date_elem.find("MedlineDate")
                if year is not None:
                    pub_date = year.text
                    month = pub_date_elem.find("Month")
                    day = pub_date_elem.find("Day")
                    if month is not None:
                        pub_date += f"-{month.text}"
                    if day is not None:
                        pub_date += f"-{day.text}"
                elif medline_date is not None:
                    pub_date = medline_date.text

            # Extract Authors
            authors = []
            author_list = article.findall(".//AuthorList/Author")
            for author in author_list:
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None:
                    name = last_name.text
                    if fore_name is not None:
                        name = f"{fore_name.text} {name}"
                    authors.append(name)
            
            articles.append({
                "source": "PubMed",
                "id": pmid,
                "title": title,
                "content": abstract,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "journal": journal,
                "publication_date": pub_date,
                "authors": authors
            })
        except Exception:
            continue
            
    print(f"Fetched {len(articles)} articles from PubMed.")
    return articles

def fetch_clinical_trials(query: str, max_results: int = Config.RETMAX) -> List[Dict]:
    """
    Fetches clinical trials from ClinicalTrials.gov API v2 (via urllib).
    """
    print(f"Fetching Clinical Trials for query: {query}")
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = urllib.parse.urlencode({
        "query.term": query,
        "pageSize": max_results,
        "format": "json"
    })
    url = f"{base_url}?{params}"
    
    content = fetch_url_content(url)
    if not content:
        return []
    
    try:
        data = json.loads(content)
    except Exception as e:
        print(f"Error parsing Clinical Trials data: {e}")
        return []

    studies = []
    if "studies" in data:
        for study in data["studies"]:
            try:
                protocol = study.get("protocolSection", {})
                id_module = protocol.get("identificationModule", {})
                nct_id = id_module.get("nctId", "Unknown")
                title = id_module.get("officialTitle") or id_module.get("briefTitle", "No Title")
                
                desc_module = protocol.get("descriptionModule", {})
                summary = desc_module.get("briefSummary", "No summary available.")
                
                studies.append({
                    "source": "ClinicalTrials.gov",
                    "id": nct_id,
                    "title": title,
                    "content": summary,
                    "url": f"https://clinicaltrials.gov/study/{nct_id}"
                })
            except Exception:
                continue
                
    print(f"Fetched {len(studies)} studies from ClinicalTrials.gov.")
    return studies

def main():
    # Define search terms relevant to Treg therapy
    queries = [
        "Treg cell therapy",
        "CAR-Treg",
        "regulatory T cell ex vivo expansion",
        "low dose IL-2 Treg"
    ]
    
    all_data = []
    
    for q in queries:
        # PubMed
        pm_data = fetch_pubmed_abstracts(q, max_results=5)
        all_data.extend(pm_data)
        time.sleep(1) # Respect API rate limits
        
        # Clinical Trials
        ct_data = fetch_clinical_trials(q, max_results=5)
        all_data.extend(ct_data)
        time.sleep(1)

    # Deduplicate based on ID
    unique_data = {item['id']: item for item in all_data}.values()
    
    output_file = "backend/data/raw_data.json"
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(list(unique_data), f, indent=2)
        
    print(f"Successfully saved {len(unique_data)} records to {output_file}")

if __name__ == "__main__":
    main()
