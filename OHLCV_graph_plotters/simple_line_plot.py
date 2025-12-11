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

# compressed axis
df["tick"] = range(len(df))
hover_text = df.index.strftime("%Y-%m-%d %H:%M:%S")

main_values = ["Open", "High", "Low", "Close"]

fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

# OHLC lines
for value in main_values:
    fig.add_trace(
        go.Scatter(
            x=df["tick"],
            y=df[value],
            name=value,
            mode="lines",
            text=hover_text,
            hovertemplate="Time: %{text}<br>%{y}<extra></extra>"
        ),
        row=1, col=1
    )

# Volume bars
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

tick_every = max(len(df)//10, 1)
for r in [1,2]:
    fig.update_xaxes(
        tickvals=df["tick"][::tick_every],
        ticktext=df.index.strftime("%H:%M")[::tick_every],
        row=r, col=1
    )

fig.update_layout(
    bargap=0,
    bargroupgap=0,
    title=tickerName,
    template="plotly_dark",
)

fig.show(renderer="browser")
