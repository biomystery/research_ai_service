import os
import json
from typing import List
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# Configuration
DATA_PATH = "backend/data/raw_data.json"
PERSIST_DIR = "backend/storage"

# Ensure GOOGLE_API_KEY is set
# os.environ["GOOGLE_API_KEY"] = "AIza..."

def load_documents() -> List[Document]:
    """Loads data from the raw JSON file and converts to LlamaIndex Documents."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
        
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        
    documents = []
    for item in data:
        # Create a text representation that includes metadata for the LLM to read
        text = f"Title: {item['title']}\nSource: {item['source']}\nID: {item['id']}\nContent: {item['content']}"
        
        doc = Document(
            text=text,
            metadata={
                "source": item['source'],
                "title": item['title'],
                "url": item['url'],
                "id": item['id']
            }
        )
        documents.append(doc)
    
    print(f"Loaded {len(documents)} documents.")
    return documents

def initialize_index(force_rebuild: bool = False):
    """Creates or loads the vector index."""
    
    # Use Google Gemini for embeddings and generation
    # model_name defaults to "models/gemini-1.5-flash" or similar, check docs for latest
    Settings.llm = Gemini(model="models/gemini-1.5-flash")
    Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")

    if os.path.exists(PERSIST_DIR) and not force_rebuild:
        print("Loading index from storage...")
        from llama_index.core import StorageContext, load_index_from_storage
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    else:
        print("Creating new index...")
        documents = load_documents()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        
    return index

class TregAgent:
    def __init__(self):
        self.index = initialize_index()
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=5,
            response_mode="compact"
        )

    def query(self, question: str):
        print(f"Agent querying: {question}")
        response = self.query_engine.query(question)
        return {
            "answer": str(response),
            "sources": [
                node.metadata for node in response.source_nodes
            ]
        }

if __name__ == "__main__":
    # Test run
    agent = TregAgent()
    response = agent.query("What are the optimal conditions for Treg expansion?")
    print("\nAnswer:", response["answer"])
    print("\nSources:", response["sources"])
