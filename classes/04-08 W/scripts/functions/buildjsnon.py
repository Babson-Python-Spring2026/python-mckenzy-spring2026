import json

dates = [
"20250102","20250103","20250106","20250107","20250108",
"20250110","20250113","20250114","20250115","20250116",
"20250117","20250121","20250122","20250123","20250124",
"20250127","20250128","20250129","20250130","20250131"
]

tickers = [
"AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","V","PG",
"KO","PEP","DIS","HD","MCD","COST","WMT","BAC","XOM","CVX",
"PFE","T","VZ","INTC","CSCO"
]

prices = {
"AAPL":243.85,"MSFT":418.58,"GOOGL":189.43,"AMZN":220.22,"NVDA":138.31,
"META":599.24,"TSLA":379.28,"JPM":240.00,"V":314.40,"PG":165.98,
"KO":61.84,"PEP":150.21,"DIS":110.82,"HD":388.46,"MCD":292.51,
"COST":909.81,"WMT":90.00,"BAC":44.29,"XOM":107.31,"CVX":146.71,
"PFE":26.61,"T":22.83,"VZ":40.21,"INTC":20.22,"CSCO":59.10
}

transactions = []

for i, ticker in enumerate(tickers):
    sell_shares = i + 1
    price = prices[ticker]

    for j in range(0, 20, 2):
        buy_date = dates[j]
        sell_date = dates[j+1]

        transactions.append({
            "date": buy_date,
            "trnType": "buy",
            "ticker": ticker,
            "shares": 50,
            "price": price
        })

        transactions.append({
            "date": sell_date,
            "trnType": "sell",
            "ticker": ticker,
            "shares": sell_shares,
            "price": price
        })

with open("transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

print("Created transactions.json with", len(transactions), "transactions")