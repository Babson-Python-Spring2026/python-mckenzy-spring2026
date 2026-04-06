import json

# Dictionary keyed by date:
# date -> list of dividend records for that date
prices_date = {}
prices_ticker = {}

# Open CSV file
with open('classes/04-06 M/data/source/portfolio_dividends_20260331b.csv', 'r') as f:
    
    next(f)  # skip header

    for line in f:
        date, ticker, price = line.strip().split(',')
        prices_date.setdefault(date,[]).append({
            'ticker': ticker,
            'price': price
        })

        prices_ticker.setdefault(ticker,[]).append({
            'date': date,
            'price': price
        })

with open('classes/04-06 M/data/system/prices_by_dates.json', 'w') as f:
    json.dump(prices_date, f,indent=2)

with open('classes/04-06 M/data/system/prices_by_ticker.json', 'w') as f:
    json.dump(prices_ticker, f,indent=2)
    