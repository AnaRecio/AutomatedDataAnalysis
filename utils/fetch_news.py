from langchain.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

def fetch_news_articles(query: str, num_results: int = 5):
    """
    Uses DuckDuckGo to perform a web search for the given query.
    Returns a list of dicts containing dummy 'title', 'link', and 'snippet'.
    DuckDuckGoSearchRun returns a single string summary, so we simulate articles.
    """
    print(f"🌐 Searching DuckDuckGo for: {query}")
    raw_result = search_tool.run(query)

    # Simulate article list from the plain result string
    articles = [{
        "title": f"{query} - Result {i+1}",
        "link": "https://www.duckduckgo.com",
        "snippet": snippet.strip()
    } for i, snippet in enumerate(raw_result.split("\n")) if snippet.strip()][:num_results]

    return articles

