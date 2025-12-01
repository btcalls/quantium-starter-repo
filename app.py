from dash import Dash, html, dcc

import pandas as pd
import plotly.express as px


DATA_PATH = "data/combined_sales_data.csv"

# Show data at least 30 days before and after the date in question to better visualise
# if there was a change in sales after the price increase
BASIS_DATE = pd.Timestamp("2021-01-15")
START_DATE = BASIS_DATE - pd.Timedelta(days=30)
END_DATE = BASIS_DATE + pd.Timedelta(days=30)

app = Dash()

# Prepare data
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

df.sort_values(by="date", inplace=True)

grouped_df = df.groupby("date")["sales"].sum().reset_index()
filtered_df = grouped_df[(grouped_df["date"] >=
                          START_DATE) & (grouped_df["date"] <= END_DATE)]

# Prepare figure
fig = px.line(filtered_df, template="seaborn", x="date", y="sales", labels={
              "date": "Date", "sales": "Sales ($)"}, markers=True)

fig.add_annotation(
    x=BASIS_DATE,
    y=filtered_df[filtered_df["date"] == BASIS_DATE]["sales"].values[0],
    text=BASIS_DATE.strftime("%b %d %Y"),
    showarrow=False,
    xanchor="right",
    yanchor="bottom"
)

app.layout = html.Div(children=[
    html.H1(children="Soul Foods's Pink Morsel Sales Analysis"),
    html.Div(children="""
        Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?
        """),
    dcc.Graph(
        id="pink-morsel-graph",
        figure=fig
    )
], style={"width": "80%", "margin": "0 auto", "font-family": "Helventica Neue, sans-serif"})

if __name__ == "__main__":
    app.run(debug=True)
