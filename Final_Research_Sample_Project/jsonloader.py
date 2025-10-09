import pandas as pd
import sqlite3
import os #interact directly with the OS
def create_db():
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

#query methods 
#get issues by date
def get_issues_by_date():
    conn = sqlite3.connect('AiM_data.db')
    c = conn.cursor()
    user_date = input("What date would you like to receive summaries for? Please enter the date in the form of YYYY-MM-DD: ")
    c.execute("SELECT * FROM issues WHERE DATE(entDate) = ?", (user_date,))
    results = c.fetchall()
    conn.close()
    return results, user_date

#get the amount of tickets per shop within a date range
def get_amt_tickets_per_shop_in_range():
     conn = sqlite3.connect('AiM_data.db')
     c = conn.cursor()
     shop = input("Which shop would you like to recieve data for? i.e. CENTRAL ZONE, RESEARCH 3, LOCKSMITH\n")
     str_date = input("\nEnter the start date in the form of YYYY-MM-DD:\n")
     end_date = input("\nEnter the end date in the form of YYYY-MM-DD:\n")
     c.execute(""" 
        SELECT shop, 
        COUNT(*) FROM issues 
        WHERE shop = ? AND 
        DATE(entDate) BETWEEN ? AND ? 
    """, (shop, str_date, end_date))
     results = c.fetchall()
     conn.close()
     return results
 
#get the amount of emergencies within a shop within a date range
def get_amt_emergencies_by_shop_in_range():
    conn = sqlite3.connect('AiM_data.db')
    c = conn.cursor()
    shop = input("Which shop would you like to receive emergency data for? i.e. CENTRAL ZONE, RESEARCH 3, LOCKSMITH\n")
    str_date = input("\nEnter the start date in the form of YYYY-MM-DD:\n")
    end_date = input("\nEnter the end date in the form of YYYY-MM-DD:\n")
    c.execute("""
        SELECT shop, COUNT(*) 
        FROM issues 
        WHERE shop = ? AND priCode = 'EMERGENCY' AND DATE(entDate) BETWEEN ? AND ?
    """, (shop, str_date, end_date))
    results = c.fetchall()
    conn.close()
    return results

#get tickets by priority code
def get_tickets_by_priority_code():
    conn = sqlite3.connect('AiM_data.db')
    c = conn.cursor()
    priority = input("Enter the priority code (e.g., URGENT, ROUTINE, PROMPT ATTN):\n")
    str_date = input("\nEnter the start date in the form of YYYY-MM-DD:\n")
    end_date = input("\nEnter the end date in the form of YYYY-MM-DD:\n")
    num_results = int(input("\nHow many results would you like to display?\n"))
    c.execute("""
        SELECT proposal, shop, description, priCode, entDate
        FROM issues
        WHERE priCode = ? AND DATE(entDate) BETWEEN ? AND ?
        ORDER BY entDate ASC
    """, (priority, str_date, end_date))
    results = c.fetchmany(num_results)
    conn.close()
    return results
