import json
from pathlib import Path
'''
TRANSACTIONS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "system"
    / "transactions"
    / "transactions.json"
)
'''
TRANSACTIONS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\transactions\transactions.json")
def load_transactions():
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return []


def get_transactions_by_ticker(ticker): 
    """
    Return all transactions for a given ticker, sorted by date.
    """
    transactions = load_transactions()

    # Normalize ticker input
    ticker = ticker.upper()

    # Filter transactions that have this ticker
    filtered = [
        txn for txn in transactions
        if txn.get("ticker") == ticker
    ]

    # Sort by date (assuming YYYY-MM-DD format)
    filtered.sort(key=lambda x: x["date"])

    return filtered


def show_ticker_history():
    ticker = input("Enter ticker: ").strip()
    results = get_transactions_by_ticker(ticker)

    if not results:
        print("No transactions found for that ticker.")
    else:
        for txn in results:
            print(txn)


if __name__ == "__main__":
    show_ticker_history()
    