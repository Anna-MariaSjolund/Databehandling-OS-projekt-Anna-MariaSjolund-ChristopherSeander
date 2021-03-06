# https://dash.plotly.com/urls how to structure a multi-page app
# https://dash.plotly.com/dash-core-components/tabs how to add tabs to the app
# https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component show and hide components
from dash.dependencies import Output, Input
from dash import dcc, html
import dash_bootstrap_components as dbc

from app import app, server
from layouts import usa_layout, sports_layout
import callbacks

# main layout
app.layout = dbc.Container([
    html.H1(id="title", className="pt-3"),      # dashboard title
    dbc.Card([
        dbc.CardBody(
        dcc.Tabs(id="tabs", value="tab-usa",    # tabs bar
                children=[
                        dcc.Tab(label="USA", 
                                value="tab-usa",
                                className="custom-tab",
                                style={"background-color": "#424242"}),
                        dcc.Tab(label="Sports statistics", 
                                value="tab-sports",
                                className="custom-tab",
                                style={"background-color": "#424242"})
                        ])
        )
    ], className="mt-3"),
    html.Div(id="content"),     # content container
])

# changed what is shown in "content"
@app.callback(
    Output("content", "children"),
    Output("title", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-usa":
        return usa_layout, "Olympic History in USA (1896-2016)"
    else:
        return  sports_layout, "Sports Statistics in the Olympic Games"

if __name__ == "__main__":
    app.run_server()