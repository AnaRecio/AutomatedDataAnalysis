from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from utils.config import OPENAI_API_KEY

# Initialize OpenAI language model for valuation commentary
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def generate_valuation_table(financial_data: dict[str, dict]) -> tuple:
    """
    Builds a markdown-formatted financial valuation table and uses an LLM to generate insights.

    Args:
        financial_data (dict): Dictionary with company name as key and Yahoo Finance data as value

    Returns:
        tuple: (markdown_table as list[str], valuation_analysis as list[str])
    """
    headers = ["Company", "Price", "Market Cap", "P/E Ratio", "52W Low", "52W High"]
    rows = []
    markdown_table = []

    # Helper to format large numbers for readability (e.g., $1.5T, $50B)
    def format_number(value):
        if value >= 1e12:
            return f"${value / 1e12:.2f}T"
        elif value >= 1e9:
            return f"${value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"${value / 1e6:.2f}M"
        return f"${value:.2f}"

    # Extract relevant fields from the financial data
    for company, data in financial_data.items():
        if not data:
            continue
        row = [
            company,
            f"${data.get('current_price', 0):.2f}",
            format_number(data.get("market_cap", 0)),
            f"{data.get('pe_ratio', 0):.2f}",
            f"${data.get('52_week_low', 0):.2f}",
            f"${data.get('52_week_high', 0):.2f}"
        ]
        rows.append(row)

    # Build markdown-formatted table from headers + rows
    markdown_table.append("| " + " | ".join(headers) + " |")
    markdown_table.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        markdown_table.append("| " + " | ".join(row) + " |")

    # Compose plain-text input for LLM prompt
    company_insights = "\n".join([
        f"{row[0]} - Price: {row[1]}, P/E: {row[3]}, Market Cap: {row[2]}"
        for row in rows
    ])

    # Prompt the LLM to analyze and summarize valuation data
    prompt_template = ChatPromptTemplate.from_template("""
You are a financial analyst. Based on the following valuation data, summarize:

1. Which company looks undervalued or overvalued based on P/E ratio and market cap?
2. Highlight notable outliers or comparisons.
3. Provide a concise investment takeaway.

Valuation Data:
{company_insights}
""")

    # Format messages and invoke the LLM
    messages = prompt_template.format_messages(company_insights=company_insights)
    response = llm.invoke(messages)

    # Return markdown table and line-by-line LLM summary
    return markdown_table, response.content.split("\n")


