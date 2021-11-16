import load_data_usa
import plotly.graph_objects as go
import plotly_express as px 

def plot_medals_per_year(season:str="all", percentage:bool=True) -> px.line:
    """
    Creates a plotly line graph, showing the US winnings in the Olympic Games.

    Parameters
    ----------
    season : str
        The season to be shown, i.e. all, summer or winter (default all).
    percentage : bool
        If the medals should be shown in percentage of the total number of medals (else in numbers; default True).

    Returns
    -------
    fig : px.line
        A line graph figure with year on the x-axis and medals on the y-axis.
    """

    #Imports the data
    medals_data = load_data_usa.import_medals_count()

    #Selects the data, sets the line color, color (if two lines) and creates data for when the Olympic Games was hosted by USA.
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
    if percentage == True:
        y_data = "Percentage of Medals"
        hover_template = "<br>Year: %{x}<br>Percentage of Medals: %{y:.1f}%<extra></extra>"
        labels=None
    else:
        y_data = "Medals USA"
        hover_template = "<br>Year: %{x}<br>Number of Medals: %{y}<extra></extra>"
        labels = {"Medals USA" : "Number of Medals"}

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

    #Settings for line
    fig.update_traces(line=dict(width=3), marker=dict(size=8))

    #Plot data for when the Olympic Games were hosted by USA
    fig.add_trace(go.Scatter(x=OG_in_USA["Year"], y=OG_in_USA[y_data], mode="markers", name="Olympic Games in USA", marker=dict(size=12, color="LightSeaGreen")))
    
    #Sets the hovertemplate for all lines
    fig.update_traces(hovertemplate=hover_template)

    #Sets the ticks and formats the background
    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)), 
                    template="plotly_dark", 
                    paper_bgcolor= "rgba(0, 0, 0, 0)", 
                    plot_bgcolor= "rgba(0, 0, 0, 0)")

    #Formats the axes                
    fig.update_xaxes(gridcolor="gray", zerolinecolor="gray")
    fig.update_yaxes(gridcolor="gray", zerolinecolor="gray")

    return fig


