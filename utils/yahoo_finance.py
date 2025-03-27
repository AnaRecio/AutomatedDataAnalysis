import yfinance as yf

def fetch_financial_data(ticker: str) -> dict:
    """
    Fetches current stock data for a given ticker using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "GOOGL")

    Returns:
        dict: Contains current price, market cap, P/E ratio, 52-week range, and company metadata.
    """
    try:
        # Create Ticker object from yfinance
        stock = yf.Ticker(ticker)

        # Retrieve key statistics and company metadata
        info = stock.info

        return {
            "ticker": ticker,
            "current_price": info.get("currentPrice"),
            "previous_close": info.get("previousClose"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "sector": info.get("sector"),
            "short_name": info.get("shortName"),
            "long_name": info.get("longName"),
        }

    except Exception as e:
        # Fallback on API failure
        print(f"Error fetching data for {ticker}: {e}")
        return {}
