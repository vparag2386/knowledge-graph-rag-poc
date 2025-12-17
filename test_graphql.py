import requests
import json

url = "http://localhost:3000/graphql"
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOjEsImdycCI6MSwiaWF0IjoxNzY0NTA0MDE3LCJleHAiOjE3OTYwNjE2MTcsImF1ZCI6InVybjp3aWtpLmpzIiwiaXNzIjoidXJuOndpa2kuanMifQ.cj26tB12QNYhNQvpER-XgZEtA6OzD__BCFPPmkbCe-S8G3xGwvTDkZeJIJBgZJo9NbuF2E_I3xPARkumJb2I1wni1j76SkhCcg9VOFoben-qUTPYY0jh5mmrZtg88dKt1LGHmZZVrfZxd1TTLwT7d2ArSd1JAD4DwccjwS40iQPSbcueIKGfAlkwBZRaGTqd99lAiA2wz-9xqglp30OsNpb9_91ZqtqeKHVfadv51w2EPWc_wYbrd6VK9dWHfZDFG0RhFrwk2jwnzZIdohoSQIHmrQ0QdSoGsjYoKu-5peLyXty218oCn3JKIZ2CNzsmag6XQpQLN7hyd0k99UZCFg",
    "Content-Type": "application/json"
}

query = """
query {
  pages {
    list {
      id
      path
      title
      content
    }
  }
}
"""

response = requests.post(url, json={"query": query}, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