def plot_top_ten_sports_or_events(y_data:str="all", sport:bool=True) -> px.bar:
    """
    Creates a plotly bar graph, showing the top sports (most medals) for the US.

    Parameters
    ----------
    y_data : str
        The medals to be shown (default all).
        This should be either:
            all: Showing gold, silver and bronze for the ten sports/events with most medals in total.
            Gold: Showing the ten sports/events with the most number of golds.
            Silver: Showing the ten sports/events with the most number of silvers.
            Bronze: Showing the ten sports/events with the most number of bronzes.
            total: Showing the total number of medals for the ten sports/events with most medals.
    sport : bool
        If sport (default) should be shown (if False, event will be shown).

    Returns
    -------
    fig : px.bar
        A bar graph figure with sport or event on the x-axis and number of medals on the y-axis.
    """

    #Imports the data
    sport_data, event_data = load_data_usa.import_top_ten_sports_and_events_all_medal_types()
    sport_total, sport_gold, sport_silver, sport_bronze = sport_data
    event_total, event_gold, event_silver, event_bronze = event_data

    #Select the datasets
    if (y_data == "all" and sport == True) or (y_data == "total" and sport == True):
        dataset = sport_total
    elif (y_data == "all" and sport == False) or (y_data == "total" and sport == False):
        dataset = event_total 
    elif y_data == "Gold" and sport == True:
        dataset = sport_gold
    elif y_data == "Gold" and sport == False:
        dataset = event_gold
    elif y_data == "Silver" and sport == True:
        dataset = sport_silver
    elif y_data == "Silver" and sport == False:
        dataset = event_silver
    elif y_data == "Bronze" and sport == True:
        dataset = sport_bronze
    elif y_data == "Bronze" and sport == False:
        dataset = event_bronze

    #Sets the x-data
    if sport == True:
        x_data = "Sport"
    else:
        x_data = "Event"

    #Sets the title
    if y_data == "all" or y_data == "total":
        title = f"Top Ten {x_data}s for USA in the Olympic Games"
    else:    
        title = f"{x_data}s with the Most {y_data} Medals for USA in the Olympic Games"

    #Settings for y_data and bar_colors
    colors_dict = dict(Bronze="#CD7F32", Silver="#C0C0C0", Gold="#FFD700")
    if y_data == "all": 
        y_data = ["Bronze", "Silver", "Gold"]  
        bar_colors = ["#CD7F32", "#C0C0C0", "#FFD700"]
    elif y_data == "total":
        y_data = "Total medals"
        bar_colors = ["OliveDrab"]
    else:
        bar_colors = [colors_dict[y_data]]

    #Creates the plot
    fig = px.bar(dataset, 
                    x=x_data, 
                    y=y_data, 
                    labels={"value" : "Number of Medals", 
                            "variable" :"Medal Type", 
                            "Gold" : "Number of Gold Medals",
                            "Silver" : "Number of Silver Medals", 
                            "Bronze" : "Number of Bronze Medals",
                            "Total medals" : "Total Number of Medals"}, 
                    title=title,
                    barmode="group", 
                    color_discrete_sequence=bar_colors, 
                    )
    
    #Settings for axis and layout
    fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_layout(template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
            
    return fig


def plot_participants(data_to_show:str="All", log_scaled:bool=True):
    """
    Creates a plotly line graph, showing the number of US participants in the Olympic Games per year.

    Parameters
    ----------
    season : str
        The season to be shown, i.e. All, Summer or Winter (default All).
    log_scaled : bool
        If the medals should be shown log-scaled or not (default True).

    Returns
    -------
    fig:px.line
        A line graph figure with year on the x-axis and number of participants on the y-axis.
    """

    #Import the data, create datasets for summer and winter and set the initial y_data
    participants_data = load_data_usa.import_participants_data()
    participants_summer = participants_data[participants_data["Season"] == "Summer"]
    participants_winter = participants_data[participants_data["Season"] == "Winter"]
    y_data = ["Total Number of Participants", "Participants from USA"]

    #Settings for Summer and Winter 
    if data_to_show == "Summer":
        dataset = participants_summer
        line_color = ["#c90016", "#f08080"]
    elif data_to_show == "Winter":
        dataset = participants_winter
        line_color=["#1560bd", "#b0c4de"]
    elif data_to_show == "Percentage":
        dataset = participants_data
        y_data = "American Participants (%)"
        y_label = "American Participants (%)"
        log_scaled = False
        line_color=["OliveDrab"]
    
    #Sets the title
    if data_to_show == "All":
        title = "Participants from the USA and the World in the Olympic Games"
    elif data_to_show == "Percentage":
        title = "American Participants in the Olympic Games in Percentage"
    else:
        title = f"Participants from the USA and the World in the {data_to_show} Olympic Games"

    #Sets the y-label
    if log_scaled == True and data_to_show != "Percentage":
        y_label = "Number of Participants (log-scaled)"
    elif log_scaled == False and data_to_show != "Percentage":
        y_label = "Number of Participants"
   
    #Creates the figure
    if data_to_show == "All":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                    x=participants_summer["Year"], 
                    y=participants_summer["Total Number of Participants"], 
                    customdata=participants_summer["Season"], 
                    hovertemplate="Year: %{x}<br>Season: %{customdata}<br>Total Number of Participants: %{y}<extra></extra>",
                    mode="lines+markers", 
                    name="Total Number of Participants (summer)", 
                    marker=dict(color="#c90016")))
        fig.add_trace(go.Scatter(
                    x=participants_winter["Year"], 
                    y=participants_winter["Total Number of Participants"], 
                    customdata=participants_winter["Season"],
                    hovertemplate="Year: %{x}<br>Season: %{customdata}<br>Total Number of Participants: %{y}<extra></extra>",
                    mode="lines+markers", 
                    name="Total Number of Participants (winter)", 
                    marker=dict(color="#1560bd"))) 
        fig.add_trace(go.Scatter(
                    x=participants_summer["Year"], 
                    y=participants_summer["Participants from USA"], 
                    customdata=participants_summer["Season"], 
                    hovertemplate="Year: %{x}<br>Season: %{customdata}<br>Participants from USA: %{y}<extra></extra>", 
                    mode="lines+markers", 
                    name="Participants from USA (summer)", 
                    marker=dict(color="#f08080")))
        fig.add_trace(go.Scatter(
                    x=participants_winter["Year"], 
                    y=participants_winter["Participants from USA"], 
                    customdata=participants_winter["Season"], 
                    hovertemplate="Year: %{x}<br>Season: %{customdata}<br>Participants from USA: %{y}<extra></extra>",
                    mode="lines+markers", 
                    name="Participants from USA (winter)", 
                    marker=dict(color="#b0c4de")))
   
    else:
        fig = px.line(dataset, 
                x="Year", 
                y=y_data, 
                color_discrete_sequence=line_color,
                markers=True,
                log_y=log_scaled,
                title=title, #title has to be set here as well (even though updated below), otherwise the grid is not evenly spaced for log-scaled Winter
                labels={"variable":"Participant Group", "value":"Number of Participants"}
                )

    #General settings for all plots
    fig.update_traces(line=dict(width=3), marker=dict(size=8))   
    fig.update_layout(title=title, yaxis_title=y_label, legend_title="Participant Group")

    #Log-scaling
    if log_scaled == True and data_to_show == "All":
        fig.update_yaxes(type="log")

    #Sets the ticks and formats the background
    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)), 
                    template="plotly_dark", 
                    paper_bgcolor= "rgba(0, 0, 0, 0)", 
                    plot_bgcolor= "rgba(0, 0, 0, 0)")

    #Formats the axes                
    fig.update_xaxes(gridcolor="gray", zerolinecolor="gray")
    fig.update_yaxes(gridcolor="gray", zerolinecolor="gray")

    return fig


