import pandas as pd

def add_sma(df, window=20):
    """
    Adds a Simple Moving Average (SMA) column to the DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing a 'Close' column.
        window (int): The number of periods to use for the SMA. Default is 20.

    Returns:
        pandas.DataFrame: The same DataFrame with an added 'SMA{window}' column.
    """
    df[f"SMA{window}"] = df["Close"].rolling(window=window).mean()
    return df


def add_rsi(df, period=14):
    """
    Adds a Relative Strength Index (RSI) column to the DataFrame.

    RSI measures the magnitude of recent price changes to evaluate
    overbought or oversold conditions.

    Args:
        df (pandas.DataFrame): DataFrame containing a 'Close' column.
        period (int): The number of periods to calculate RSI over. Default is 14.

    Returns:
        pandas.DataFrame: The same DataFrame with an added 'RSI' column.
    """
    delta = df["Close"].diff(1)  # Calculate day-to-day price change
    gain = delta.clip(lower=0)   # Keep only positive changes (gains)
    loss = -1 * delta.clip(upper=0)  # Keep only negative changes (losses as positive values)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss  # Relative Strength
    df["RSI"] = 100 - (100 / (1 + rs))  # RSI formula

    return df
