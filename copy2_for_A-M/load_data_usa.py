import pandas as pd
 

#FULL DATASETS

def import_world_data() -> pd.DataFrame: 
    """
    Imports and returns the full dataset.
    
    Returns
    -------
    DataFrame with columns:
        ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event and Medal. 
    """
    
    return pd.read_csv("../Data/athlete_events.csv")


def import_full_data_usa() -> pd.DataFrame:
    """
    Creates a dataset that exclusively contains data from the US.
    
    Returns
    -------
    usa_data:pd.DataFrame
        Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event and Medal. 
    """

    usa_data = import_world_data()
    usa_data = usa_data[usa_data["NOC"] == "USA"].reset_index(drop=True)
    
    return usa_data 


#MEDALS DATA

def import_medals_won() -> pd.DataFrame: 
    """
    Creates a dataset that contains only the winnings for the US.
    Since team winnings are counted per participants in the original dataset, 
    the function only returns the rows that are unique across event, games and medal.
    (However in the cases where there is a tie between two Americans, this will not give the correct result.)
    
    Returns
    -------
    medals:pd.DataFrame
        Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event and Medal.
        The dataframe contains only the winnings for the US. 
    """

    usa_data = import_full_data_usa()
    medals = usa_data.dropna(subset=["Medal"])
    medals = medals.drop_duplicates(subset=["Event", "Games", "Medal"]).reset_index(drop=True)

    return medals


def import_medals_data() -> pd.DataFrame:
    """
    Creates a dataset with information about the number of medals for each Olympic Game.

    Returns
    -------
    medals_merged_data:pd.DataFrame
        Columns: Year, Season, Games, Medals USA, Medals total and Percentage of Medals.

    """

    #Creates datasets
    #Only include the rows where there are medals and do not include team sports
    sport_data = import_world_data().dropna(subset=["Medal"]).drop_duplicates(subset=["NOC", "Event", "Games", "Medal"])
    medals_usa = import_medals_won()

    #Counting the medals for USA for each Olympic Game and creating a new dataframe
    medals_usa = pd.DataFrame({"Medals USA": medals_usa["Medal"].groupby(medals_usa["Games"]).count()}).reset_index()
    year_season = medals_usa["Games"].str.split(" ", n = 1, expand = True) #Splits each string in the Games column into two columns. Reference: https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
    medals_usa.insert(0, "Year", year_season[0])
    medals_usa.insert(1, "Season", year_season[1])
    medals_usa["Year"] = medals_usa["Year"].astype(int)

    #Counting the total number of medals for each Olympic Game and creating a dataframe
    medals_total = pd.DataFrame({"Medals total": sport_data["Medal"].groupby(sport_data["Games"]).count()})
        
    #Merge the data (USA did not take part in the summer games of 1980, so this will not be included)
    medals_merged_data = pd.merge(medals_usa, medals_total, on="Games", how="left")

    #Add a column with the percentage of medals won by the US
    medals_merged_data["Percentage of Medals"] = (medals_merged_data["Medals USA"]/medals_merged_data["Medals total"])*100

    return medals_merged_data


"""def import_medals_per_sport() -> pd.DataFrame:
    medals = import_medals_won()
    number_medals_sport = pd.DataFrame({"Total medals": medals["Medal"].groupby(medals["Sport"]).count()}).reset_index()

    #This part is for plotting divided by the number of events
    number_medals_sport["Number of events"] = number_medals_sport["Sport"].apply(lambda row: len(medals[medals["Sport"] == row]["Event"].unique()))
    number_medals_sport["Medals per event"] = number_medals_sport["Total medals"]/number_medals_sport["Number of events"]

    return number_medals_sport"""


def import_medals_per_sport_and_event() -> list:
    """
    Creates two dataframes (sport and event) with the number of medals for the US.

    Returns
    -------
    return_data:list (of two pd.DataFrames)
        Columns: Sport/Event, Total medals, Gold, Silver and Bronze
    """

    #Import the data
    medals = import_medals_won()

    return_data = []

    for game in ["Sport", "Event"]:

        #Count the number of total, gold, silver and bronze medals per sport
        number_medals = pd.DataFrame({"Total medals": medals["Medal"].groupby(medals[game]).count()}).reset_index()
        number_gold = pd.DataFrame({"Gold": medals["Medal"][medals["Medal"] == "Gold"].groupby(medals[game]).count()}).reset_index()
        number_silver = pd.DataFrame({"Silver": medals["Medal"][medals["Medal"] == "Silver"].groupby(medals[game]).count()}).reset_index()
        number_bronze = pd.DataFrame({"Bronze": medals["Medal"][medals["Medal"] == "Bronze"].groupby(medals[game]).count()}).reset_index()
        
        #Merge the data
        number_medals = pd.merge(number_medals, number_gold, on=game, how="outer")
        number_medals = pd.merge(number_medals, number_silver, on=game, how="outer")
        number_medals = pd.merge(number_medals, number_bronze, on=game, how="outer")

        return_data.append(number_medals)
    
    return return_data


def import_top_ten_sports_and_events_all_medal_types():
    """Picks out the top ten sports and events for total, gold, silver and bronze.
    
    Returns
    -------
    return_data:list
        A list of two lists, each consisting of four dataframes.
        Columns: Sport/Event, Total medals, Gold, Silver and Bronze
    """

    #Import the data
    sport_medals, event_medals = import_medals_per_sport_and_event()

    return_data = []

    for df in [sport_medals, event_medals]:
        #Sort the medals 
        top_ten_total = df.sort_values(by="Total medals", ascending=False).reset_index(drop=True).head(10)
        top_ten_gold = df.sort_values(by="Gold", ascending=False).reset_index(drop=True).head(10)
        top_ten_silver = df.sort_values(by="Silver", ascending=False).reset_index(drop=True).head(10)
        top_ten_bronze = df.sort_values(by="Bronze", ascending=False).reset_index(drop=True).head(10)

        return_data.append([top_ten_total, top_ten_gold, top_ten_silver, top_ten_bronze])
    
    return return_data





