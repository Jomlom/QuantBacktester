import yfinance as yf

tickers = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA",
    "TSLA", "AMD", "INTC", "AVGO", "ADBE", "CSCO",
]

for name in tickers:
    data = yf.download(name, period='1wk', interval='1m', auto_adjust=True)
    data.to_csv('../OHLCV_data/'+name+'.csv')
    print(tickers.index(name)+1, " of ", len(tickers), " items downloaded" )

print("all items complete")