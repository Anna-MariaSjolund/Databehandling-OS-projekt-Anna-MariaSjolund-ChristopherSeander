import dash
import dash_bootstrap_components as dbc

stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, suppress_callback_exceptions=True,  external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")]) #For mobile devices
server = app.server