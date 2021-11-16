from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from unique_medals import unique_medals

class SportStatistics:

    def __init__(self) -> None:
        read_data = pd.read_csv("../Data/athlete_events_anonymized.csv")
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

    def medals(self, sport, from_year = 0) -> DataFrame:
        """Returns: Medal count for top 10 countries based on sport and time period"""

        # select correct sport and time period
        medal_data = self.sport_and_year(sport, from_year)
        medal_data = unique_medals(medal_data)

        # prepair data for plot
        medal_data = medal_data["Medal"].groupby(medal_data["NOC"]).count().sort_values(ascending=False).head(10)
        medal_data = pd.DataFrame(dict(NOC = medal_data.index, Medal = medal_data)).reset_index(drop=True)
        
        return medal_data

    def gender(self, sport, from_year = 0) -> DataFrame:
        """Returns: gender count per year for selected sport and time period"""

        # select correct sport and time period
        gender_data = self.sport_and_year(sport, from_year)

        # male data
        gender_data_m = gender_data[gender_data["Sex"] == "M"]
        gender_data_m = gender_data_m["Sex"].groupby(gender_data_m["Year"]).count()

        # female data
        gender_data_f = gender_data[gender_data["Sex"] == "F"]
        gender_data_f = gender_data_f["Sex"].groupby(gender_data_f["Year"]).count()

        # prepair data for plot
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

    def height_basketball(self, from_year = 0) -> DataFrame:
        """Returns: mean height per medal for basketball players for set time period"""

        # select basketball data from selected time period
        height_data = self.sport_and_year("Basketball", from_year)

        # calculate mean height for players with a medal
        mean_hight_data = {}
        for medal in ["Gold", "Silver", "Bronze"]:
            mean_hight_data[medal] = height_data[height_data["Medal"] == medal]["Height"].mean()

        # add mean height for players without a medal
        mean_hight_data["No medal"] = height_data[height_data["Medal"].isna()]["Height"].mean()

        # prepair data for plot
        mean_hight_data = pd.DataFrame(mean_hight_data.items(), columns=["Medal", "Mean height"])

        return mean_hight_data

    # help function for selecting sport and year
    def sport_and_year(self, sport, from_year = 0) -> DataFrame:
        """Returns: Dataframe with specific sport and time period"""
        data = self._data[self._data["Sport"] == sport]
        data = data[data["Year"] >= from_year]

        return data