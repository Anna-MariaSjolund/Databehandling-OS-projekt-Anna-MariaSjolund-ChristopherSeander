from dash import dcc, html
from load_data_chris import SportStatistics
from noc_to_region import noc_to_region

sport_statistics = SportStatistics()

sport_options_dropdown = [{"label" : sport, "value" : sport} for sport in sport_statistics.sports()]

usa_options_dict = dict(medals = "Medals",
                        participants = "Participants"
                        )

usa_options_dropdown = [{"label" : label, "value" : value} for value, label in usa_options_dict.items()]

usa_layout = html.Div([  
    html.H1("USA content"), 
    dcc.Dropdown(
        id="usa-dropdown",
        options=usa_options_dropdown,
        value="medals"
    ),
    dcc.Graph(id="usa-graph")
])

sports_layout = html.Div([ 
    dcc.Store(id="sports-data"),
    html.H1("Sports statistics content"),
    dcc.Dropdown(
        id="sports-dropdown",
        options=sport_options_dropdown,
        value="Alpine Skiing"
    ),
    dcc.Dropdown(id='sport-statistics', className='',
        value="age",
    ),
    html.H2(id="test-text"),
    dcc.Graph(id="sports-graph")
    
])