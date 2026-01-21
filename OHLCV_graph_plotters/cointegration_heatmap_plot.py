import csv
import statistics
from dataclasses import dataclass
import plotly.graph_objs as go

tickers = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "BTC", "ETH"
]

@dataclass
class Series:
    date: list
    open: list
    high: list
    low: list
    close: list
    volume: list

    def at(self, i: int):
        return {
            "date": self.date[i],
            "open": self.open[i],
            "high": self.high[i],
            "low": self.low[i],
            "close": self.close[i],
            "adj_close": self.adj_close[i],
            "volume": self.volume[i],
        }

    def last(self):
        return self.at(-1)

def load_ticker_csvs(tickers, folder="../OHLCV_data/"):
    out = {}

    for t in tickers:
        path = f"{folder}/{t}.csv"
        dt, opn, high, low, close, vol = [], [], [], [], [], []

        with open(path, "r", newline="") as f:
            r = csv.reader(f)

            next(r)  # skip row 1
            next(r)  # skip row 2

            for row in r:
                if not row or len(row) < 6:
                    continue

                if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "" or row[4] == "" or row[5] == "":
                    continue

                dt.append(row[0])
                close.append(float(row[1]))
                high.append(float(row[2]))
                low.append(float(row[3]))
                opn.append(float(row[4]))
                vol.append(float(row[5]))

        out[t] = Series(dt, opn, high, low, close, vol)

    return out

def show_heatmap(grid, tickers, title="Correlation Heatmap"):
    n = len(tickers)
    z = [row[:] for row in grid]
    text = [[f"{v:.2f}" for v in row] for row in grid]
    for i in range(n):
        z[i][i] = None
        text[i][i] = ""
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=tickers,
            y=tickers,
            text=text,
            texttemplate="%{text}",
            hovertemplate="X: %{x}<br>Y: %{y}<br>Value: %{z:.4f}<extra></extra>",
        )
    )
    fig.update_layout(title=title, template="plotly_dark")
    fig.show(renderer="browser")

def main():
    tickerData = load_ticker_csvs(tickers)
    tickerGrid = [[0.0 for _ in tickers] for _ in tickers]
    for a, ticker1 in enumerate(tickers):
        for b, ticker2 in enumerate(tickers):

            # get and format data
            series1 = tickerData[ticker1]
            series2 = tickerData[ticker2]
            dates = {}
            pairs = []
            for i in range(len(series1.date)):
                dates[series1.date[i]] = series1.close[i]
            for j in range(len(series2.date)):
                if series2.date[j] in dates:
                    pairs.append((series2.close[j], dates.get(series2.date[j])))
            #print(pairs)

            # calculate covariance
            justSeries1 = []
            justSeries2 = []
            for pair in pairs:
                justSeries1.append(pair[0])
                justSeries2.append(pair[1])
            returns1 = []
            returns2 = []
            for i in range(1, len(justSeries1)):
                returns1.append((justSeries1[i] - justSeries1[i - 1]) / justSeries1[i - 1])
                returns2.append((justSeries2[i] - justSeries2[i - 1]) / justSeries2[i - 1])
            series1mean = sum(returns1)/len(returns1)
            series2mean = sum(returns2)/len(returns2)
            #print(series1mean, series2mean)
            adjustedPairs = []
            for i in range(len(pairs)-1):
                adjustedPairs.append((returns1[i] - series1mean, returns2[i] - series2mean))
            products = []
            for i in range(len(adjustedPairs)):
                products.append(adjustedPairs[i][0] * adjustedPairs[i][1])
            total = sum(products)
            covariance = total/(len(pairs)-1)
            #print(covariance)
            correlationCoefficient = (
                    covariance/(statistics.stdev(returns1)*statistics.stdev(returns2))
            )
            #print(correlationCoefficient)
            tickerGrid[a][b] = correlationCoefficient
    show_heatmap(tickerGrid, tickers)

main()