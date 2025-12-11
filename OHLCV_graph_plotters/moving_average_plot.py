import plotly.graph_objs as go
import pandas as pd

tickerName = "AAPL"
fileName = "../OHLCV_data/" + tickerName + ".csv"

windows = [5, 20, 50, 100]

# load data
columns = ["Datetime", "Close", "High", "Low", "Open", "Volume"]
df = pd.read_csv(
    fileName,
    skiprows=2,
    names=columns,
    parse_dates=["Datetime"],
)

df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
df = df.dropna(subset=["Datetime"])
df = df.set_index("Datetime")

# compressed x-axis
df["tick"] = range(len(df))
hover_text = df.index.strftime("%Y-%m-%d %H:%M:%S")

fig = go.Figure()

# add actual price
df[f"Close Price"] = df["Close"]
fig.add_trace(
    go.Scatter(
        x=df["tick"],
        y=df[f"Close Price"],
        name=f"Close Price",
        mode="lines",
        text=hover_text,
        hovertemplate="Time: %{text}<br>SMA: %{y}<extra></extra>"
    )
)

# add averages
for window in windows:
    df[f"SMA_{window}"] = df["Close"].rolling(window).mean()
    fig.add_trace(
        go.Scatter(
            x=df["tick"],
            y=df[f"SMA_{window}"],
            name=f"SMA {window}",
            mode="lines",
            text=hover_text,
            hovertemplate="Time: %{text}<br>SMA: %{y}<extra></extra>"
        )
    )

tick_every = max(len(df)//10, 1)
fig.update_xaxes(
    tickvals=df["tick"][::tick_every],
    ticktext=df.index.strftime("%H:%M")[::tick_every]
)

fig.update_layout(
    title=tickerName,
    xaxis_title="Trading Tick",
    yaxis_title="Price (USD)",
    template="plotly_dark",
)

fig.show(renderer="browser")
