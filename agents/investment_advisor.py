from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils.config import OPENAI_API_KEY

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.4,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def compare_investments(summaries: dict) -> str:
    """
    Given a dictionary of summaries per company, generates a ranked investment recommendation.
    """
    summary_text = "\n\n".join([f"{company}:\n{summary}" for company, summary in summaries.items()])

    prompt = f"""
You are an experienced investment analyst. Based on the following summaries for FAANG companies, provide:

1. A ranked list from best to worst investment **as of Q1 2025**
2. A short justification (2-3 sentences) for each company
3. Overall recommendation or caution for investors

Make the analysis professional, concise, and suitable for a report.
    
Company Summaries:
{summary_text}
"""

    messages = [HumanMessage(content=prompt)]
    response = llm(messages)
    return response.content
