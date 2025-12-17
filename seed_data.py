import requests
import sys

def seed_content(api_url, api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # GraphQL mutation to create a page
    query = """
    mutation ($content: String!, $description: String!, $editor: String!, $isPublished: Boolean!, $locale: String!, $path: String!, $tags: [String]!, $title: String!) {
      pages {
        create (content: $content, description: $description, editor: $editor, isPublished: $isPublished, locale: $locale, path: $path, tags: $tags, title: $title) {
          responseResult {
            succeeded
            errorCode
            slug
            message
          }
        }
      }
    }
    """
    
    pages = [
        {
            "title": "Project Alpha",
            "path": "projects/alpha",
            "content": "<h1>Project Alpha</h1><p>Project Alpha is a secret initiative to build a time machine. The lead engineer is Dr. Emmett Brown.</p>",
            "description": "Details about Project Alpha",
            "tags": ["project", "top-secret"]
        },
        {
            "title": "Project Beta",
            "path": "projects/beta",
            "content": "<h1>Project Beta</h1><p>Project Beta focuses on teleportation. It is currently on hold due to safety concerns.</p>",
            "description": "Details about Project Beta",
            "tags": ["project", "on-hold"]
        },
        {
            "title": "Employee Handbook",
            "path": "hr/handbook",
            "content": "<h1>Employee Handbook</h1><p>All employees must wear a badge at all times. Lunch is from 12 PM to 1 PM.</p>",
            "description": "Company policies",
            "tags": ["hr", "policy"]
        }
    ]
    
    for page in pages:
        variables = {
            "content": page["content"],
            "description": page["description"],
            "editor": "ckeditor",
            "isPublished": True,
            "locale": "en",
            "path": page["path"],
            "tags": page["tags"],
            "title": page["title"]
        }
        
        response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)
        print(f"Creating {page['title']}: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python seed_data.py <api_url> <api_token>")
        sys.exit(1)
        
    api_url = sys.argv[1]
    api_token = sys.argv[2]
    seed_content(api_url, api_token)
