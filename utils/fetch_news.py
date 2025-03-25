import requests
from utils.config import SERPER_API_KEY

def fetch_news_articles(query: str, num_results: int = 5):
    """
    Uses Serper.dev (Google Search API) to retrieve relevant article links and snippets.
    """
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {
        "q": query,
        "num": num_results
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    results = response.json()
    articles = []

    for item in results.get("news", []):
        articles.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return articles
