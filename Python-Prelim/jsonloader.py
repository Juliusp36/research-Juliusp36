import pandas as pd
import os #interact directly with the OS

#obtain current directory and join it with AiM data file
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "JSON", "AiM-Phases-Last-3-Months.json")

dataframe = pd.read_json(file_path)
normalizeddf = pd.json_normalize(dataframe)
print(dataframe.head())



#flatten json file feilds
#create and add to a database with all of the colums in the json file, with an 
#additional column titled 'Summary' that begins null and will be filled by the AI generated summaries 
# via API as requests are made

#Summary column should pertain to the day and specific ticket right now
#SQLite > os library > API
