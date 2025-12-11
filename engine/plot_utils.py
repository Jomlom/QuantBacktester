import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_multi_strategy(equity_curves, price_dfs, signals_dict, title="Strategy"):

    tickers = list(equity_curves.keys())
    n_tickers = len(tickers)

    # combine equity curves into one total curve
    equity_df = pd.DataFrame(equity_curves)
    total_equity = equity_df.mean(axis=1)
    total_ticks = range(len(total_equity))

    fig = make_subplots(
        rows=1 + n_tickers,
        cols=1,
        row_heights= ([1 / (n_tickers + 1)] * (n_tickers + 1))
    )

    fig.add_trace(
        go.Scatter(
            x=list(total_ticks),
            y=total_equity,
            mode="lines",
            name="Total Equity Curve",
            line=dict(color="lime", width=3),
        ),
        row=1, col=1
    )

    current_row = 2

    for ticker in tickers:

        df = price_dfs[ticker].copy()

        if not isinstance(df.index, pd.DatetimeIndex):
            continue

        signals = signals_dict[ticker]

        df["tick"] = range(len(df))
        hover = df.index.strftime("%Y-%m-%d %H:%M:%S")

        # price line
        fig.add_trace(
            go.Scatter(
                x=df["tick"],
                y=df["Close"],
                mode="lines",
                name=f"{ticker} Price",
                line=dict(color="blue", width=2),
                text=hover,
                hovertemplate="Time: %{text}<br>Price: %{y}<extra></extra>"
            ),
            row=current_row, col=1
        )

        # entry/exit detection
        pos_change = signals["position"].ne(signals["position"].shift())
        entries = signals["position"].gt(signals["position"].shift()) & pos_change
        exits = signals["position"].lt(signals["position"].shift()) & pos_change

        # entries
        fig.add_trace(
            go.Scatter(
                x=df["tick"][entries],
                y=df["Close"][entries],
                mode="markers",
                marker=dict(symbol="triangle-up", color="green", size=12),
                name=f"{ticker} Entry"
            ),
            row=current_row, col=1
        )

        # exits
        fig.add_trace(
            go.Scatter(
                x=df["tick"][exits],
                y=df["Close"][exits],
                mode="markers",
                marker=dict(symbol="triangle-down", color="red", size=12),
                name=f"{ticker} Exit"
            ),
            row=current_row, col=1
        )
        fig.update_yaxes(title=f"{ticker} Price", row=current_row, col=1)
        current_row += 1

    # layout
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=400 + 300 * n_tickers,
        showlegend=False
    )

    fig.show(renderer="browser")
