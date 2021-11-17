# https://dash.plotly.com/urls how to structure a multi-page app
# https://dash.plotly.com/dash-core-components/tabs how to add tabs to the app
# https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
from dash.dependencies import Output, Input
from dash import dcc, html
import dash_bootstrap_components as dbc

from app import app
#from layouts import usa_layout, sports_layout
import callbacks

import sys
import logging

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# main layout
app.layout = dbc.Container([
    html.H1("asdasd"),      # dashboard title

])


if __name__ == "__main__":
    app.run_server()