from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from utils.config import OPENAI_API_KEY

# Default LLM instance used across the application for consistency
llm = ChatOpenAI(
    temperature=0.4,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def compare_investments(summaries: dict[str, str], model=llm) -> str:
    """
    Uses an LLM to compare company summaries and produce a ranked investment outlook.

    Args:
        summaries (dict): { "CompanyName": "LLM-generated summary" }
        model: Optional override of the default LLM instance.

    Returns:
        str: Markdown-formatted analysis ranking investment opportunities.
    """
    if not summaries:
        return "No company summaries provided to generate investment advice."

    # Concatenate company summaries into one structured string for prompt context
    company_summary_block = "\n\n".join(
        [f"**{company}**:\n{summary.strip()}" for company, summary in summaries.items()]
    )

    # Prompt to guide the LLM in generating a ranked, professional outlook
    prompt_template = ChatPromptTemplate.from_template("""
You are a senior investment analyst creating a summary for an internal strategy memo.

Using the company summaries below, generate:

1. A **ranked list (1st to 5th)** showing which companies are the best investments in Q1 2025.
2. A **brief justification** (1-2 sentences) per company.
3. A final **overall recommendation** or warning for investors.

Be concise, professional, and use markdown formatting with bold, bullets, or headers where appropriate.

Company Summaries:
{company_summary_block}
""")

    # Format the prompt and invoke the model
    prompt = prompt_template.format_messages(company_summary_block=company_summary_block)
    response = model.invoke(prompt)

    return response.content



