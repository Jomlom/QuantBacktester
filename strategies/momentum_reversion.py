import pandas as pd

class MomentumReversalStrategy:

    def __init__(self, short_window=2, mid_window=10, long_window=200, roc_period=3):
        self.short_window = short_window
        self.mid_window = mid_window
        self.long_window = long_window
        self.roc_period = roc_period

    def generate_signals(self, df):
        df = df.copy()

        # indicators
        df["sma_short"] = df["Close"].rolling(self.short_window).mean()
        df["sma_mid"] = df["Close"].rolling(self.mid_window).mean()
        df["sma_long"]  = df["Close"].rolling(self.long_window).mean()
        df["roc"] = df["Close"].pct_change(self.roc_period)

        # default position = 0
        df["position"] = 0

        long_condition = (
                (df["Close"] < df["sma_short"]) &
                (df["sma_short"] < df["sma_long"]) &
                (df["roc"] > 0)
        )

        short_condition = (
                (df["Close"] > df["sma_short"]) &
                (df["sma_short"] > df["sma_long"]) &
                (df["roc"] < 0)
        )

        df.loc[long_condition, "position"] = 1
        df.loc[short_condition, "position"] = -1

        # forward fill signals so we hold until exit
        df["position"] = df["position"].replace(0, pd.NA).ffill().fillna(0)

        return df[["position"]]
