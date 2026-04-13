import json
from pathlib import Path

TICKER_UNIVERSE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\ticker_universe.json")
TRANSACTIONS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\transactions\transactions.json")
def load_transactions():
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return []
def load_ticker_universe():
    if TICKER_UNIVERSE.exists():
        with open(TICKER_UNIVERSE, "r") as f:
            data = json.load(f)
            return set(ticker.upper().strip() for ticker in data)
    return set()

def is_valid_ticker(ticker, universe):
    return ticker.upper().strip() in universe

def get_transactions_by_ticker(ticker, universe): 
    """
    Return all transactions for a valid ticker, sorted by date.
    """
    transactions = load_transactions()

    ticker = ticker.upper().strip()

    # VALIDATION STEP
    if ticker not in universe:
        return None

    filtered = [
        txn for txn in transactions
        if txn.get("ticker") == ticker
    ]

    filtered.sort(key=lambda x: x["date"])

    return filtered


def show_ticker_history():

    universe = load_ticker_universe()

    ticker = input("Enter ticker: ").upper().strip()

    results = get_transactions_by_ticker(ticker, universe)

    if results is None:
        print(" Invalid ticker. Not in ticker universe.")
        return

    if not results:
        print("No transactions found for that ticker.")
    else:
        for txn in results:
            if txn["type"] in ["buy", "sell"]:
                print(f"{txn['date']} | {txn['type']} | {txn['ticker']} | {txn['shares']} shares @ ${txn['price']}")
            else:
                print(f"{txn['date']} | {txn['type']} | ${txn['amount']}")


if __name__ == "__main__":
    show_ticker_history()
    