"""def import_top_ten_sports_average_medals_per_event() -> pd.DataFrame:
    medals = import_medals_per_sport()
    top_sports = medals.sort_values(by="Medals per event", ascending=False).reset_index(drop=True)
    
    return top_sports.head(10)"""


"""def import_medals_top_ten_events() -> pd.DataFrame: 

    #Import the data
    medals_won_all = import_medals_won()

    #Create dataset with the number of medals per event and sort the medals by Total Medals
    medals_per_event = pd.DataFrame({"Total medals": medals_won_all["Medal"].groupby(medals_won_all["Event"]).count()}).reset_index()
    top_ten_events = medals_per_event.sort_values(by="Total medals", ascending=False).reset_index(drop=True).head(10)
    
    #Creates new data frame with the different medal types for the top ten sports
    list_of_events = list(top_ten_events["Event"])
    event_medals_top_ten = pd.DataFrame({"Total medals": medals_won_all["Medal"].groupby(medals_won_all["Event"]).value_counts()}).reset_index()
    event_medals_top_ten = event_medals_top_ten[event_medals_top_ten["Event"].isin(list_of_events)] #Reference: https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/

    #Change format
    event_medals_top_ten = event_medals_top_ten.pivot_table("Total medals", ["Event"], "Medal").reset_index() #Reference: https://stackoverflow.com/questions/17298313/python-pandas-convert-rows-as-column-headers
    event_medals_top_ten = event_medals_top_ten.rename_axis(None, axis=1) #Reference: https://stackoverflow.com/questions/29765548/remove-index-name-in-pandas
    
    #Merge the data
    event_medals_top_ten = event_medals_top_ten[["Event", "Bronze", "Silver", "Gold"]]
    event_medals_top_ten = pd.merge(event_medals_top_ten, top_ten_events, on="Event")
    event_medals_top_ten = event_medals_top_ten.sort_values(by="Total medals", ascending=False).reset_index(drop=True)

    return event_medals_top_ten"""      



#PARTICIPANTS (INCLUDING GENDER) DATA

def import_participants_data() -> pd.DataFrame:
    usa_data = import_full_data_usa()
    world_data = import_world_data()

    #Remove people who participate in several events (the ID:s should be unique for each game)
    usa_data_unique_ID = usa_data.drop_duplicates(subset=["Games", "ID"])
    world_data_unique_ID = world_data.drop_duplicates(subset=["Games", "ID"])

    #Create two dataframes for the participants and count the number of people for each olympic game and then merge them
    usa_participants = pd.DataFrame({"Participants from USA":usa_data_unique_ID["ID"].groupby(usa_data_unique_ID["Games"]).count()}).reset_index()
    world_participants = pd.DataFrame({"Total Number of Participants":world_data_unique_ID["ID"].groupby(world_data_unique_ID["Games"]).count()}).reset_index()
    participants_data = pd.merge(usa_participants, world_participants, on="Games", how="left")

    #Split the Games column into two and create Year and Season 
    year_season = participants_data["Games"].str.split(" ", n = 1, expand = True) #Splits each string in the Games column into two columns. Reference: https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
    participants_data.insert(0, "Year", year_season[0])
    participants_data.insert(1, "Season", year_season[1])
    participants_data["Year"] = participants_data["Year"].astype(int)

    #Calculates the percentage of american participants for each game
    participants_data["American Participants (%)"] = ((participants_data["Participants from USA"]/participants_data["Total Number of Participants"])*100).round(1)

    #Creates gender data
    gender_usa = pd.DataFrame({"Number of Males from USA":usa_data_unique_ID["Sex"][usa_data_unique_ID["Sex"] == "M"].groupby(usa_data_unique_ID["Games"]).count(),
                            "Number of Females from USA":usa_data_unique_ID["Sex"][usa_data_unique_ID["Sex"] == "F"].groupby(usa_data_unique_ID["Games"]).count()}).reset_index()
    gender_world = pd.DataFrame({"Total Number Males":world_data_unique_ID["Sex"][world_data_unique_ID["Sex"] == "M"].groupby(world_data_unique_ID["Games"]).count(),
                            "Total Number Females":world_data_unique_ID["Sex"][world_data_unique_ID["Sex"] == "F"].groupby(world_data_unique_ID["Games"]).count()}).reset_index()

    #Merge the gender data with the participants data and fill the NaN (created when there were no females in the data) with 0
    participants_data = pd.merge(participants_data, gender_usa, on="Games", how="left").fillna(0)
    participants_data = pd.merge(participants_data, gender_world, on="Games", how="left").fillna(0)

    #Calculates the percentage of female and male participants from USA and the world
    participants_data["Female Participants from USA (%)"] = ((participants_data["Number of Females from USA"]/participants_data["Participants from USA"])*100).round(1)
    participants_data["Male Participants from USA (%)"] = ((participants_data["Number of Males from USA"]/participants_data["Participants from USA"])*100).round(1)
    participants_data["World Female Participants (%)"] = ((participants_data["Total Number Females"]/participants_data["Total Number of Participants"])*100).round(1)
    participants_data["World Male Participants (%)"] = ((participants_data["Total Number Males"]/participants_data["Total Number of Participants"])*100).round(1)

    return participants_data

