import plotly_express as px
import pandas as pd
import plotly.figure_factory as ff

from dash.dependencies import Output, Input
from app import app
from noc_to_region import noc_to_region
from layouts import sport_statistics

sport_statistics_dict = dict(age = " Age distribution",
                            athlete = " Athlete info",
                            gender = " Gender distribution", 
                            medals = " Most medals")
no_athlete_info_dict = dict(age = " Age distribution",
                            gender = " Gender distribution", 
                            medals = " Most medals")

@app.callback(
    Output("sport-statistics", "options"),
    Input("sports-dropdown", "value")
)
def update_sports_statistics_dropdown(sport):
    if sport == "Basketball":
        return [{"label" : sport_statistics_dict[index], "value" : index} for index in sport_statistics_dict]
    else:
        return [{"label" : no_athlete_info_dict[index], "value" : index} for index in no_athlete_info_dict]


# updates dcc.Store based on chosen sport and stat
@app.callback(
    Output("sports-data", "data"),
    Input("sports-dropdown", "value"),
    Input("sport-statistics", "value"),
)
def filtered_sports(sport, statistic):
    if statistic == "medals":
        return sport_statistics.medals(sport).to_json()

    if statistic == "gender":
        return sport_statistics.gender(sport).to_json()

    if statistic == "age":
        return sport_statistics.age(sport).to_json()
    
    if statistic == "athlete":
        return sport_statistics.height_basketball().to_json()

# Text
@app.callback(
    Output("test-text", "children"),
    Input("sports-dropdown", "value"),
    Input("sport-statistics", "value")
)
def print_name_of_sport(sport, statistic):
    return f"{sport_statistics_dict[statistic]} for {sport.lower()}"

# displays graph
@app.callback(
    Output("sports-graph", "figure"),   # return outputs to here
    Input("sports-data", "data"),       # gets data based on which country is chosen
    Input("sport-statistics", "value"),  # select which statistic that should be shown
    Input("sports-dropdown", "value"),
)
def update_sports_graph(df_json, statistic, sport):
    data = pd.read_json(df_json)

    # most medals per country
    if statistic == "medals":
        fig = px.bar(data, x="NOC", y="Medal", color="NOC")
        fig.update_xaxes(tickmode='array',
                        tickvals = data["NOC"],
                        ticktext=[noc_to_region(NOC) for NOC in data["NOC"]],
                        gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_layout(title=f"Countries with most medals in {sport.lower()}", template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
        return fig
    
    # gender distribution
    if statistic == "gender":
        fig = px.line(data, x="Year", y=["Male", "Female"], labels={"value" : "Number", "variable" : "Gender"})
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_layout(title=f"Gender distribution for {sport.lower()}", template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
        return fig

    # TODO gender choice
    # age distribution
    if statistic == "age":
        # ff.create_distplot needs the data as list of lists
        hover_template = "<br>Age: %{x:.1f}<extra></extra>"
        
        data_split = [data[data["Male"].notna()]["Male"], data[data["Female"].notna()]["Female"]]
        fig = ff.create_distplot(data_split, data.columns, curve_type="normal", show_hist=False, show_rug=False)
        fig.update_traces(hovertemplate=hover_template)
        fig.update_layout(title=f"Normal distribution for ages in {sport.lower()}", xaxis_title="Age", yaxis_title="Density", template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
        return fig

    # -----------WORKS ONLY FOR BASKETBALL RIGHT NOW-----------
    if statistic == "athlete":
        fig = px.bar(data, x="Medal", y="Mean height")
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_layout(title=f"Mean height of players based on which medal", template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
        return fig