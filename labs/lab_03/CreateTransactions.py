import json
from datetime import datetime
from pathlib import Path


TRANSACTIONS_FILE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\transactions\transactions.json")
TICKER_UNIVERSE = Path(r"C:\PythonClass\student_repo\classes\04-08 W\data\system\ticker_universe.json")
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


def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")


def is_valid_date(date):
    try:
        parse_date(date)
        return True
    except ValueError:
        return False
    
def is_valid_ticker(ticker, universe):
    return ticker.upper().strip() in universe

def save_transactions(trns):
    trns_sorted = sorted(trns, key=lambda x: x["date"])
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(trns_sorted, f, indent=2)


def create_transaction(trn_type, date, ticker_universe):

    trn_type = trn_type.lower().strip()

    trn = {
        "date": date
    }

    # 🔥 HANDLE CASH (convert to $$$$ system)
    if trn_type in ["contribution", "withdrawal"]:
        amt = float(input("Enter cash amount: "))

        trn["ticker"] = "$$$$"
        trn["shares"] = amt
        trn["price"] = 1.0

        # convert to buy/sell
        if trn_type == "contribution":
            trn["type"] = "buy"
        else:
            trn["type"] = "sell"

    # 🔥 HANDLE NORMAL TRADES
    elif trn_type in ["buy", "sell"]:

        while True:
            ticker = input("Enter ticker: ").upper().strip()

            # allow $$$$ OR valid ticker
            if ticker == "$$$$" or is_valid_ticker(ticker, ticker_universe):
                break
            else:
                print("Invalid ticker. Not in universe. Try again.")

        shares = float(input("Enter shares: "))
        price = float(input("Enter price: "))

        trn["type"] = trn_type
        trn["ticker"] = ticker
        trn["shares"] = shares
        trn["price"] = price

    else:
        print("Invalid transaction type")
        return None

    return trn

def transaction_session():

    trns = load_transactions()
    ticker_universe = load_ticker_universe()

    # DATE VALIDATION LOOP
    while True:
        date = input("Enter working date (YYYY-MM-DD): ").strip()

        if is_valid_date(date):
            break
        else:
            print("Invalid date format. Try again.\n")

    while True:
        trn_type = input(
            "Enter transaction type (contribution, withdrawal, buy, sell) or q to quit: "
        ).lower().strip()

        if trn_type == "q":
            break

        trn = create_transaction(trn_type, date, ticker_universe)

        if trn is None:
            print("Transaction not created.\n")
            continue

        trns.append(trn)

        # SORT BEFORE SAVE (IMPORTANT)
        trns = sorted(trns, key=lambda x: x["date"])

        save_transactions(trns)

        print("Transaction saved.\n")


if __name__ == "__main__":
    transaction_session()
