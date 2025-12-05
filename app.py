from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px


DATA_PATH = "data/combined_sales_data.csv"

app = Dash()

# Prepare data
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

df.sort_values(by="date", inplace=True)

REGIONS = list(map(lambda x: x.capitalize(),
               df["region"].unique().tolist() + ['all']))


@callback(
    Output("pink-morsel-graph", "figure"),
    Input("radio", "value")
)
def update_figure_by_region(selected_region):
    filtered_df = df.copy()

    if selected_region != REGIONS[-1]:
        filtered_df = df[df["region"] == selected_region.lower()]

    # Prepare figure
    fig = px.line(filtered_df, template="seaborn", x="date", y="sales", color="region", labels={
        "date": "Date", "sales": "Sales ($)", "region": "Region"}, markers=True)

    fig.update_layout(transition_duration=500)

    return fig


app.layout = html.Div(children=[
    html.H1(children="Soul Foods's Pink Morsel Sales Analysis"),
    html.Div(children="""
        Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?
        """),

    dcc.Graph(id="pink-morsel-graph"),

    html.Label('Region:'),
    dcc.RadioItems(REGIONS, value=REGIONS[-1], id="radio", labelStyle={'display': 'inline-block', 'margin-right': '20px', 'fontSize': '16px'},
                   inputStyle={'margin-right': '8px',
                               'width': '16px', 'height': '16px'},
                   style={'padding': '8px'})
], style={"width": "80%", "margin": "0 auto", "font-family": "Helventica Neue, sans-serif"})

if __name__ == "__main__":
    app.run(debug=True)
