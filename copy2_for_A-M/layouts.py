import dash_bootstrap_components as dbc
import dash_daq as daq

from dash import dcc, html
from load_data import SportStatistics
from noc_to_region import noc_to_region

sport_statistics = SportStatistics() 

sport_options_dropdown = [{"label" : sport, "value" : sport} for sport in sport_statistics.sports()]




#A-Ms part USA

usa_options_dict = dict(medals = "Medals", participants = "Participants")
usa_options_dropdown = [{"label" : label, "value" : value} for value, label in usa_options_dict.items()]

usa_layout = html.Div([
        dbc.Row([
        html.H1("USA in the Olympic Games"),
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Dropdown(
                            id="usa-dropdown",
                            options=usa_options_dropdown,
                            value="medals"
                        )
                    )                       
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Dropdown(
                            id="graph-dropdown",
                            options = []
                        )
                    )
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        daq.ToggleSwitch(
                        id='my-toggle-switch',
                        value=False
                        ),
                        dcc.RadioItems(
                            id="radio-settings", 
                            options = []
                        )
                    ]
                    )
                )
            )
        ]),
        dbc.Card(
            dbc.CardBody(
                dcc.Graph(id="usa-graph")
            )
        ) 
    ])

    


sports_layout = html.Div([
    dcc.Store(id="sports-data"),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    html.H1("Sports statistics"),
                    style={"justify-content": "center", "align-items": "center", "display": "flex"}
                ),
                style={"height": "100%"}
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                        html.H5("Select sport:"),
                        dcc.Dropdown(id="sports-dropdown",
                                options=sport_options_dropdown,
                                value="Alpine Skiing")
                ]),
                style={"height": "100%"}
            ),
            width=2
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Select statistic:", className="pb-2"),
                    dcc.RadioItems(id='sport-statistics', 
                                    value="age")
                ]),
                style={"height": "100%"},
                className="",
            ),
            width=6
        )
    ],
        className="mt-4"),
    dbc.Card(
        dbc.CardBody(
            dcc.Graph(id="sports-graph")
        ),
        className="mt-4"
    )
])