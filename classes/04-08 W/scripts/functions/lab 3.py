import json
from pathlib import Path

TRANSACTIONS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "system"
    / "transactions"
    / "transactions.json"
)


def load_transactions():
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return []


def save_transactions(trns):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(trns, f, indent=2)


def create_transaction(trn_type, date):
    trn = {
        "date": date,
        "trnType": trn_type
    }

    if trn_type == "contribution" or trn_type == "withdrawal":
        amt = float(input("Enter cash amount: "))
        trn["cashAmount"] = amt

    elif trn_type == "buy" or trn_type == "sell":
        ticker = input("Enter ticker: ")
        shares = int(input("Enter shares: "))
        price = float(input("Enter price: "))

        trn["ticker"] = ticker
        trn["shares"] = shares
        trn["price"] = price

    return trn


def transaction_session():
    trns = load_transactions()

    date = input("Enter working date (YYYYMMDD): ")

    while True:
        trn_type = input(
            "Enter transaction type (contribution, withdrawal, buy, sell) or q to quit: "
        )

        if trn_type == "q":
            break

        trn = create_transaction(trn_type, date)
        trns.append(trn)

        save_transactions(trns)
        print("Transaction saved.\n")


if __name__ == "__main__":
    transaction_session()

