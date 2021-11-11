import pandas as pd

#TODO: Save the new dataset with hashed names and use that instead

class LoadDataUSA:

    @staticmethod  
    def full_data():
        usa_data = LoadSportData.full_data()
        usa_data = usa_data[usa_data["NOC"] == "USA"].reset_index(drop=True)
        
        return usa_data 
    
    @staticmethod
    def medals_won():
        usa_data = LoadDataUSA.full_data()
        medals = usa_data.dropna(subset=["Medal"])
        medals = usa_data.drop_duplicates(subset=["Event", "Games", "Medal"])

        return medals

    @staticmethod 
    def medals_data():
        #Loads data from USA and the full sport data
        sport_data = LoadSportData.sport_data_per_team()
        medals_usa = LoadDataUSA.medals_won()

        #Counting the medals for USA
        medals_usa = pd.DataFrame({"Medals USA": medals_usa["Medal"].groupby(medals_usa["Games"]).count()}).reset_index()
        year_season = medals_usa["Games"].str.split(" ", n = 1, expand = True) #Splits each string in the Games column into two columns. Reference: https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
        medals_usa.insert(0, "Year", year_season[0])
        medals_usa.insert(1, "Season", year_season[1])

        #Counting the total number of medals
        medals_total = pd.DataFrame({"Medals total": sport_data["Medal"].groupby(sport_data["Games"]).count()})
            
        #Merge the data (USA did not take part in the games of 1980 summer)
        medals_merged_data = pd.merge(medals_usa, medals_total, on="Games", how="left")
        medals_merged_data["Percentage of Medals"] = (medals_merged_data["Medals USA"]/medals_merged_data["Medals total"])*100
 
        return medals_merged_data
  
    @staticmethod
    def medals_per_sport():
        medals = LoadDataUSA.medals_won()
        number_medals_sport = pd.DataFrame({"Total medals": medals["Medal"].groupby(medals["Sport"]).count()}).reset_index()

        number_medals_sport["Number of events"] = number_medals_sport["Sport"].apply(lambda row: len(medals[medals["Sport"] == row]["Event"].unique()))
        number_medals_sport["Medals per event"] = number_medals_sport["Total medals"]/number_medals_sport["Number of events"]

        return number_medals_sport

    @staticmethod
    def medals_top_ten_sports():

        #Import the data
        medals_won_all = LoadDataUSA.medals_won()
        sport_medals = LoadDataUSA.medals_per_sport()

        #Sort the medals by Total Medals
        top_ten_sports = sport_medals.sort_values(by="Total medals", ascending=False).reset_index(drop=True).head(10)

        #Creates new data frame with the different medal types for the top ten sports
        list_of_sports = list(top_ten_sports["Sport"]) #Creates a list of the names for the sports in the top_ten_sports
        sport_medals_top_ten = pd.DataFrame({"Total medals": medals_won_all["Medal"].groupby(medals_won_all["Sport"]).value_counts()}).reset_index()
        sport_medals_top_ten = sport_medals_top_ten[sport_medals_top_ten["Sport"].isin(list_of_sports)] #Reference: https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/

        #Change format
        sport_medals_top_ten = sport_medals_top_ten.pivot_table("Total medals", ["Sport"], "Medal").reset_index() #Reference: https://stackoverflow.com/questions/17298313/python-pandas-convert-rows-as-column-headers
        sport_medals_top_ten = sport_medals_top_ten.rename_axis(None, axis=1) #Reference: https://stackoverflow.com/questions/29765548/remove-index-name-in-pandas
        sport_medals_top_ten = sport_medals_top_ten[["Sport", "Bronze", "Silver", "Gold"]]
        
        #Merge the data
        sport_medals_top_ten = pd.merge(sport_medals_top_ten, top_ten_sports, on="Sport")
        sport_medals_top_ten = sport_medals_top_ten.sort_values(by="Total medals", ascending=False).reset_index(drop=True)

        return sport_medals_top_ten

    @staticmethod
    def top_ten_sports_average_medals_per_event():
        medals = LoadDataUSA.medals_per_sport()
        top_sports = medals.sort_values(by="Medals per event", ascending=False).reset_index(drop=True)
        
        return top_sports.head(10)
  
    @staticmethod 
    def medals_top_ten_events(): 

        #Import the data
        medals_won_all = LoadDataUSA.medals_won()

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

        return event_medals_top_ten      
    
    @staticmethod
    def participants_data():
        usa_data = LoadDataUSA.full_data()
        world_data = LoadSportData.full_data()

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

class LoadSportData:

    @staticmethod
    def full_data(): 
        sport_data = pd.read_csv("../Data/athlete_events.csv")

        return sport_data

    @staticmethod
    def sport_data_per_team():
        sport_data_team = LoadSportData.full_data()
        sport_data_team = sport_data_team.dropna(subset=["Medal"]).drop_duplicates(subset=["NOC", "Event", "Games", "Medal"])
        
        return sport_data_team