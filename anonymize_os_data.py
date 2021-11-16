import pandas as pd
import hashlib as hl

os_data = pd.read_csv("Data/athlete_events.csv")

os_data["Name"] = os_data["Name"].apply(lambda name:hl.sha256(name.encode()).hexdigest())

os_data.to_csv("Data/athlete_events_anonymized.csv", index=False, header=True)