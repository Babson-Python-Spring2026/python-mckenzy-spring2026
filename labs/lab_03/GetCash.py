import json
from pathlib import Path
from datetime import datetime

TRANSACTIONS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\transactions\transactions.json")
DIVIDENDS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-06 M\data\system\dividends_dates.json")

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")

def is_valid_cash_date(as_of_date):
    try:
        parse_date(as_of_date)
    except ValueError:
        return False, "Invalid date format."

    transactions = load_transactions()
    dividends = load_dividends()

    all_dates = set()

    all_dates.update(t["date"] for t in transactions)
    all_dates.update(dividends.keys())

    if as_of_date not in all_dates:
        return False, "Date not found in transaction/dividend data."

    return True, "OK"

def load_transactions():
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def load_dividends(file_path=DIVIDENDS_FILE):
    if not file_path.exists():
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def get_share_position(ticker, as_of_date, transactions):
    """
    Calculate net shares held for a ticker up to (and including) a given date.
    """
    shares = 0.0
    for txn in transactions:
        if txn["ticker"] == ticker and txn["date"] <= as_of_date:
            if txn["type"] == "buy":
                shares += txn["shares"]
            elif txn["type"] == "sell":
                shares -= txn["shares"]
    return shares


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


def get_cash_balance(as_of_date):
    transactions = load_transactions()

    relevant = sorted(
        [t for t in transactions if t["date"] <= as_of_date],
        key=lambda t: t["date"]
    )

    cash = 0.0

    for txn in relevant:
        ticker = txn["ticker"]
        shares = txn["shares"]
        price = txn["price"]
        t = txn["type"]

        if ticker == "$$$$":
            if t == "buy":
                cash += shares * price
            elif t == "sell":
                cash -= shares * price

        else:
            if t == "buy":
                cash -= shares * price
            elif t == "sell":
                cash += shares * price

    dividend_income, dividend_log = get_dividend_income(as_of_date, transactions)
    cash += dividend_income

    return cash, relevant, dividend_income, dividend_log

def show_cash_balance():

    while True:
        as_of_date = input("Enter date to check balance (YYYY-MM-DD): ").strip()

        valid, message = is_valid_cash_date(as_of_date)

        if valid:
            break
        else:
            print(f"Try again. {message}\n")

    cash, relevant, dividend_income, dividend_log = get_cash_balance(as_of_date)

    print(f"\nTransactions up to {as_of_date}:")
    if not relevant:
        print("  No transactions found.")
    else:
        for txn in relevant:
            print(f"  {txn}")

    if dividend_log:
        print(f"\nDividends received up to {as_of_date}:")
        for d in dividend_log:
            print(f"  {d['date']} | {d['ticker']} | {d['shares']} shares x ${d['dividend_per_share']} = ${d['income']:.2f}")

    print(f"\nTotal transactions: {len(relevant)}")
    print(f"Dividend income:    ${dividend_income:,.2f}")
    print(f"Cash balance as of {as_of_date}: ${cash:,.2f}")

if __name__ == "__main__":
    show_cash_balance()
