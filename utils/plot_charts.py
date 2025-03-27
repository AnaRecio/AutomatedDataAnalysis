import matplotlib.pyplot as plt
import os

def plot_stock_prices(data: dict, save_path: str = "charts/stock_prices.png"):
    """
    Generates and saves a horizontal bar chart showing stock prices for each company.

    Args:
        data (dict): Dictionary in the form { "Company": price }
        save_path (str): File path to save the generated chart image
    """
    # Extract keys and values from the input data
    companies = list(data.keys())
    prices = list(data.values())

    # Set figure size and bar color
    plt.figure(figsize=(8, 4))
    bars = plt.bar(companies, prices, color="steelblue")
    plt.ylabel("Stock Price (USD)")
    plt.title("Current Stock Prices (Q1 2025)")
    plt.tight_layout()

    # Annotate bars with their respective price values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + 0.15, yval + 2, f"${yval:.2f}", fontsize=8)

    # Ensure directory exists before saving
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save and close the chart
    plt.savefig(save_path, dpi=150)
    plt.close()

