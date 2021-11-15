import dash_bootstrap_components as dbc

from dash import dcc, html
from load_data import SportStatistics
from noc_to_region import noc_to_region

sport_statistics = SportStatistics()

sport_options_dropdown = [{"label" : sport, "value" : sport} for sport in sport_statistics.sports()]

usa_layout = html.Div([
    html.H1("USA content")
])

sports_layout = html.Div([
    dcc.Store(id="sports-data"),
    html.H1("Sports statistics", className="pt-3"),
    
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
            md=4
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
            md=3
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
#style={"justify-content": "center", "align-items": "center", "display": "flex"}

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