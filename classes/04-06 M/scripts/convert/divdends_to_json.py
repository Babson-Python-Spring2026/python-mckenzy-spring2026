import json

# Dictionary keyed by date:
# date -> list of dividend records for that date
divs_date = {}
divs_ticker = {}

# Open CSV file
with open('classes/04-06 M/data/source/portfolio_dividends_20260331b.csv', 'r') as f:
    
    next(f)  # skip header

    for line in f:
        date, ticker, dividend = line.strip().split(',')
        divs_date.setdefault(date,[]).append({
            'ticker': ticker,
            'dividend': dividend
        })

        divs_ticker.setdefault(ticker,[]).append({
            'date': date,
            'dividend': dividend
        })

with open('classes/04-06 M/data/system/dividends_by_dates.json', 'w') as f:
    json.dump(divs_date, f,indent=2)

with open('classes/04-06 M/data/system/dividends_by_ticker.json', 'w') as f:
    json.dump(divs_ticker, f,indent=2)
    