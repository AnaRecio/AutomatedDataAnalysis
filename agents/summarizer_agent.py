from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from typing import List, Dict
from utils.config import OPENAI_API_KEY

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.4,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def summarize_articles(company: str, articles: List[Dict]) -> str:
    """
    Summarizes multiple articles about a single company using a prompt-engineered LLM.
    """
    content_blocks = "\n\n".join(
        [f"{idx+1}. {article['title']}\n{article['snippet']}" for idx, article in enumerate(articles)]
    )

    prompt = f"""
You are a financial analyst. Based on the following news snippets about {company}, summarize the key points related to:

- Market performance and stock behavior in Q1 2025
- Product launches, strategic moves, or earnings
- Investment risks or red flags
- Overall investment outlook (positive, negative, neutral)

Use professional tone. Be concise and structured. Output should be 3-5 bullet points max.

News Snippets:
{content_blocks}
"""

    messages = [HumanMessage(content=prompt)]
    response = llm(messages)
    return response.content
