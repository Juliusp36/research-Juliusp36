import pandas as pd
import os 
import sqlite3
from dotenv import load_dotenv
from google import genai
from jsonloader import create_db, get_issues_by_date,get_amt_emergencies_by_shop_in_range,get_amt_tickets_per_shop_in_range,get_tickets_by_priority_code
from API import summarize,update_summary

load_dotenv()

def main():
    create_db()

    while True:
        print("""
        Welcome to the AiM Data Client!
        What would you like to do? (Enter the number corresponding to your choice):
        
        (Current database date range: 2025-02-13 to 2025-05-13)
        
        1. Receive a summary for a day of issues 
        2. Receive the amount of tickets per shop within a date range
        3. Receive the amount of emergencies within a shop within a date range
        4. Receive tickets by priority code
        5. Exit
        """)

        choice = input("\nEnter your choice: ")
        if choice == "1":
            summarize()
        elif choice == "2":
            print(get_amt_tickets_per_shop_in_range())
        elif choice == "3":
            print(get_amt_emergencies_by_shop_in_range())
        elif choice == "4":
            print(get_tickets_by_priority_code())
        elif choice == "5": 
            break
        else:
            print("Invalid choice. Please select 1–4.")

if __name__ == "__main__":
    main()
