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


def save_transactions(trns):
    trns_sorted = sorted(trns, key=lambda x: x["date"])
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(trns_sorted, f, indent=2)


def create_transaction(trn_type, date):
    trn_type = trn_type.lower().strip()

    trn = {
        "date": date,
        "type": trn_type
    }

    if trn_type in ["contribution", "withdrawal"]:
        amt = float(input("Enter cash amount: "))
        trn["amount"] = amt

    elif trn_type in ["buy", "sell"]:
        ticker = input("Enter ticker: ").upper().strip()
        shares = int(input("Enter shares: "))
        price = float(input("Enter price: "))

        trn["ticker"] = ticker
        trn["shares"] = shares
        trn["price"] = price

    else:
        print("Invalid transaction type")
        return None

    return trn

def transaction_session():
    trns = load_transactions()

    date = input("Enter working date (YYYY-MM-DD): ")

    while True:
        trn_type = input(
        "Enter transaction type (contribution, withdrawal, buy, sell) or q to quit: "
    ).lower().strip()

        if trn_type == "q":
            break

        trn = create_transaction(trn_type, date)

    # safety check (prevents corrupt entries)
        if trn is None:
            print("Invalid transaction. Try again.\n")
        continue

    trns.append(trn)

    # ALWAYS sort before saving (fixes your ordering issue)
    trns = sorted(trns, key=lambda x: x["date"])

    save_transactions(trns)

    print("Transaction saved.\n")


if __name__ == "__main__":
    transaction_session()
