import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
import plotly.express as px

class CointegrationHeatmap:

    def __init__(
        self,
        lookback=200,
        zscore_window=30,
        significance_level=0.05
    ):
        self.lookback = lookback
        self.zscore_window = zscore_window
        self.significance_level = significance_level

    def download_prices(self, tickers):
        print(f"Downloading {len(tickers)} tickers...")

        data = yf.download(
            tickers,
            period="1y",
            interval="1d",
            auto_adjust=True,
            progress=False
        )["Close"]

        data = data.dropna()
        print(f"Downloaded price matrix shape: {data.shape}")
        return data

    def engle_granger(self, series_x, series_y):

        x = series_x
        y = series_y

        x_const = sm.add_constant(x)
        model = sm.OLS(y, x_const).fit()
        beta = model.params[1]

        resid = y - beta * x
        adf_pvalue = sm.tsa.adfuller(resid)[1]

        return adf_pvalue, beta, resid

    def compute_zscore(self, series):
        mean = series.rolling(self.zscore_window).mean()
        std = series.rolling(self.zscore_window).std()
        return (series - mean) / std

    def generate(self, tickers):
        prices = self.download_prices(tickers)

        n = len(tickers)
        z_matrix = np.zeros((n, n))
        p_matrix = np.zeros((n, n))

        print("Running cointegration tests...")
        for i in range(n):
            for j in range(n):
                if i == j:
                    z_matrix[i, j] = 0
                    p_matrix[i, j] = 1
                else:
                    x = prices[tickers[i]]
                    y = prices[tickers[j]]

                    pvalue, beta, resid = self.engle_granger(x, y)
                    zscore_series = self.compute_zscore(resid)

                    z_matrix[i, j] = zscore_series.iloc[-1]
                    p_matrix[i, j] = pvalue

        # Convert to DataFrames
        z_df = pd.DataFrame(z_matrix, index=tickers, columns=tickers)
        p_df = pd.DataFrame(p_matrix, index=tickers, columns=tickers)

        # Plot heatmap
        fig = px.imshow(
            z_df,
            color_continuous_scale="RdBu",
            title="Cointegration Z-Score Heatmap",
            labels=dict(x="Ticker", y="Ticker", color="Z-Score"),
            aspect="auto",
        )

        fig.update_layout(width=1000, height=900)
        fig.show(renderer="browser")

        return z_df, p_df

if __name__ == "__main__":

    tickers = [
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA",
        "TSLA", "AMD", "INTC", "AVGO", "ADBE", "CSCO",
    ]

    coint = CointegrationHeatmap(
        lookback=200,
        zscore_window=30,
        significance_level=0.05
    )

    zscores, pvalues = coint.generate(tickers)

    print("\nFinal Z-Scores Matrix")
    print(zscores)

    print("\nCointegration P-Values")
    print(pvalues)
