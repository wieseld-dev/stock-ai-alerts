import requests
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# API keys (replace these with your actual environment variables or hardcoded keys if needed)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")  # FINNHUB_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")    # OPENAI_API_KEY

# Create an OpenAI client instance using your API key
client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_recent_news(ticker: str, days: int = 7):
    """
    Fetches recent company news for a given stock ticker using the Finnhub API.
    The default time window is the last 7 days.

    Args:
        ticker (str): The stock symbol (e.g., "AAPL").
        days (int): Number of days of news to fetch. Default is 7.

    Returns:
        list: A list of recent news articles, or an empty list if the request fails.
    """
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)

    url = (
        f"https://finnhub.io/api/v1/company-news?"
        f"symbol={ticker}&from={start_date}&to={today}&token={FINNHUB_API_KEY}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()  # Raise exception for non-200 responses
        return resp.json() or []
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []


def summarize_with_ai(ticker: str, news_items: list):
    """
    Sends recent company news to OpenAI for financial impact analysis.
    The AI returns a short recommendation (Buy / Sell / Hold).

    Args:
        ticker (str): The stock symbol.
        news_items (list): A list of news dictionaries from Finnhub.

    Returns:
        str or None: A short AI-generated summary or None if failed.
    """
    if not news_items:
        return None

    # Take up to 3 most recent news articles for context
    news_texts = [
        f"{n.get('headline', '')} - {n.get('summary', '')}"
        for n in news_items[:3]
    ]
    combined_text = "\n".join(news_texts)

    # Prompt that instructs the AI to act as a financial analyst
    prompt = f"""
    You are an AI financial analyst.
    Analyze the following recent news about {ticker}.
    Decide if the impact on the stock price could be significant.
    Respond in 1–2 sentences with a clear suggestion (Buy / Sell / Hold).

    News:
    {combined_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing with AI for {ticker}: {e}")
        return None


def ai_infer_ticker(ticker: str):
    """
       Main function to analyze a stock ticker.
       Fetches news, runs AI summarization, and returns the recommendation.

       Args:
           ticker (str): The stock symbol (e.g., "TSLA").

       Returns:
           str: AI recommendation or message if analysis fails.
       """
    news = fetch_recent_news(ticker)
    if not news:
        # No news = no analysis
        return None

    summary = summarize_with_ai(ticker, news)

    # Return None if AI didn’t produce output
    return summary if summary else None
