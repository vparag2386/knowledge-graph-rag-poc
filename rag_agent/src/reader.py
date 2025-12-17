"""Wiki.js GraphQL Client to fetch pages."""
import requests
from typing import List, Dict
from llama_index.core import Document
from .config import WIKI_URL, WIKI_API_KEY


class WikiReader:
    """Reads pages from Wiki.js via GraphQL API."""
    
    def __init__(self):
        self.api_url = f"{WIKI_URL}/graphql"
        self.headers = {
            "Authorization": f"Bearer {WIKI_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def fetch_all_pages(self) -> List[Document]:
        """Fetch all pages from Wiki.js and convert to LlamaIndex Documents."""
        # First, get the list of all pages
        list_query = """
        query {
          pages {
            list {
              id
              path
            }
          }
        }
        """
        
        try:
            response = requests.post(
                self.api_url,
                json={"query": list_query},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"GraphQL Error: {data['errors']}")
            
            page_list = data["data"]["pages"]["list"]
            documents = []
            
            # Fetch each page individually to get content
            for page_info in page_list:
                page_query = """
                query ($id: Int!) {
                  pages {
                    single(id: $id) {
                      id
                      path
                      title
                      description
                      content
                    }
                  }
                }
                """
                
                page_response = requests.post(
                    self.api_url,
                    json={"query": page_query, "variables": {"id": page_info["id"]}},
                    headers=self.headers
                )
                page_response.raise_for_status()
                page_data = page_response.json()
                
                if "errors" in page_data:
                    print(f"Warning: Could not fetch page {page_info['id']}: {page_data['errors']}")
                    continue
                
                page = page_data["data"]["pages"]["single"]
                
                # Create LlamaIndex Document
                doc = Document(
                    text=page["content"],
                    metadata={
                        "id": page["id"],
                        "path": page["path"],
                        "title": page["title"],
                        "description": page.get("description", "")
                    }
                )
                documents.append(doc)
            
            print(f"Fetched {len(documents)} pages from Wiki.js")
            return documents
            
        except Exception as e:
            print(f"Error fetching pages: {e}")
            raise
