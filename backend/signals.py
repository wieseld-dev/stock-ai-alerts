import pandas as pd

# Explanation dictionary for signal meanings
EXPLANATIONS = {
    "SMA20": "Price crossed above SMA20 → Uptrend signal.",
    "RSI_HIGH": "RSI > 70 → Overbought, possible correction.",
    "RSI_LOW": "RSI < 30 → Oversold, possible rebound.",
    "DROP": "Price dropped >5% in one day → Extreme event."
}


def generate_signals(df):
    """
    Generates trading signals based on technical indicators.

    Args:
        df (pandas.DataFrame): DataFrame containing columns:
                               'Close', 'SMA20', and 'RSI'.

    Returns:
        list: A list of tuples, where each tuple contains:
              (signal_description, explanation)
    """
    signals = []

    # Ensure there are enough data points
    if len(df) < 2:
        return signals

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    latest_close = latest["Close"]
    latest_sma20 = latest["SMA20"] if not pd.isna(latest["SMA20"]) else None
    latest_rsi = latest["RSI"] if not pd.isna(latest["RSI"]) else None
    prev_close = prev["Close"]

    # --- SMA-based signal ---
    if latest_sma20 is not None and latest_close > latest_sma20:
        signals.append(("Price above SMA20 → Possible Buy", EXPLANATIONS["SMA20"]))

    # --- RSI-based signals ---
    if latest_rsi is not None and latest_rsi > 70:
        signals.append(("RSI > 70 (Overbought) → Possible Sell", EXPLANATIONS["RSI_HIGH"]))
    if latest_rsi is not None and latest_rsi < 30:
        signals.append(("RSI < 30 (Oversold) → Possible Buy", EXPLANATIONS["RSI_LOW"]))

    # --- Daily percentage change ---
    daily_change = (latest_close - prev_close) / prev_close
    if daily_change < -0.05:
        signals.append(("Price dropped more than 5% in one day", EXPLANATIONS["DROP"]))

    return signals
