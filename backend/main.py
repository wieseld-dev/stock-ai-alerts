from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from concurrent.futures import ThreadPoolExecutor

# === Local modules ===
from data_fetcher import fetch_stock_data
from indicators import add_sma, add_rsi
from signals import generate_signals
from watchlist import init_watchlist, add_to_watchlist, remove_from_watchlist, get_watchlist
from extreme_engine import detect_extreme_events
from ai_engine import ai_infer_ticker

# Initialize FastAPI application
app = FastAPI()

# === CORS Configuration ===
# Allows the frontend (or any origin during development) to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === API Keys and Global Variables ===
# Replace this with environment variable loading for security in production
FINNHUB_API_KEY = "d37svkhr01qskreho7q0d37svkhr01qskreho7qg"

# Simple in-memory caches for optimization
profile_cache = {}   # Stores company profiles
search_cache = {}    # Stores search results
data_cache = {}      # Can be used for price data (optional)

# Thread pool to perform parallel API calls efficiently
executor = ThreadPoolExecutor(max_workers=5)

# Initialize the watchlist when the server starts
init_watchlist()

# === WATCHLIST ENDPOINTS ===

@app.post("/watchlist/add")
def api_add_watchlist(ticker: str):
    """
    Adds a ticker to the user's watchlist.
    """
    add_to_watchlist(ticker)
    return {"watchlist": get_watchlist()}


@app.get("/watchlist")
def api_get_watchlist():
    """
    Returns the current watchlist.
    """
    return {"watchlist": get_watchlist()}


@app.delete("/watchlist/remove")
def api_remove_watchlist(ticker: str):
    """
    Removes a ticker from the watchlist.
    """
    remove_from_watchlist(ticker)
    return {"watchlist": get_watchlist()}


# === HELPER FUNCTION ===

def get_profile(symbol: str):
    """
    Fetches company profile data (including logo) from Finnhub.
    Results are cached to avoid redundant API requests.
    """
    if symbol in profile_cache:
        return profile_cache[symbol]

    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_API_KEY}"
    profile = requests.get(url).json()
    profile_cache[symbol] = profile
    return profile


# === SEARCH ENDPOINT ===

@app.get("/search")
def search(query: str):
    """
    Searches for tickers that match the given query.
    Returns up to 5 results, each with symbol, name, and logo.
    """
    query = query.lower().strip()

    # Return from cache if available
    if query in search_cache:
        return search_cache[query]

    # Query Finnhub search API
    url = f"https://finnhub.io/api/v1/search?q={query}&token={FINNHUB_API_KEY}"
    resp = requests.get(url)
    results = resp.json().get("result", [])[:5]

    # Fetch company profiles in parallel
    futures = [executor.submit(get_profile, r.get("symbol")) for r in results]
    profiles = [f.result() for f in futures]

    # Combine ticker data with company profile info
    output = []
    for r, profile in zip(results, profiles):
        symbol = r.get("symbol")
        description = r.get("description", "")
        name = profile.get("name") or description or symbol
        logo_url = profile.get("logo") or "https://cdn-icons-png.flaticon.com/512/4946/4946378.png"

        output.append({
            "symbol": symbol,
            "name": name,
            "logo_url": logo_url
        })

    # Cache the result
    search_cache[query] = output
    return output


# === ANALYSIS ENDPOINT ===

@app.get("/analyze")
def analyze(ticker: str):
    """
    Performs a basic technical analysis for a given ticker.
    Includes moving averages, RSI, trading signals, and extreme event detection.
    """
    ticker = ticker.upper()
    data = fetch_stock_data(ticker, period="6mo")
    df = add_sma(data.copy(), 20)
    df = add_rsi(df, 14)

    signals = generate_signals(df)
    extreme_alerts = detect_extreme_events(df)

    return {"ticker": ticker, "signals": signals, "extreme_alerts": extreme_alerts}


# === INFER WATCHLIST (AI + TECHNICAL COMBINED) ===

@app.get("/infer")
def infer_watchlist():
    tickers = get_watchlist()
    results = []

    for ticker in tickers:
        # Fetch recent data (you can use "5d" if you only want today's events)
        data = fetch_stock_data(ticker, period="5d")
        df = add_sma(data.copy(), 20)
        df = add_rsi(df, 14)
        extreme_alerts = detect_extreme_events(df)

        # Skip tickers with no extreme events
        if not extreme_alerts:
            continue

        # Optional AI analysis
        ai_suggestion = None
        try:
            ai_suggestion = ai_infer_ticker(ticker)
        except Exception as e:
            ai_suggestion = f"AI error: {e}"

        results.append({
            "ticker": ticker,
            "extreme_alerts": extreme_alerts,
            "ai_suggestion": ai_suggestion
        })

    return {"results": results}
