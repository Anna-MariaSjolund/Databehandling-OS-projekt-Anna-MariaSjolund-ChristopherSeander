import pandas as pd
from pandas.core.frame import DataFrame

def unique_medals(df) -> DataFrame:
    """Returns: DataFrame with unique medals per event/games"""
    data = df.dropna(subset=["Medal"])
    return data.drop_duplicates(subset=["Event", "Games", "Medal", "NOC"])