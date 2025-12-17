"""Wikipedia Reader to fetch articles via MediaWiki API."""
import wikipedia
from typing import List, Optional
from llama_index.core import Document


class WikipediaReader:
    """Reads articles from Wikipedia using the MediaWiki API."""
    
    def __init__(self, language: str = "en", max_articles: int = 10):
        """
        Initialize Wikipedia reader.
        
        Args:
            language: Wikipedia language code (default: "en")
            max_articles: Maximum number of articles to fetch per topic
        """
        self.language = language
        self.max_articles = max_articles
        wikipedia.set_lang(language)
    
    def search_articles(self, topic: str, limit: Optional[int] = None) -> List[str]:
        """
        Search for articles related to a topic.
        
        Args:
            topic: Search query/topic
            limit: Maximum number of results (uses max_articles if not specified)
            
        Returns:
            List of article titles
        """
        limit = limit or self.max_articles
        try:
            results = wikipedia.search(topic, results=limit)
            print(f"Found {len(results)} articles for topic: {topic}")
            return results
        except Exception as e:
            print(f"Error searching for topic '{topic}': {e}")
            return []
    
    def fetch_article(self, title: str) -> Optional[Document]:
        """
        Fetch a single Wikipedia article by title.
        
        Args:
            title: Article title
            
        Returns:
            LlamaIndex Document or None if fetch fails
        """
        try:
            page = wikipedia.page(title, auto_suggest=False)
            
            # Create LlamaIndex Document
            doc = Document(
                text=page.content,
                metadata={
                    "title": page.title,
                    "url": page.url,
                    "summary": page.summary,
                    "categories": page.categories if hasattr(page, 'categories') else [],
                    "source": "wikipedia",
                    "language": self.language
                }
            )
            return doc
            
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation page for '{title}'. Options: {e.options[:5]}")
            # Try the first option
            if e.options:
                return self.fetch_article(e.options[0])
            return None
            
        except wikipedia.exceptions.PageError:
            print(f"Page not found: {title}")
            return None
            
        except Exception as e:
            print(f"Error fetching article '{title}': {e}")
            return None
    
    def fetch_articles_by_topic(self, topic: str, limit: Optional[int] = None) -> List[Document]:
        """
        Fetch multiple articles related to a topic.
        
        Args:
            topic: Search query/topic
            limit: Maximum number of articles to fetch
            
        Returns:
            List of LlamaIndex Documents
        """
        article_titles = self.search_articles(topic, limit)
        documents = []
        
        for title in article_titles:
            print(f"Fetching article: {title}")
            doc = self.fetch_article(title)
            if doc:
                documents.append(doc)
        
        print(f"Successfully fetched {len(documents)} articles")
        return documents
    
    def fetch_articles_by_titles(self, titles: List[str]) -> List[Document]:
        """
        Fetch specific articles by their titles.
        
        Args:
            titles: List of article titles
            
        Returns:
            List of LlamaIndex Documents
        """
        documents = []
        
        for title in titles:
            print(f"Fetching article: {title}")
            doc = self.fetch_article(title)
            if doc:
                documents.append(doc)
        
        print(f"Successfully fetched {len(documents)} articles")
        return documents
