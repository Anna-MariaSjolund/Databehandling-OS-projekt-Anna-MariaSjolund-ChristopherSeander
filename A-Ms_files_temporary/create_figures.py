from load_data import LoadDataUSA
import plotly.graph_objects as go
import plotly_express as px

class PlotFigures: 
     
    @staticmethod
    def plot_medals_per_season(season="all", percentage=True):

        #Imports the data
        medals_data = LoadDataUSA.medals_data()

        #Selects the data, sets the line color, color (if two lines) and creates data for when OG was hosted by USA
        if season == "all":
            dataset=medals_data
            line_color=["OrangeRed", "RoyalBlue"]
            color="Season"
            OG_in_USA = medals_data.iloc[[2, 11, 12, 22, 31, 32, 39, 42]].reset_index(drop=True) #Creates a dataset with data for when the Olympic Games were hosted by USA
        elif season == "summer":
            dataset=medals_data[medals_data["Season"] == "Summer"]
            line_color = ["OrangeRed"] 
            color=None
            OG_in_USA = medals_data.iloc[[2, 11, 32, 39]].reset_index(drop=True)
        elif season == "winter":
            dataset=medals_data[medals_data["Season"] == "Winter"]
            line_color=["RoyalBlue"]
            color=None
            OG_in_USA = medals_data.iloc[[12, 22, 31, 42]].reset_index(drop=True)

        #Sets the title
        if season == "all" and percentage == True:
            title = "Percentage of Medals Won by the USA in the Olympic Games"
        elif season == "all" and percentage == False:
            title = "Number of Medals Won by the USA in the Olympic Games"
        elif season == "summer" and percentage == True:
            title = "Percentage of Medals Won by the USA in the Summer Olympic Games"
        elif season == "summer"and percentage == False:
            title = "Number of Medals Won by the USA in the Summer Olympic Games"
        elif season == "winter" and percentage == True:
            title = "Percentage of Medals Won by the USA in the Winter Olympic Games"
        elif season == "winter" and percentage == False:
            title = "Number of Medals Won by the USA in the Winter Olympic Games"

        #Sets the y-data, hover_template and labels based on if values should be shown in percentage or not
        if percentage==True:
            y_data = "Percentage of Medals"
            hover_template = "<br>Year: %{x}<br>Percentage of Medals: %{y:.1f}%<extra></extra>"
            labels=None
        else:
            y_data = "Medals USA"
            hover_template = "<br>Year: %{x}<br>Number of Medals: %{y}<extra></extra>"
            labels={"Medals USA":"Number of medals"}

        #Creates the figure
        fig = px.line(dataset, 
                    x="Year", 
                    y=y_data,
                    labels=labels, 
                    color=color, 
                    title=title, 
                    color_discrete_sequence=line_color,
                    markers=True, 
                    )

        #Plot data for when the Olympic Games were hosted by USA
        fig.add_trace(go.Scatter(x=OG_in_USA["Year"], y=OG_in_USA[y_data], mode="markers", name="Olympic Games in USA", marker=dict(size=10, color="LightSeaGreen")))
        
        #Sets the hovertemplate
        fig.update_traces(hovertemplate=hover_template)

        #Sets the ticks
        fig.update_layout(
                        xaxis=(dict(
                        tickmode = "linear",
                        tick0 = 0,
                        dtick = 4,
                        )))

        return fig
    
    #TODO:Change name for this plot function and add documentation
    def plot_medals_per_sport(sport_or_event="sport", y_data=["Bronze", "Silver", "Gold"], total=False):

        if sport_or_event == "sport":
            dataset = LoadDataUSA.medals_top_ten_sports()
            x_data = "Sport"
            title="Top Ten Sports for USA in the Olympic Games"
        elif sport_or_event == "event":
            dataset = LoadDataUSA.medals_top_ten_events()
            x_data = "Event"
            title="Top Ten Events for USA in the Olympic Games"

        if total == False:
            bar_colors = []
            for medal in y_data:
                if medal == "Bronze":
                    bar_colors.append("#CD7F32")
                elif medal == "Silver":
                    bar_colors.append("#C0C0C0")
                elif medal == "Gold":
                    bar_colors.append("#FFD700")
        else:
            y_data = "Total medals"
            bar_colors = ["OliveDrab"]
            
        fig = px.bar(dataset, 
                        x=x_data, 
                        y=y_data, 
                        labels={"value":"Number of medals", "variable":"Medal Type"}, 
                        title=title,
                        barmode="group", 
                        color_discrete_sequence=bar_colors, 
                        template="plotly_white")
        return fig