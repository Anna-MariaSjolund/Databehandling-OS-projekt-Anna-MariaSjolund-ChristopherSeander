import plotly_express as px
import pandas as pd
import plotly.figure_factory as ff

from dash.dependencies import Output, Input
from app import app
from noc_to_region import noc_to_region
from layouts import sport_statistics, gender_selection, hidden_gender_selection

# includes mean height
sport_statistics_dict = dict(age = " Age distribution",
                            athlete = " Mean height",
                            gender = " Gender distribution", 
                            medals = " Most medals")
# standard choices
no_athlete_info_dict = dict(age = " Age distribution",
                            gender = " Gender distribution", 
                            medals = " Most medals")

# line colors
line_colors = ['cyan', 'magenta']
male_color = ['cyan']
female_color = ['magenta']

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
    Input("gender-selection", "value")
)
def filtered_sports(sport, statistic, gender):
    if statistic == "medals":
        return sport_statistics.medals(sport, gender).to_json()

    if statistic == "gender":
        return sport_statistics.gender(sport).to_json()

    if statistic == "age":
        return sport_statistics.age(sport).to_json()
    
    if statistic == "athlete":
        return sport_statistics.height_basketball(gender).to_json()

# displays graph
@app.callback(
    Output("sports-graph", "figure"),   # return outputs to here
    Input("sports-data", "data"),       # gets data based on which country is chosen
    Input("sport-statistics", "value"), # select which statistic that should be shown
    Input("sports-dropdown", "value"),   # get which sport that is chosen
    Input("gender-selection", "value")
)
def update_sports_graph(df_json, statistic, sport, gender):
    data = pd.read_json(df_json)

    # most medals per country
    if statistic == "medals":
        fig = px.bar(data, 
                    x="NOC", 
                    y="Medal", 
                    color="NOC", 
                    labels={"Medal" : "Number of medals"},
                    text="Medal")
        
        # layout and colors
        fig.update_layout(title=f"Countries with most medals in {sport.lower()}", 
                            template='plotly_dark', 
                            paper_bgcolor= 'rgba(0, 0, 0, 0)', 
                            plot_bgcolor= 'rgba(0, 0, 0, 0)')
        fig.update_xaxes(tickmode='array',
                        tickvals = data["NOC"],
                        ticktext=[noc_to_region(NOC) for NOC in data["NOC"]],
                        gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
                
        return fig
    
    # gender distribution
    if statistic == "gender":
        fig = px.line(data, x="Year", 
                        y=["Male", "Female"], 
                        labels={"value" : "Number of athletes", "variable" : "Gender"},
                        color_discrete_sequence=line_colors)
        
        # layout and colors
        fig.update_layout(title=f"Gender distribution for {sport.lower()}", 
                            template='plotly_dark', 
                            paper_bgcolor= 'rgba(0, 0, 0, 0)', 
                            plot_bgcolor= 'rgba(0, 0, 0, 0)')
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')

        return fig

    # age distribution
    if statistic == "age":
        if gender == "both":
            # ff.create_distplot needs the data as list of lists
            data_split = [data[data["Male"].notna()]["Male"], data[data["Female"].notna()]["Female"]]
            fig = ff.create_distplot(data_split, 
                                    data.columns, 
                                    curve_type="normal", 
                                    show_hist=False, 
                                    show_rug=False, 
                                    colors=line_colors)
        elif gender == "male":
            fig = ff.create_distplot([data[data["Male"].notna()]["Male"]], ["Male"], 
                                        curve_type="normal", 
                                        show_hist=False, 
                                        show_rug=False, 
                                        colors=male_color)
        else: 
           fig = ff.create_distplot([data[data["Female"].notna()]["Female"]], ["Female"], 
                                    curve_type="normal", 
                                    show_hist=False, 
                                    show_rug=False, 
                                    colors=female_color)
       
        # hover format
        hover_template = "<br>Age: %{x:.1f}<extra></extra>"
        fig.update_traces(hovertemplate=hover_template)

        # layout and colors
        fig.update_layout(title=f"Normal distribution for ages in {sport.lower()}", 
                            xaxis_title="Age", 
                            yaxis_title="Density", 
                            template='plotly_dark', 
                            paper_bgcolor= 'rgba(0, 0, 0, 0)', 
                            plot_bgcolor= 'rgba(0, 0, 0, 0)')
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')

        return fig
    
    # mean height for Basketball
    if statistic == "athlete":
        if gender == "male":
            bar_color = px.colors.sequential.Teal
        elif gender == "female":
            bar_color = px.colors.sequential.Magenta
        else:
            bar_color = px.colors.sequential.turbid
        
        fig = px.bar(data, 
                    x="Medal", 
                    y="Mean height", 
                    text="Mean height",
                    color="Medal",
                    color_discrete_sequence=bar_color)
        
        # layout and colors
        fig.update_layout(title=f"Mean height of players per medal", 
                            template='plotly_dark', 
                            paper_bgcolor= 'rgba(0, 0, 0, 0)', 
                            plot_bgcolor= 'rgba(0, 0, 0, 0)')
        fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
        fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
               
        return fig

@app.callback(
    Output("third-box", "children"),
    Input("sport-statistics", "value")
)
def update_third_box(statistic):
    if statistic == "medals":
        return gender_selection

    if statistic == "gender":
        return hidden_gender_selection

    if statistic == "age":
        return gender_selection
    
    if statistic == "athlete":
        return gender_selection