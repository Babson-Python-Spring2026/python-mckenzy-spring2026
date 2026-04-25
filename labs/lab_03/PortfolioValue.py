from pathlib import Path
import json
from datetime import datetime
from GetCash import get_share_position

PRICES_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\prices_dates.json")
DIVIDENDS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-06 M\data\system\dividends_dates.json")
TRANSACTIONS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\transactions\transactions.json")
def load_transactions():
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")

def load_dividends(file_path=DIVIDENDS_FILE):
    if not file_path.exists():
        return {}
    with open(file_path, "r") as f:
        return json.load(f)
    
def get_dividend_income(as_of_date, transactions):
    """
    Calculate total dividend income received up to as_of_date.
    For each dividend date, check how many shares were held at that moment.
    """
    dividends = load_dividends()
    dividend_log = []
    total = 0.0

    for div_date, payouts in dividends.items():
        if div_date > as_of_date:
            continue  # dividend hasn't happened yet

        for payout in payouts:
            ticker = payout["ticker"]
            div_per_share = float(payout["dividend"])

            # Only count buy/sell transactions for this ticker
            ticker_txns = [t for t in transactions if t.get("ticker") == ticker]
            shares_held = get_share_position(ticker, div_date, ticker_txns)

            if shares_held > 0:
                income = shares_held * div_per_share
                total += income
                dividend_log.append({
                    "date": div_date,
                    "ticker": ticker,
                    "shares": shares_held,
                    "dividend_per_share": div_per_share,
                    "income": income
                })

    return total, sorted(dividend_log, key=lambda x: x["date"])


def load_prices():
    if not PRICES_FILE.exists():
        return {}
    with open(PRICES_FILE, "r") as f:
        return json.load(f)
    
def get_price_on_date(ticker, as_of_date, prices):

    if ticker == "$$$$":
        return 1.0  # cash always equals face value

    as_of = parse_date(as_of_date)

    valid_dates = sorted(
        [d for d in prices.keys() if parse_date(d) <= as_of],
        reverse=True
    )

    for date in valid_dates:
        day_data = prices.get(date, [])
        for entry in day_data:
            if entry.get("ticker") == ticker:
                return float(entry["raw_price"])

    return 0.0

   
def get_positions(as_of_date, transactions):
    positions = {}

    for txn in transactions:
        if parse_date(txn["date"]) > parse_date(as_of_date):
            continue

        ticker = txn["ticker"]
        shares = txn["shares"]
        t = txn["type"]

        if t == "buy":
            positions[ticker] = positions.get(ticker, 0) + shares

        elif t == "sell":
            positions[ticker] = positions.get(ticker, 0) - shares

    return positions

def get_portfolio_value(as_of_date):
    
    transactions = load_transactions()
    prices = load_prices()

    positions = get_positions(as_of_date, transactions)
    cash = 0

    breakdown = {}
    total_value = cash  # start with cash

    for ticker, amount in positions.items():
        price = get_price_on_date(ticker, as_of_date, prices)
        value = amount * price
        breakdown[ticker] = value
        total_value += value

    return total_value, breakdown, positions, cash

def is_valid_portfolio_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid format. Use YYYY-MM-DD."

    prices = load_prices()
    transactions = load_transactions()

    price_dates = set(prices.keys())
    txn_dates = set(t["date"] for t in transactions)

    valid_dates = price_dates.union(txn_dates)

    if date_str not in valid_dates:
        return False, "Date not found in data files."

    return True, ""

def show_portfolio_value():

    while True:
        as_of_date = input("Enter date (YYYY-MM-DD): ").strip()

        valid, message = is_valid_portfolio_date(as_of_date)

        if valid:
            break
        else:
           print(f"Try again. {message}\n")

    total, breakdown, positions, cash = get_portfolio_value(as_of_date)

    print(f"\nPortfolio as of {as_of_date}:\n")

    for ticker in breakdown:
        print(f"{ticker}:")
        print(f"  Shares: {positions[ticker]:,.2f}")
        print(f"  Value:  ${breakdown[ticker]:,.2f}")

    print(f"\nTotal Portfolio Value: ${total:,.2f}")

if __name__ == "__main__":
    show_portfolio_value()