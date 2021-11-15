import load_data_usa
import plotly.graph_objects as go
import plotly_express as px

def plot_medals_per_year(season="all", percentage=True):

    #Imports the data
    medals_data = load_data_usa.import_medals_data()

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
    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)))

    fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_layout(template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    return fig

#Maybe change it to Bronze, Silver, Gold, All medals, Total number
#def plot_top_ten_sports_or_events(sport_or_event="sport", y_data=["Bronze", "Silver", "Gold"], total=False):
def plot_top_ten_sports_or_events(y_data="all", sport=True):

    sport_data, event_data = load_data_usa.import_top_ten_sports_and_events_all_medal_types()
    sport_total, sport_gold, sport_silver, sport_bronze = sport_data
    event_total, event_gold, event_silver, event_bronze = event_data

    if sport == True:
        x_data = "Sport"
        title="Top Ten Sports for USA in the Olympic Games"
    else:
        x_data = "Event"
        title="Top Ten Events for USA in the Olympic Games"

    if y_data == "all":
        if sport == True:
            dataset=sport_total
        else:
            dataset=event_total
        y_data = ["Bronze", "Silver", "Gold"]
        bar_colors = ["#CD7F32", "#C0C0C0", "#FFD700"] 
    elif y_data == "Bronze":
        if sport == True:
            dataset=sport_bronze
        else:
            dataset=event_bronze
        bar_colors = ["#CD7F32"]
    elif y_data == "Silver":
        if sport == True:
            dataset=sport_silver
        else:
            dataset=event_silver
        bar_colors = ["#C0C0C0"]
    elif y_data == "Gold":
        if sport == True:
            dataset=sport_gold
        else:
            dataset=event_gold
        bar_colors = ["#FFD700"]
    elif y_data == "total":
        if sport == True:
            dataset=sport_total
        else:
            dataset=event_total
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
    
    fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_layout(template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')
            
    return fig

def plot_participants(data_to_show = "all", log_scaled=True):

    participants_data = load_data_usa.import_participants_data()
    y_data = ["Participants from USA", "Total Number of Participants"]

    if data_to_show == "all":
        color="Season"
        line_color = ["OrangeRed", "RoyalBlue"]
        title="Participants from the USA and the World in the Olympic Games"
    elif data_to_show == "summer":
        participants_data = participants_data[participants_data["Season"] == "Summer"]
        line_color = ["IndianRed", "DarkRed"]
        title="Participants from the USA and the World in the Summer Olympic Games"
    elif data_to_show == "winter":
        participants_data = participants_data[participants_data["Season"] == "Winter"]
        line_color=["CornflowerBlue", "Navy"]
        title="Participants from the USA and the World in the Winter Olympic Games"
    
    if data_to_show == "summer" or data_to_show == "winter" or data_to_show == "percentage":
        color=None

    if log_scaled == True:
        y_label = "Number of Participants (log-scaled)"
    else:
        y_label = "Number of Participants"

    if data_to_show == "percentage":
        y_data = "American Participants (%)"
        log_scaled = False
        line_color=["OliveDrab"]
        title = "American Participants in the Olympic Games in Percentage"

    fig = px.line(participants_data, 
            x="Year", 
            y=y_data,
            color=color, 
            log_y=log_scaled,
            labels={"value":y_label, "variable": "Participants"}, 
            color_discrete_sequence=line_color,
            title=title,
            markers=True,
            )

    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)))

    fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_layout(template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    return fig


def plot_gender_distribution(season="all"):
    
    participants_data = load_data_usa.import_participants_data()

    if season == "all":
        title = "Gender Distribution among Participants from USA and the World at the Olympic Games"
    elif season == "summer":
        participants_data = participants_data[participants_data["Season"] == "Summer"]
        title = "Gender Distribution among Participants from USA and the World at the Summer Olympic Games"
    elif season == "winter":
        participants_data = participants_data[participants_data["Season"] == "Winter"]
        title = "Gender Distribution among Participants from USA and the World at the Winter Olympic Games"

    fig = px.line(participants_data, 
            x="Year", 
            y=["Female Participants from USA (%)", "Male Participants from USA (%)", "World Female Participants (%)", "World Male Participants (%)"], 
            title=title, 
            labels={"value":"Percentage", "variable": "Participant Group"}, 
            color_discrete_sequence=["LightPink", "CornflowerBlue", "DeepPink", "MidnightBlue"],
            markers=True, 
            )

    fig.update_layout(xaxis=(dict(tickmode = "linear", tick0 = 0, dtick = 4)))

    fig.update_xaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_yaxes(gridcolor='gray', zerolinecolor='gray')
    fig.update_layout(template='plotly_dark', paper_bgcolor= 'rgba(0, 0, 0, 0)', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    return fig