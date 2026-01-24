import yfinance as yf

tickers = [
    "SPY",
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD",
    "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "LINK-USD"
]


for name in tickers:
    data = yf.download(name, period='1wk', interval='1m', auto_adjust=True)
    data.to_csv('../OHLCV_data/'+name+'.csv')
    print(tickers.index(name)+1, " of ", len(tickers), " items downloaded" )

print("all items complete")