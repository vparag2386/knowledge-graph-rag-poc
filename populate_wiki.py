import requests
import json

# Configuration
API_URL = "http://localhost:3000/graphql"
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOjEsImdycCI6MSwiaWF0IjoxNzY0NTA0MDE3LCJleHAiOjE3OTYwNjE2MTcsImF1ZCI6InVybjp3aWtpLmpzIiwiaXNzIjoidXJuOndpa2kuanMifQ.cj26tB12QNYhNQvpER-XgZEtA6OzD__BCFPPmkbCe-S8G3xGwvTDkZeJIJBgZJo9NbuF2E_I3xPARkumJb2I1wni1j76SkhCcg9VOFoben-qUTPYY0jh5mmrZtg88dKt1LGHmZZVrfZxd1TTLwT7d2ArSd1JAD4DwccjwS40iQPSbcueIKGfAlkwBZRaGTqd99lAiA2wz-9xqglp30OsNpb9_91ZqtqeKHVfadv51w2EPWc_wYbrd6VK9dWHfZDFG0RhFrwk2jwnzZIdohoSQIHmrQ0QdSoGsjYoKu-5peLyXty218oCn3JKIZ2CNzsmag6XQpQLN7hyd0k99UZCFg"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# GraphQL Mutation to create a page
CREATE_PAGE_MUTATION = """
mutation ($content: String!, $description: String!, $editor: String!, $isPublished: Boolean!, $isPrivate: Boolean!, $locale: String!, $path: String!, $tags: [String]!, $title: String!) {
  pages {
    create (
      content: $content,
      description: $description,
      editor: $editor,
      isPublished: $isPublished,
      isPrivate: $isPrivate,
      locale: $locale,
      path: $path,
      tags: $tags,
      title: $title
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
        path
        title
      }
    }
  }
}
"""

def create_page(path, title, content, description=""):
    variables = {
        "content": content,
        "description": description,
        "editor": "markdown",
        "isPublished": True,
        "isPrivate": False,
        "locale": "en",
        "path": path,
        "tags": ["sample", "rag-test"],
        "title": title
    }
    
    response = requests.post(API_URL, json={"query": CREATE_PAGE_MUTATION, "variables": variables}, headers=HEADERS)
    
    if response.status_code == 200:
        result = response.json()
        if "errors" in result:
             print(f"Error creating {path}: {result['errors'][0]['message']}")
        else:
            res = result["data"]["pages"]["create"]["responseResult"]
            if res["succeeded"]:
                print(f"Successfully created: {path}")
            else:
                print(f"Failed to create {path}: {res['message']}")
    else:
        print(f"HTTP Error {response.status_code}: {response.text}")

# Hierarchy Data (Space Mission Theme)
hierarchy = [
    {
        "path": "mission-alpha",
        "title": "Mission Alpha",
        "content": "# Mission Alpha\n\nMission Alpha is the first interstellar attempt by the agency. Its goal is to reach Proxima Centauri.",
        "children": [
            {
                "path": "mission-alpha/vehicle",
                "title": "Starship X1",
                "content": "# Starship X1\n\nThe primary vehicle for Mission Alpha. It uses an experimental warp drive.",
                "children": [
                    {
                        "path": "mission-alpha/vehicle/propulsion",
                        "title": "Propulsion System",
                        "content": "# Propulsion System\n\nThe heart of the Starship X1. It consists of the Warp Core and the Impulse Engines.",
                        "children": [
                            {
                                "path": "mission-alpha/vehicle/propulsion/warp-core",
                                "title": "Warp Core",
                                "content": "# Warp Core\n\nGenerates the warp field. Requires Dilithium crystals to operate.",
                                "children": [
                                    {
                                        "path": "mission-alpha/vehicle/propulsion/warp-core/injector",
                                        "title": "Antimatter Injector",
                                        "content": "# Antimatter Injector\n\nInjects antimatter into the reaction chamber. Critical component for maintaining stable warp field."
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "path": "mission-alpha/vehicle/life-support",
                        "title": "Life Support",
                        "content": "# Life Support\n\nMaintains atmosphere and gravity for the crew."
                    }
                ]
            },
            {
                "path": "mission-alpha/crew",
                "title": "Crew Roster",
                "content": "# Crew Roster\n\n1. Commander Shepard\n2. Lt. Ripley\n3. Science Officer Spock"
            }
        ]
    }
]

def process_hierarchy(nodes):
    for node in nodes:
        create_page(node["path"], node["title"], node["content"])
        if "children" in node:
            process_hierarchy(node["children"])

if __name__ == "__main__":
    print("Starting Wiki Population...")
    try:
        process_hierarchy(hierarchy)
        print("Population Complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
