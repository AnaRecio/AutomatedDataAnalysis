from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from typing import List, Dict
from utils.config import OPENAI_API_KEY

# Initialize the OpenAI LLM for article summarization
llm = ChatOpenAI(
    temperature=0.4,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def summarize_articles(company: str, articles: List[Dict], model=llm) -> str:
    """
    Uses an LLM to summarize recent news articles for a given company.
    
    Args:
        company (str): Company name
        articles (List[Dict]): List of dicts with 'title' and 'snippet' keys
        model: LangChain LLM instance (optional override)

    Returns:
        str: Bullet-point summary written in a financial analyst tone
    """
    if not articles:
        return f"No articles found for {company}."

    # Flatten and format snippets into a numbered list for better prompt context
    snippets = "\n\n".join(
        [f"{i+1}. {a.get('title', '')}\n{a.get('snippet', '')}" for i, a in enumerate(articles)]
    )

    # LLM prompt template to simulate analyst-style synthesis
    prompt_template = ChatPromptTemplate.from_template("""
You are a senior financial analyst writing a short internal report.

Summarize the news about **{company}** in Q1 2025 by identifying:

- Stock behavior and market reaction
- Earnings or product developments
- Strategic actions or partnerships
- Key risks, controversies, or signals
- Your overall investment sentiment: Positive, Neutral, Negative

Use a concise, structured tone. Max 5 bullet points.

News:
{snippets}
""")

    # Format structured messages for the LLM
    prompt = prompt_template.format_messages(company=company, snippets=snippets)

    # Invoke the model and return raw string content
    response = model.invoke(prompt)
    return response.content


