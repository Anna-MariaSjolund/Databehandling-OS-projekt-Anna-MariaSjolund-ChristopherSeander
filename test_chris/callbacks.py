import plotly_express as px
import pandas as pd

from dash.dependencies import Output, Input
from app import app
from noc_to_region import noc_to_region
from layouts import sport_statistics

@app.callback(
    Output("sports-data", "data"),
    Input("sports-dropdown", "value")
)
def filtered_sports(sport):
    sport_data = sport_statistics.medals(sport)
    return sport_data.to_json()

@app.callback(
    Output("test-text", "children"),
    Input("sports-dropdown", "value")
)
def print_name_of_sport(sport):
    return f"Countries with the most {sport} medals."

@app.callback(
    Output("sports-graph", "figure"),
    Input("sports-data", "data"),
    # drop down input for if statements in update
)
def update_sports_graph(df_json):
    data = pd.read_json(df_json)
    fig = px.bar(data, x="NOC", y="Medal", color="NOC")
    fig.update_xaxes(tickmode='array',
                    tickvals = data["NOC"],
                    ticktext=[noc_to_region(NOC) for NOC in data["NOC"]])
    return fig