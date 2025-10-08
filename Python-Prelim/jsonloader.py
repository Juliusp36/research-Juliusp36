import pandas as pd
import sqlite3
import os #interact directly with the OS

#obtain current location of this file and join it with AiM data file to create a correct file path regardless of the system 
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "JSON", "AiM-Phases-Last-3-Months.json")

dataframe = pd.read_json(file_path)
normalized_df = pd.json_normalize(dataframe["ResultSet"]["Results"]) #flattens the json file, converting it from a list, to a table. Because we had nested json objects, we add the "Results" and "Resultset" parameters in brackets to flatten all of the data

#to make the database more viewable, we use this line to remove "fields." from in front of each category. This issue was initially caused by "title" being the header for the issues within the json file
normalized_df.columns = normalized_df.columns.str.replace(r"^fields\.", "", regex=True)

if "fields" in normalized_df.columns: 
    normalized_df = pd.json_normalize(normalized_df["fields"]) #flattens the final nested objects within the json file, "fields"

#directly assign summary classes 
normalized_df["dailySummary"] = None
normalized_df["ticketSummary"] = None

db_path = os.path.join(base_dir,"AiM_data.db") #create a file path to hold the database 
conn = sqlite3.connect(db_path) #create or open the database at the file path with the name "AiM_data.db"
cursor = conn.cursor() 

normalized_df.to_sql("issues", conn, schema=None, if_exists='replace',index=False,chunksize=None, dtype=None, method=None )

conn.commit()
conn.close()

#flatten json file fields
#create and add to a database with all of the colums in the json file, with an 
#additional column titled 'Summary' that begins null and will be filled by the AI generated summaries 
# via API as requests are made

#Summary column should pertain to the day and specific ticket right now
#SQLite > os library > API
