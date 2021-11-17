from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from unique_medals import unique_medals

#FULL DATASETS

def import_world_data() -> pd.DataFrame: 
    """
    Imports and returns the full dataset.
    
    Returns
    -------
    pd.DataFrame
        Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC, 
                Games, Year, Season, City, Sport, Event and Medal. 
    """
    
    return pd.read_csv("Data/athlete_events_anonymized.csv")


def import_full_data_usa() -> pd.DataFrame:
    """
    Creates a dataframe that exclusively contains data from the US.
    
    Returns
    -------
    usa_data : pd.DataFrame
        Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC, 
                Games, Year, Season, City, Sport, Event and Medal. 
    """

    usa_data = import_world_data()
    usa_data = usa_data[usa_data["NOC"] == "USA"].reset_index(drop=True)
    
    return usa_data 


#MEDALS DATA

def import_medals_won() -> pd.DataFrame: 
    """
    Creates a dataframe, which contains only the winnings for the US.
    Since team winnings are counted per participants in the original dataset, 
    the function only returns the rows that are unique across event, games and medal.
    (However in the cases where there is a tie between two Americans, this will still not give the correct result.)
    
    Returns
    -------
    medals : pd.DataFrame
        Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event and Medal.
        The dataframe contains only the winnings for the US. 
    """

    usa_data = import_full_data_usa()
    medals = usa_data.dropna(subset=["Medal"])
    medals = medals.drop_duplicates(subset=["Event", "Games", "Medal"]).reset_index(drop=True)

    return medals


def import_medals_count() -> pd.DataFrame:
    """
    Creates a dataframe with information about the number of medals for each Olympic Game.

    Returns
    -------
    medals_merged_data : pd.DataFrame
        Columns: Year, Season, Games, Medals USA, Medals total and Percentage of Medals.
    """

    #Creates dataframes
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


def import_medals_per_sport_and_event() -> list:
    """
    Creates two dataframes (sport and event) with the number of medals for the US.

    Returns
    -------
    sport_and_event_data : list
        The returned list consists of two pd.DataFrames (first=Sport, second=Event).
        Columns: Sport or Event, Total medals, Gold, Silver and Bronze
    """

    #Import the data
    medals = import_medals_won()

    sport_and_event_data = []

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

        sport_and_event_data.append(number_medals)
    
    return sport_and_event_data


def import_top_ten_sports_and_events_all_medal_types() -> list:
    """
    Picks out the top ten sports and events for total, gold, silver and bronze medals.
    
    Returns
    -------
    sport_event_all_medals_data : list
        A list of two lists, each consisting of four dataframes (first list=Sport, second list=Event).
        Lists: [[top_ten_total, top_ten_gold, top_ten_silver, top_ten_bronze], [top_ten_total, top_ten_gold, top_ten_silver, top_ten_bronze]]
        Columns in dataframe: Sport or Event, Total medals, Gold, Silver and Bronze.
    """

    #Import the data
    sport_medals, event_medals = import_medals_per_sport_and_event()

    sport_event_all_medals_data = []

    for df in [sport_medals, event_medals]:

        #Sort the medals 
        top_ten_total = df.sort_values(by="Total medals", ascending=False).reset_index(drop=True).head(10)
        top_ten_gold = df.sort_values(by="Gold", ascending=False).reset_index(drop=True).head(10)
        top_ten_silver = df.sort_values(by="Silver", ascending=False).reset_index(drop=True).head(10)
        top_ten_bronze = df.sort_values(by="Bronze", ascending=False).reset_index(drop=True).head(10)

        sport_event_all_medals_data.append([top_ten_total, top_ten_gold, top_ten_silver, top_ten_bronze])
    
    return sport_event_all_medals_data 


#PARTICIPANTS (INCLUDING GENDER) DATA

def import_participants_data() -> pd.DataFrame:
    """
    Creates a dataframe with information about participants (number and gender) for US and the world.
    The participants are only counted once per Olympic Games (even though they participated in several events).
    
    Returns
    -------
    participants_data : pd.DataFrame
        A dataframe with information about participants (number and gender) for US and the world.
        Columns: Year, Season, Games, Participants from USA, Total Number of Participants, 
                American Participants (%), Number of Males from USA, Number of Females from USA, 
                Total Number Males, Total Number Females, Female Participants from USA (%), 
                Male Participants from USA (%), World Female Participants (%), World Male Participants (%)
    """

    #Import the data
    usa_data = import_full_data_usa()
    world_data = import_world_data()

    #Removes people who participate in several events (the ID:s should be unique for each Olympic Game).
    usa_data_unique_ID = usa_data.drop_duplicates(subset=["Games", "ID"])
    world_data_unique_ID = world_data.drop_duplicates(subset=["Games", "ID"])

    #Creates two dataframes for the participants and count the number of people for each olympic game and then merge them
    usa_participants = pd.DataFrame({"Participants from USA" : usa_data_unique_ID["ID"].groupby(usa_data_unique_ID["Games"]).count()}).reset_index()
    world_participants = pd.DataFrame({"Total Number of Participants" : world_data_unique_ID["ID"].groupby(world_data_unique_ID["Games"]).count()}).reset_index()
    participants_data = pd.merge(usa_participants, world_participants, on="Games", how="left")

    #Split the Games column into two and create Year and Season 
    year_season = participants_data["Games"].str.split(" ", n = 1, expand = True) #Splits each string in the Games column into two columns. Reference: https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
    participants_data.insert(0, "Year", year_season[0])
    participants_data.insert(1, "Season", year_season[1])
    participants_data["Year"] = participants_data["Year"].astype(int)

    #Calculates the percentage of American participants for each game
    participants_data["American Participants (%)"] = ((participants_data["Participants from USA"]/participants_data["Total Number of Participants"])*100).round(1)

    #Creates gender data for the US and the world
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

