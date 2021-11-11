import dash_bootstrap_components as dbc

from dash import dcc, html
from load_data import SportStatistics
from noc_to_region import noc_to_region

sport_statistics = SportStatistics()

sport_options_dropdown = [{"label" : sport, "value" : sport} for sport in sport_statistics.sports()]



usa_layout = html.Div([
    html.H1("USA content")
])
sports_layout = dbc.Container([
    dcc.Store(id="sports-data"),
    dbc.Card([
        dbc.CardBody(html.H1("Sports statistics"), className="mt-3")
    ]),
    dbc.Row([html.H4("Sport", className="card-title"),
        dbc.Col(dcc.Dropdown(id="sports-dropdown",
                            options=sport_options_dropdown,
                            value="Alpine Skiing"),
                            className="mb-3"),        
        dbc.Col(dcc.Dropdown(id='sport-statistics', 
                            className='',
                            value="age"))
    ], className="mt-4"),
    dbc.Card([
            dcc.Graph(id="sports-graph")
    ])
])