'''
Function Purpose
create_transaction(...)	Create one of four transaction types: contribution, withdrawal, buy, or sell
get_cash_balance(as_of_date)	Reconstruct the cash balance on a chosen day
build_portfolio(as_of_date)	Reconstruct the portfolio on a chosen day from transaction history
list_transactions_for_ticker(ticker)	Show the dated transaction history for one ticker
'''
'''
import json

with open('price_ticker.json', 'r') as f:
    price_by_ticker = json.load(f)

with open('price_date.json', 'r') as f:
    price_by_date = json.load(f)
'''
def create_transaction(txn_type, date, amount=None, ticker=None, shares=None, price=None):
    
    # Base structure (common to all)
    transaction = {
        "type": txn_type,
        "date": date
    }

    if txn_type == "contribution":
        transaction["amount"] = amount

    elif txn_type == "withdrawal":
        transaction["amount"] = amount

    elif txn_type == "buy":
        transaction["ticker"] = ticker
        transaction["shares"] = shares
        transaction["price"] = price

    elif txn_type == "sell":
        transaction["ticker"] = ticker
        transaction["shares"] = shares
        transaction["price"] = price

    else:
        return None

    return transaction
    
print(create_transaction("contribution","2024-09-09",100,"APPL",2,50))