class SportStatistics:

    def __init__(self) -> None:
        read_data = import_world_data()
        sports = read_data[read_data["Sport"].isin(["Alpine Skiing", "Basketball", "Gymnastics", "Rhythmic Gymnastics"])]

        # Running does not have its own sport tag, its under Atheltics
        running_events = ["Athletics Women's 100 metres", "Athletics Women's 200 metres", "Athletics Women's 400 metres",  "Athletics Women's 800 metres", "Athletics Women's 1,500 metres", 
        "Athletics Women's 3,000 metres", "Athletics Women's 5,000 metres", "Athletics Women's 10,000 metres",  "Athletics Women's Marathon", "Athletics Men's 60 metres", 
        "Athletics Men's 100 metres", "Athletics Men's 200 metres", "Athletics Men's 400 metres", "Athletics Men's 800 metres", "Athletics Men's 1,500 metres", 
        "Athletics Men's 5,000 metres", "Athletics Men's 10,000 metres", "Athletics Men's Marathon"]
        running = read_data[read_data["Event"].isin(running_events)]
        
        # add Running to sports
        sports = sports.append(running)
        sports.reset_index(drop=True, inplace=True)

        # renaming Athletics to Running and Rhythmic Gymnastics to Gymnastics
        sports.loc[sports["Sport"] == "Athletics", "Sport"] = "Running"
        sports.loc[sports["Sport"] == "Rhythmic Gymnastics", "Sport"] = "Gymnastics"

        self._data = sports

    def sports(self) -> List:
        """Returns: Sorted list of sports"""
        return self._data["Sport"].sort_values().unique()

    def medals(self, sport, gender) -> DataFrame:
        """Returns: Medal count for top 10 countries based on sport and time period"""

        # select correct sport and time period
        medal_data = self.sport_and_year(sport)
        medal_data = unique_medals(medal_data)

        # selects geneder
        if gender == "both":
            medal_data = medal_data["Medal"].groupby(medal_data["NOC"]).count().sort_values(ascending=False).head(10)
        elif gender == "male":
            medal_data = medal_data[medal_data["Sex"] == "M"]["Medal"].groupby(medal_data["NOC"]).count().sort_values(ascending=False).head(10)
        else:
            medal_data = medal_data[medal_data["Sex"] == "F"]["Medal"].groupby(medal_data["NOC"]).count().sort_values(ascending=False).head(10)
        
        # prepare data for plot
        medal_data = pd.DataFrame(dict(NOC = medal_data.index, Medal = medal_data)).reset_index(drop=True)
        
        return medal_data

    def gender(self, sport) -> DataFrame:
        """Returns: gender count per year for selected sport and time period"""

        # select correct sport and time period
        gender_data = self.sport_and_year(sport)

        # male data
        gender_data_m = gender_data[gender_data["Sex"] == "M"]
        gender_data_m = gender_data_m["Sex"].groupby(gender_data_m["Year"]).count()

        # female data
        gender_data_f = gender_data[gender_data["Sex"] == "F"]
        gender_data_f = gender_data_f["Sex"].groupby(gender_data_f["Year"]).count()

        # prepare data for plot
        gender_data = pd.DataFrame(dict(Male = gender_data_m, Female = gender_data_f)).reset_index()

        return gender_data
    
    def age(self, sport) -> DataFrame:
        """Returns: ages of everyone in selected sport"""
        
        # select correct sport and time period
        age_data = self.sport_and_year(sport)

        # new DataFrame with all ages from males and females
        age_data = pd.DataFrame([age_data["Age"][age_data["Sex"] == "M"], 
                                    age_data["Age"][age_data["Sex"] == "F"]], 
                                    index=["Male", "Female"])
        age_data = age_data.transpose().reset_index(drop=True)

        return age_data

    def height_basketball(self, gender) -> DataFrame:
        """Returns: mean height per medal for basketball players for set time period"""

        # select basketball data from selected time period
        height_data = self.sport_and_year("Basketball")

        # select gender
        if gender == "male":
            height_data = height_data[height_data["Sex"] == "M"]
        elif gender == "female":
            height_data = height_data[height_data["Sex"] == "F"]
        else:
            pass

        # calculate mean height for players with a medal
        mean_hight_data = {}
        for medal in ["Gold", "Silver", "Bronze"]:
            mean_hight_data[medal] = height_data[height_data["Medal"] == medal]["Height"].mean()

        # add mean height for players without a medal
        mean_hight_data["No medal"] = height_data[height_data["Medal"].isna()]["Height"].mean()

        # prepare data for plot
        mean_hight_data = pd.DataFrame(mean_hight_data.items(), columns=["Medal", "Mean height"])
        
        # shorten to two decimals
        mean_hight_data["Mean height"] = mean_hight_data["Mean height"].apply('{:.2f}'.format)

        return mean_hight_data

    # help function for selecting sport and year
    def sport_and_year(self, sport) -> DataFrame:
        """Returns: Dataframe with specific sport and time period"""
        data = self._data[self._data["Sport"] == sport]

        return data

