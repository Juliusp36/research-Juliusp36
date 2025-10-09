import requests
import pandas as pd
#Marketstack API key: ommitted for security reasons 
#this project sends requests to the marketstack api and recieves ticker information

API_KEY = "___"
User_I = input("What ticker would you like to recieve data for?\n")
SYMBOL = User_I.upper()
BASE_URL = "https://api.marketstack.com/v1"
FEATURE = f"/tickers/{SYMBOL}"

params = {
    "access_key": API_KEY,

}

response = requests.get(BASE_URL + FEATURE ,params=params)


if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    
    df_cleaned = pd.json_normalize(data)
    print(df_cleaned)
    
else:
    print(response.status_code)
