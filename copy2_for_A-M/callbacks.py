import plotly_express as px
import pandas as pd
import plotly.figure_factory as ff

from dash.dependencies import Output, Input
from app import app
from noc_to_region import noc_to_region
from layouts import sport_statistics
from create_figures import PlotFigures

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

#A-Ms part

@app.callback(
    Output("graph-dropdown", "options"),
    Input("usa-dropdown", "value")
)
def update_graph_dropdown(choice):
    if choice == "medals":
        return [{"label" : medals_options_dict[index], "value" : index} for index in medals_options_dict]
    elif choice == "participants":
        return [{"label" : participants_options_dict[index], "value" : index} for index in participants_options_dict]
    
@app.callback(
    Output("radio-settings", "options"),
    Input("usa-dropdown", "value"),
    Input("graph-dropdown", "value")
)
def update_radio_buttons(choice1, choice2):
    
    if choice1 == "medals":
        if choice2 == "medals_year":
            return [{"label" : label, "value" : value} for value, label in medals_per_year_options_dict.items()]
        else:
            return [{"label" : label, "value" : value} for value, label in medals_per_sport_options_dict.items()]
    else:
        if choice2 == "participants":
            return [{"label" : label, "value" : value} for value, label in plot_participants_options_dict.items()]
        else :
            return [{"label" : label, "value" : value} for value, label in gender_options_dict.items()]

@app.callback(
    Output("my-toggle-switch", component_property="label"),
    Output("my-toggle-switch", component_property="disabled"),
    Input("usa-dropdown", "value"),
    Input("graph-dropdown", "value"),
    Input("radio-settings", "value")
)
def update_toggle_switch(choice1, choice2, choice3):
    if choice1 == "medals":
        if choice2 == "medals_year":
            return ("Number / Percentage", False) #TODO: Fix spaces
        else:
            return ("Event / Sport", False)
    else:
        if choice2 == "participants" and choice3 != "percentage":
            return ("Normal / Log-scaled", False)
        else:
            return ("Not available", True)


@app.callback(
    Output("usa-graph", "figure"),
    Input("usa-dropdown", "value"),
    Input("graph-dropdown", "value"),
    Input("radio-settings", "value"),
    Input("my-toggle-switch", "value")
)
def update_graph(choice1, choice2, choice3, choice4):
    if choice1 == "medals":
        if choice2 == "medals_year":
            return PlotFigures.plot_medals_per_year(season=choice3, percentage=choice4)
        else:
            return PlotFigures.plot_top_ten_sports_or_events(y_data=choice3, sport=choice4) #TODO: Change function, not interested in total here

    else:
        if choice2 == "participants":
            return PlotFigures.plot_participants(data_to_show=choice3, log_scaled=choice4)
        else:
            return PlotFigures.plot_gender_distribution(choice3)

#Dictionaries for Graph Dropdown
medals_options_dict = dict(medals_year = "Medals won per year", top_ten_sports_events = "Top ten sports or events")
participants_options_dict = dict(participants = "Participants from USA and the World", gender="Gender distribution for USA and the world")

#Dictionaries for Radio Buttons
medals_per_year_options_dict = dict(all = "All seasons", winter="Winter", summer="Summer") #percentage="Percentage or Total")
medals_per_sport_options_dict = dict(all = "All medals", Gold = "Gold", Silver = "Silver", Bronze = "Bronze", total = "Total number of medals") #sport_or_event="Sport or Event?", 
plot_participants_options_dict = dict(all = "All seasons", winter="Winter", summer="Summer", percentage="American Participants (%)") #, percentage="Percentage or Total", log_scaled="Yes or no?")
gender_options_dict = dict(all = "All seasons", winter="Winter", summer="Summer")
