import plotly_express as px
import pandas as pd
import plotly.figure_factory as ff

from dash.dependencies import Output, Input
from app import app
from noc_to_region import noc_to_region
from layouts import sport_statistics
from create_figures import PlotFigures

sport_statistics_dict = dict(age = "Age distribution",
                                        athlete = "Athlete info",
                                        gender = "Gender distribution", 
                                        medals = "Most medals")
no_athlete_info_dict = dict(age = "Age distribution",
                                        gender = "Gender distribution", 
                                        medals = "Most medals")

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
    Input("sport-statistics", "value")  # select which statistic that should be shown
)
def update_sports_graph(df_json, statistic):
    data = pd.read_json(df_json)

    # most medals per country
    if statistic == "medals":
        fig = px.bar(data, x="NOC", y="Medal", color="NOC")
        fig.update_xaxes(tickmode='array',
                        tickvals = data["NOC"],
                        ticktext=[noc_to_region(NOC) for NOC in data["NOC"]])
        return fig
    
    # gender distribution
    if statistic == "gender":
        fig = px.line(data, x="Year", y=["Male", "Female"])
        return fig

    # age distribution
    if statistic == "age":
        # ff.create_distplot needs the data as list of lists
        data_split = [data[data["Male"].notna()]["Male"], data[data["Female"].notna()]["Female"]]
        fig = ff.create_distplot(data_split, data.columns)

        return fig

    # -----------WORKS ONLY FOR BASKETBALL RIGHT NOW-----------
    if statistic == "athlete":
        fig = px.bar(data, x="Medal", y="Mean height")

        return fig


@app.callback(
    Output("usa-graph", "figure"),   # return outputs to here
    Input("usa-dropdown", "value")  # select which statistic that should be shown
)   
def update_sports_graph(category):
    # most medals per country 
    if category == "medals":
        return PlotFigures.plot_participants() 


@app.callback(Output("filtered-df", "data"), 
            Input("stock-picker-dropdown", "value"), 
            Input("time-slider", "value"))

def filter_df(stock, time_index):
    """Filters the dataframe and stores in intermediary for callbacks.
    
    Returns:
        json object of filtered dataframe.
    """
    #Called dff because we "filter" the df
    dff_daily, dff_intraday = df_dict[stock] #df_dict[stock] gives us a list of two stocks (both dataframes) which we unpack

    dff = dff_intraday if time_index <= 2 else dff_daily

    #It is a dictionary because we want to map 0-6 (i) to the number of days
    #The list in enumerate is the number of days (365*5 the number of days for five years)
    days = {i:day for i, day in enumerate([1, 7, 30, 90, 365, 365*5])}

    #If time_index is 6 it should be set to max
    #time_index is 0 to 6 
    dff = dff if time_index == 6 else filter_time(dff, days[time_index])
    
    return dff.to_json() #We change our dff to json