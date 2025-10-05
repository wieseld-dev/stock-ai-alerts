import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetches historical stock data from Yahoo Finance.

    Args:
        ticker (str): The stock symbol (e.g., "AAPL").
        period (str): The time period to download (e.g., "1y", "6mo", "1d").
        interval (str): The data interval (e.g., "1d", "1h", "15m").

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing the stock data.
                          Columns typically include Open, High, Low, Close, Adj Close, and Volume.
    """
    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=False,  # Do not automatically adjust for splits/dividends
        group_by="column"
    )

    # If the DataFrame has MultiIndex columns (e.g., (Ticker, Column)), remove the outer level
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(-1, axis=1)

    # Keep only relevant financial columns if they exist
    keep = [c for c in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if c in df.columns]

    return df[keep]
