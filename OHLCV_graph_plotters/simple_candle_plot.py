import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

tickerName = "AAPL"
fileName = "../OHLCV_data/" + tickerName + ".csv"

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

# Compressed axis
df["tick"] = range(len(df))
hover_text = df.index.strftime("%Y-%m-%d %H:%M:%S")

# Create subplot
fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

# Candlestick data
fig.add_trace(
    go.Candlestick(
        x=df["tick"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=tickerName,
        text=hover_text,
        hovertemplate="Time: %{text}<br>Open: %{open}<br>Close: %{close}<extra></extra>"
    ),
    row=1, col=1
)

# volume data
fig.add_trace(
    go.Bar(
        x=df["tick"],
        y=df["Volume"],
        name="Volume",
        text=hover_text,
        hovertemplate="Time: %{text}<br>Volume: %{y}<extra></extra>",
    ),
    row=2, col=1
)

# layout & tick labels
tick_every = max(len(df)//10, 1)
fig.update_xaxes(
    tickvals=df["tick"][::tick_every],
    ticktext=df.index.strftime("%H:%M")[::tick_every],
    row=2, col=1
)
fig.update_xaxes(
    tickvals=df["tick"][::tick_every],
    ticktext=df.index.strftime("%H:%M")[::tick_every],
    row=1, col=1
)

fig.update_layout(
    bargap=0,
    bargroupgap=0,
    title=tickerName,
    xaxis_rangeslider_visible=False,
    template="plotly_dark",
)

fig.show(renderer="browser")
