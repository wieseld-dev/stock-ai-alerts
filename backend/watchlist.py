import sqlite3

# Define the SQLite database file name
DB_FILE = "stocks.db"


def init_watchlist():
    """
    Initializes the 'watchlist' table in the database if it does not exist.

    The table stores:
        - id: Auto-increment primary key
        - ticker: Unique stock symbol (e.g., "AAPL", "TSLA")
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_to_watchlist(ticker: str):
    """
    Adds a ticker symbol to the watchlist.

    Args:
        ticker (str): The stock symbol to add (case-insensitive).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO watchlist (ticker) VALUES (?)",
        (ticker.upper(),)
    )
    conn.commit()
    conn.close()


def remove_from_watchlist(ticker: str):
    """
    Removes a ticker symbol from the watchlist.

    Args:
        ticker (str): The stock symbol to remove (case-insensitive).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM watchlist WHERE ticker = ?",
        (ticker.upper(),)
    )
    conn.commit()
    conn.close()


def get_watchlist():
    """
    Retrieves all tickers currently stored in the watchlist.

    Returns:
        list[str]: A list of ticker symbols in uppercase.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT ticker FROM watchlist")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]
