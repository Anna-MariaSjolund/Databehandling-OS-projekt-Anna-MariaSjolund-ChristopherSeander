import pandas as pd

# import noc_regions.csv
_noc = pd.read_csv("Data/noc_regions.csv")

# set NOC as index
_noc.set_index("NOC", inplace=True)

# remove the "notes" column
_noc = _noc["region"]

def noc_to_region(NOC) -> str:
    """Method that returns a string with the region name"""
    return _noc.loc[NOC]