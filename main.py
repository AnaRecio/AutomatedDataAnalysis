import os
from dotenv import load_dotenv

# Load keys and configurations
from utils.config import OPENAI_API_KEY

# Core business logic modules
from utils.fetch_news import fetch_news_articles
from utils.clean_text import clean_articles
from agents.summarizer_agent import summarize_articles
from agents.investment_advisor import compare_investments
from agents.valuation_agent import generate_valuation_table
from utils.yahoo_finance import fetch_financial_data
from utils.plot_charts import plot_stock_prices
from utils.generate_pdf import markdown_to_pdf

def setup_environment():
    """
    Load environment variables and ensure required folders exist.
    """
    load_dotenv()
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY is not set. Check your .env file.")
    os.makedirs("reports", exist_ok=True)
    os.makedirs("charts", exist_ok=True)

def main():
    """
    Executes the complete FAANG analysis workflow:
    - Fetches news & stock data
    - Generates LLM-based summaries
    - Builds markdown & PDF reports
    """
    setup_environment()

    tickers = {
        "Apple": "AAPL",
        "Amazon": "AMZN",
        "Meta": "META",
        "Google": "GOOGL",
        "Netflix": "NFLX"
    }

    summaries = {}          # Company -> summarized article insights
    stock_metadata = {}     # Company -> Yahoo Finance data
    stock_prices = {}       # Company -> Latest stock price for plotting
    sources = {}            # Company -> List of news article URLs

    print("\nStarting Automated FAANG Analysis...\n")

    for company, ticker in tickers.items():
        print(f"Fetching news and data for {company}...")

        # 1. Get and clean news articles
        articles = fetch_news_articles(f"{company} stock Q1 2025 outlook")
        cleaned_articles = clean_articles(articles)

        # 2. Generate LLM summary
        summary = summarize_articles(company, cleaned_articles)
        summaries[company] = summary

        # 3. Fetch financials
        data = fetch_financial_data(ticker)
        if data:
            stock_metadata[company] = data
            if data.get("current_price"):
                stock_prices[company] = round(data["current_price"], 2)

        # 4. Save original article sources for citation
        sources[company] = [article["link"] for article in articles if article.get("link")]

        print(f"Completed: {company}\n")

    # Generate visual chart of current stock prices
    print("Generating price chart...\n")
    plot_stock_prices(stock_prices)

    # Create final investment ranking using LLM
    print("Generating final investment recommendation...\n")
    final_recommendation = compare_investments(summaries)

    # Create financial valuation summary table and interpretation
    print("Generating valuation table using agent...\n")
    valuation_md, valuation_analysis = generate_valuation_table(stock_metadata)

    # Compose markdown report
    report_path = "reports/investment_report_q1_2025.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# FAANG Investment Report - Q1 2025\n\n")

        for company in tickers:
            f.write(f"## {company}\n")
            f.write(summaries[company] + "\n\n")

        f.write("## Financial Valuation Overview\n\n")
        f.write("\n".join(valuation_md) + "\n\n")

        f.write("## Valuation Analysis\n\n")
        f.write("\n".join(valuation_analysis) + "\n\n")

        f.write("## Final Investment Recommendation\n\n")
        f.write(final_recommendation + "\n\n")

        # Append article sources to the report
        f.write("## Sources\n\n")
        for company, links in sources.items():
            f.write(f"### {company}\n")
            for link in links:
                f.write(f"- {link}\n")
            f.write("\n")

    print(f"Markdown report saved to: {report_path}")

    # Convert the markdown to a polished PDF
    print("Generating PDF version...\n")
    markdown_to_pdf(report_path)

    print("All done!")

if __name__ == "__main__":
    main()



