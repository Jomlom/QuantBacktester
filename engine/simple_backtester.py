import pandas as pd

class SimpleBacktester:

    def run(self, df, signals):
        df = df.copy()
        df["position"] = signals["position"]

        # daily returns
        df["returns"] = df["Close"].pct_change()

        # strategy returns
        df["strategy_returns"] = df["returns"] * df["position"].shift(1)

        # cumulative performance
        df["equity_curve"] = (1 + df["strategy_returns"]).cumprod()

        return df
