import pandas as pd

from engine.plot_utils import plot_multi_strategy
from engine.simple_backtester import SimpleBacktester
from strategies.momentum_reversion import MomentumReversalStrategy

# tickers to test
tickers = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA",
    "TSLA", "AMD", "INTC", "AVGO", "ADBE", "CSCO",
]

def load_data(path):
    df = pd.read_csv(
        path,
        skiprows=3,
        names=["Datetime", "Close", "High", "Low", "Open", "Volume"],
        parse_dates=["Datetime"]
    )
    df = df.set_index("Datetime")
    return df

def main():
    result_msgs = []

    strat = MomentumReversalStrategy()
    bt = SimpleBacktester()

    all_equity_curves = {}
    all_price_dfs = {}
    all_signals = {}

    for ticker in tickers:
        print(f"Running {ticker}...")

        df = load_data(f"OHLCV_data/{ticker}.csv")
        signals = strat.generate_signals(df)

        results = bt.run(df, signals)

        all_equity_curves[ticker] = results["equity_curve"]
        all_price_dfs[ticker] = df
        all_signals[ticker] = signals

        if results is None or len(results) == 0 or "equity_curve" not in results or results[
            "equity_curve"].isna().all():
            continue

        result_msgs += (f"{ticker} Final return: ", (results["equity_curve"].iloc[-1]))

    for result in result_msgs:
        print(result)

    # plot all results together
    plot_multi_strategy(
        all_equity_curves,
        all_price_dfs,
        all_signals,
        title="Momentum Reversal Strategy"
    )

if __name__ == "__main__":
    main()
