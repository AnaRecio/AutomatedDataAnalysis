# utils/fetch_news.py

import requests
from utils.config import SERPER_API_KEY

def fetch_news_articles(query: str, num_results: int = 5):
    """
    Uses Serper.dev (Google Search API) to retrieve relevant article links and snippets.
    
    Parameters:
        query (str): The search query (e.g., "Apple stock Q1 2025").
        num_results (int): Number of articles to retrieve (default is 5).

    Returns:
        List[Dict]: List of articles, each with title, link, and snippet.
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 403:
            print("❌ ERROR: 403 Forbidden. Check your Serper API key or usage limits.")
            print("🔗 Request URL:", url)
            print("📦 Payload:", payload)
            print("🔑 API Key prefix:", SERPER_API_KEY[:6], "... (truncated)")
            print("💬 Response message:", response.text)

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

    except requests.exceptions.RequestException as e:
        print(f"🚨 Request failed: {e}")
        return []

