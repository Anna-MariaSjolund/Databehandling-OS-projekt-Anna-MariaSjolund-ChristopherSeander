from load_data import LoadDataUSA
import plotly.graph_objects as go
import plotly_express as px

class PlotFigures:
    
    @staticmethod
    def plot_medals_per_season(percentage=True, summer=False, winter=False):

        medals_data = LoadDataUSA.medals_data()

        #Picks out data for when the Olympic Games were hosted by USA
        OG_in_USA = medals_data.iloc[[2, 11, 12, 22, 31, 32, 39, 42]].reset_index(drop=True)
        OG_in_USA_summer = medals_data.iloc[[2, 11, 32, 39]].reset_index(drop=True)
        OG_in_USA_winter = medals_data.iloc[[12, 22, 31, 42]].reset_index(drop=True)

        hover_template_percentage = '<br>Year: %{x}<br>Percentage of Medals: %{y:.1f}%<extra></extra>'
        hover_template_number = '<br>Year: %{x}<br>Number of Medals: %{y}<extra></extra>'

        if percentage == True and summer == True:
            fig = px.line(medals_data[medals_data["Season"] == "Summer"], 
                        x="Year", 
                        y="Percentage of Medals",
                        color_discrete_sequence=["OrangeRed"],
                        title="Percentage of Medals Won by the USA in the Summer Olympic Games",
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA_summer["Year"], y=OG_in_USA_summer["Percentage of Medals"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        elif percentage == False and summer == True:
            fig = px.line(medals_data[medals_data["Season"] == "Summer"], 
                        x="Year", 
                        y="Medals USA",
                        labels={"Medals USA":"Number of medals"},
                        color_discrete_sequence=["OrangeRed"],
                        title="Number of Medals Won by the USA in the Summer Olympic Games",
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA_summer["Year"], y=OG_in_USA_summer["Medals USA"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        elif percentage == True and winter == True:
            fig = px.line(medals_data[medals_data["Season"] == "Winter"], 
                        x="Year", 
                        y="Percentage of Medals", 
                        color_discrete_sequence=["RoyalBlue"],
                        title="Percentage of Medals Won by the USA in the Winter Olympic Games",
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA_winter["Year"], y=OG_in_USA_winter["Percentage of Medals"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        elif percentage == False and winter == True:
            fig = px.line(medals_data[medals_data["Season"] == "Winter"], 
                        x="Year", 
                        y="Medals USA",
                        labels={"Medals USA":"Number of medals"},
                        color_discrete_sequence=["RoyalBlue"],
                        title="Number of Medals Won by the USA in the Winter Olympic Games",
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA_winter["Year"], y=OG_in_USA_winter["Medals USA"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        elif percentage == True:    
            fig = px.line(medals_data, 
                        x="Year", 
                        y="Percentage of Medals", 
                        color="Season", 
                        title="Percentage of Medals Won by the USA in the Olympic Games", 
                        color_discrete_sequence=["OrangeRed", "RoyalBlue"],
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA["Year"], y=OG_in_USA["Percentage of Medals"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        elif percentage == False:    
            fig = px.line(medals_data, 
                        x="Year", 
                        y="Medals USA",
                        labels={"Medals USA":"Number of medals"}, 
                        color="Season", 
                        title="Number of Medals Won by the USA in the Olympic Games", 
                        color_discrete_sequence=["OrangeRed", "RoyalBlue"],
                        markers=True, 
                        )
            fig.add_trace(go.Scatter(x=OG_in_USA["Year"], y=OG_in_USA["Medals USA"], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))

        if percentage==True:
            fig.update_traces(hovertemplate=hover_template_percentage)
        else:
            fig.update_traces(hovertemplate=hover_template_number)
        
        fig.update_layout(
                        xaxis=(dict(
                        tickmode = "linear",
                        tick0 = 0,
                        dtick = 4,
                        )))

        return fig