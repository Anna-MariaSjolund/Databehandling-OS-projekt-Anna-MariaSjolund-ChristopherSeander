import dash_bootstrap_components as dbc
import dash_daq as daq

from dash import dcc, html
from load_data import SportStatistics
from noc_to_region import noc_to_region

# SportStatistics object
sport_statistics = SportStatistics()

# drop down meny for chosing sport
sport_options_dropdown = [{"label" : sport, "value" : sport} for sport in sport_statistics.sports()]

#USA LAYOUT

#Creates the options for the first dropdown (Medals or Participants)
usa_options_dict = dict(medals = "Medals", participants = "Participants")
usa_options_dropdown = [{"label" : label, "value" : value} for value, label in usa_options_dict.items()]

usa_layout = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Category:"),
                            dcc.Dropdown(
                                id="usa-dropdown",
                                options=usa_options_dropdown,
                                value="medals",
                                clearable=False)
                            ], 
                            ), style={"height": "100%"}                    
                        ), 
                    xl=2, lg=2, md=6, sm=12
                    ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Data:"),
                            dcc.Dropdown(
                                id="second-dropdown",
                                value="medals_year",
                                clearable=False),
                            ],
                            ), style={"height": "100%"}
                        ), 
                    xl=4, lg=4, md=6, sm=12
                    ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Graph Settings:"),
                            dcc.RadioItems(
                                id="radio-settings", 
                                value="all",
                                style={"display" : "inline-block", "width" : "80%"}) #Reference: https://social.msdn.microsoft.com/Forums/en-US/9880882b-212a-4bc1-8932-8676784e4299/exact-alignment-of-radio-buttons-in-rows-and-columns?forum=asphtmlcssjavascript
                            ],
                            ), style={"height": "100%"}
                        ), 
                    xl=4, lg=4, md=8, sm=12
                    ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            daq.ToggleSwitch(
                                id="my-toggle-switch",
                                value=True,
                                size=40,
                                color="CornFlowerBlue",
                                labelPosition="bottom"),
                            ),style={"height": "100%"}
                        ), 
                    xl=2, lg=2, md=4, sm=12
                )],
                className="mt-4"
            ),
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(id="usa-graph")
                    ),
            className="mt-4" ) 
        ])

# SPORTS LAYOUT

sports_layout = html.Div([
    dcc.Store(id="sports-data"),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                        html.H5("Select sport:"),
                        dcc.Dropdown(id="sports-dropdown",
                                options=sport_options_dropdown,
                                value="Alpine Skiing",
                                clearable=False)
                ]),
                style={"height": "100%"}
            ),
            xl=2,
            md=3
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
            xl=7,
            md=5
        ),
        dbc.Col(
            id="third-box",
            xl=3,
            md=4
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

# gender selection card, is not showed all the time
gender_selection = dbc.Card(
dbc.CardBody([
    html.H5("Select gender:", className="pb-2"),
    dcc.RadioItems(id='gender-selection',
                    options=[{"label" : gender, "value" : gender.strip(" ").lower()} for gender in [" Both", " Male", " Female"]],
                    value="both")
    ]),
    style={"height": "100%"}
)

# callback breaks if this doesnt exist
hidden_gender_selection = dbc.RadioItems(id='gender-selection', value="both")