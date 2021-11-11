# https://dash.plotly.com/urls how to structure a multi-page app
# https://dash.plotly.com/dash-core-components/tabs how to add tabs to the app
# https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
from dash.dependencies import Output, Input
from dash import dcc, html

from app import app
from layouts import usa_layout, sports_layout
import callbacks

app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab-usa", # style={"width": "50%"}
    children=[
        dcc.Tab(label="USA", value="tab-usa"),
        dcc.Tab(label="Sports statistics", value="tab-sports")
    ]),
    html.Div(id="content")
])

@app.callback(
    Output("content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-usa":
        return usa_layout
    else:
        return  sports_layout

if __name__ == "__main__":
    app.run_server(debug=True)