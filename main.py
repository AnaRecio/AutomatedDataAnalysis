import os
from utils.fetch_news import fetch_news_articles
from agents.summarizer_agent import summarize_articles
from agents.investment_advisor import compare_investments
from utils.generate_pdf import markdown_to_pdf
from langchain_openai import ChatOpenAI
from utils.config import OPENAI_API_KEY, SERPER_API_KEY

print("[DEBUG] OPENAI_API_KEY:", OPENAI_API_KEY[:6], "...")
print("[DEBUG] SERPER_API_KEY:", SERPER_API_KEY[:6], "...")



# Create folders if not exist
os.makedirs("reports", exist_ok=True)

def main():
    faangs = ["Apple", "Amazon", "Meta", "Google", "Netflix"]
    all_articles = {}
    all_summaries = {}

    print("\n🚀 Starting Automated FAANG Analysis...\n")

    for company in faangs:
        print(f"🔍 Fetching news for {company}...")
        articles = fetch_news_articles(f"{company} stock Q1 2025 outlook")
        all_articles[company] = articles

        print(f"✍️ Summarizing news for {company}...")
        summary = summarize_articles(company, articles)
        all_summaries[company] = summary
        print(f"✅ Done: {company}\n")

    print("🧠 Generating investment recommendation...\n")
    final_analysis = compare_investments(all_summaries)

    # Save markdown report
    report_path = "reports/investment_report_q1_2025.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📈 FAANG Investment Report - Q1 2025\n\n")
        for company in faangs:
            f.write(f"## {company}\n")
            f.write(all_summaries[company] + "\n\n")
        f.write("## 📊 Final Investment Recommendation\n\n")
        f.write(final_analysis)

    print(f"✅ Markdown report saved at {report_path}")

    markdown_to_pdf(report_path)


if __name__ == "__main__":
    main()

