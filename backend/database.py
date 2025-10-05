import sqlite3

# Define the database file name
DB_NAME = "stocks.db"

def get_connection():
    """
    Creates and returns a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    return sqlite3.connect(DB_NAME)


def save_to_db(df, table_name="prices"):
    """
    Saves a Pandas DataFrame to the SQLite database.

    Args:
        df (pandas.DataFrame): The DataFrame to store in the database.
        table_name (str): The name of the table where the data will be saved.
                          Default is 'prices'.

    Behavior:
        - Replaces the table if it already exists.
        - Includes the DataFrame index as a column in the database.
    """
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists="replace", index=True)
    conn.close()


def get_sample_rows(table_name="prices", limit=5):
    """
    Retrieves a sample of rows from a given table in the database.

    Args:
        table_name (str): The name of the table to query. Default is 'prices'.
        limit (int): The number of rows to fetch. Default is 5.

    Returns:
        list: A list of tuples representing the retrieved rows.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    rows = cursor.fetchall()
    conn.close()
    return rows
