import requests
from utils.config import SERPER_API_KEY
from utils.clean_text import clean_snippet

def fetch_news_articles(query: str, num_results: int = 5) -> list[dict]:
    """
    Fetches news articles from Serper.dev (Google Search API).
    Returns a list of dicts with: title, snippet, link.
    """
    url = "https://google.serper.dev/news"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }

    try:
        # Send POST request to Serper's news endpoint
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()

        articles = []
        # Parse and clean the top `num_results` news items
        for item in results.get("news", [])[:num_results]:
            articles.append({
                "title": item.get("title", "").strip(),
                "link": item.get("link", "").strip(),
                "snippet": clean_snippet(item.get("snippet", ""))
            })

        return articles

    except requests.exceptions.HTTPError as e:
        # Log HTTP error and return empty result
        print(f"Serper API error: {e}")
        print(f"Response message: {response.text}")
        return []



