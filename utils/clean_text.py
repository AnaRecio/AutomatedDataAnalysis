import re
from typing import List, Dict

# Regex patterns to remove junk phrases from snippets
JUNK_PATTERNS = [
    r"(Read more.*)", 
    r"(Click here.*)", 
    r"(Full story.*)", 
    r"https?:\/\/\S+"  # Remove URLs
]

def clean_snippet(snippet: str) -> str:
    """
    Cleans a raw text snippet from a news source.

    Steps:
    - Strips junk content (links, read-more phrases, etc.)
    - Removes duplicate adjacent words
    - Normalizes spacing
    - Optionally capitalizes the first character

    Args:
        snippet (str): The raw snippet string

    Returns:
        str: Cleaned and normalized text
    """
    if not snippet:
        return ""

    # Remove predefined noise patterns
    for pattern in JUNK_PATTERNS:
        snippet = re.sub(pattern, "", snippet, flags=re.IGNORECASE)

    # Collapse duplicate adjacent words (e.g., "Apple Apple stock" → "Apple stock")
    snippet = re.sub(r'\b(\w+)( \1\b)+', r'\1', snippet)

    # Normalize whitespace
    snippet = re.sub(r'\s+', ' ', snippet).strip()

    # Capitalize first character (for better readability)
    if snippet:
        snippet = snippet[0].upper() + snippet[1:]

    return snippet


def clean_articles(articles: List[Dict]) -> List[Dict]:
    """
    Cleans a list of article dictionaries by processing the 'snippet' field.

    Args:
        articles (List[Dict]): Each dict contains 'title', 'link', 'snippet'

    Returns:
        List[Dict]: Same structure with cleaned 'snippet'
    """
    cleaned = []
    for article in articles:
        cleaned.append({
            "title": article.get("title", "").strip(),
            "link": article.get("link", "").strip(),
            "snippet": clean_snippet(article.get("snippet", ""))
        })
    return cleaned


