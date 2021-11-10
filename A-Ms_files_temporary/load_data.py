import pandas as pd

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
        number_medals_sport = pd.DataFrame({"Number of medals": medals["Medal"].groupby(medals["Sport"]).count()}).reset_index()

        number_medals_sport["Number of events"] = number_medals_sport["Sport"].apply(lambda row: len(medals[medals["Sport"] == row]["Event"].unique()))
        number_medals_sport["Medals per event"] = number_medals_sport["Number of medals"]/number_medals_sport["Number of events"]

        return number_medals_sport

    @staticmethod
    def top_ten_sports():
        medals = LoadDataUSA.medals_per_sport()
        top_sports = medals.sort_values(by="Number of medals", ascending=False).reset_index(drop=True)
        
        return top_sports.head(10)

    @staticmethod
    def top_ten_sports_average_medals_per_event():
        medals = LoadDataUSA.medals_per_sport()
        top_sports = medals.sort_values(by="Medals per event", ascending=False).reset_index(drop=True)
        
        return top_sports.head(10)
 
    @staticmethod 
    def top_ten_events():
        medals = LoadDataUSA.medals_won()
        medals_per_event = pd.DataFrame({"Number of medals": medals["Medal"].groupby(medals["Event"]).count()}).reset_index()
        medals_per_event = medals_per_event.sort_values(by="Number of medals", ascending=False).reset_index(drop=True)
        
        return medals_per_event.head(10)
    
    @staticmethod
    def medal_types_top_ten_sports():
        medals = LoadDataUSA.medals_won()
        sports_top_ten = LoadDataUSA.top_ten_sports()
        list_of_sports = list(sports_top_ten["Sport"])
        medals_won_per_type = pd.DataFrame({"Number medals won": medals["Medal"].groupby(medals["Sport"]).value_counts()}).reset_index()
        medals_won_per_type = medals_won_per_type[medals_won_per_type["Sport"].isin(list_of_sports)] #Reference: https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/
        
        return medals_won_per_type

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