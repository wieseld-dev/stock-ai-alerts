import pandas as pd

def detect_extreme_events(df, news_sentiment=None):
    """
    Detect extreme financial events and generate human-readable suggestions.
    """
    suggestions = []

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Rule 1: Daily drop > 5%
    drop = (latest["Close"] - prev["Close"]) / prev["Close"]
    if drop < -0.05:
        suggestions.append(
            "🚨 Large drop (>5%) in one day → Suggestion: Be cautious, possible panic selling."
        )
    elif drop > 0.05:
        suggestions.append(
            "🚀 Large spike (>5%) in one day → Suggestion: Momentum strong, but beware of volatility."
        )

    # Rule 2: Unusual trading volume
    avg_volume = df["Volume"].rolling(30).mean().iloc[-1]
    if latest["Volume"] > 2 * avg_volume:
        suggestions.append(
            "📊 Trading volume >2x average → Suggestion: Market is reacting strongly, watch news closely."
        )

    # Rule 3: RSI extremes
    if latest["RSI"] > 80:
        suggestions.append(
            "⚠️ RSI > 80 → Suggestion: Stock is overbought, consider selling or tightening stop-loss."
        )
    elif latest["RSI"] < 20:
        suggestions.append(
            "💡 RSI < 20 → Suggestion: Stock is oversold, possible buying opportunity."
        )

    # Rule 4: Price vs SMA trend
    if pd.notna(latest["SMA20"]):
        if latest["Close"] > latest["SMA20"] * 1.05:
            suggestions.append(
                "📈 Price >5% above SMA20 → Suggestion: Uptrend strong, but price may be overheated."
            )
        elif latest["Close"] < latest["SMA20"] * 0.95:
            suggestions.append(
                "📉 Price >5% below SMA20 → Suggestion: Downtrend forming, be cautious or reduce exposure."
            )

    # Rule 5: News sentiment
    if news_sentiment is not None:
        if news_sentiment < -0.7:
            suggestions.append(
                "📰 Strong negative sentiment → Suggestion: Analysts/news are bearish, consider reducing position."
            )
        elif news_sentiment > 0.7:
            suggestions.append(
                "📰 Strong positive sentiment → Suggestion: Market outlook is bullish, may support holding or buying."
            )

    return suggestions