def plot_gender_distribution(season="all"):
    """
    Creates a plotly line graph, showing the gender distribution for US and the world.

    Parameters
    ----------
    season : str
        The season to be shown, i.e. all, summer or winter (default all).

    Returns
    -------
    fig : px.line
        A line graph figure with year on the x-axis and the gender distribution on the y-axis.
    """
    
    #Import the data
    participants_data = load_data_usa.import_participants_data()

    #Sets the title and overwrites the participants_data for summer and winter
    if season == "all":
        title = "Gender Distribution among Participants from USA and the World at the Olympic Games"
    elif season == "summer":
        participants_data = participants_data[participants_data["Season"] == "Summer"]
        title = "Gender Distribution among Participants from USA and the World at the Summer Olympic Games"
    elif season == "winter":
        participants_data = participants_data[participants_data["Season"] == "Winter"]
        title = "Gender Distribution among Participants from USA and the World at the Winter Olympic Games"

    #Creates the plot
    fig = px.line(participants_data, 
            x="Year", 
            y=["World Male Participants (%)", "Male Participants from USA (%)", "World Female Participants (%)", "Female Participants from USA (%)"], 
            title=title, 
            labels={"value" : "Percentage", "variable" : "Participant Group"}, 
            color_discrete_sequence=["RoyalBlue", "LightSteelBlue", "DeepPink", "LightPink"],
            markers=True)

    #Sets the line width and the marker size
    fig.update_traces(line=dict(width=3), marker=dict(size=8))

    #Sets the ticks and formats the background
    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)), 
                    template="plotly_dark", 
                    paper_bgcolor= "rgba(0, 0, 0, 0)", 
                    plot_bgcolor= "rgba(0, 0, 0, 0)")

    #Formats the axes                
    fig.update_xaxes(gridcolor="gray", zerolinecolor="gray")
    fig.update_yaxes(gridcolor="gray", zerolinecolor="gray")

    return fig