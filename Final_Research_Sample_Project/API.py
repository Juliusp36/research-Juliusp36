from dotenv import load_dotenv
import sqlite3
from google import genai
from jsonloader import get_issues_by_date
import requests 
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize():
    results, user_date = get_issues_by_date()
    if not results:
        print(f"No issues found for {user_date}.")
        return
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Summarize the following facility issues from {user_date}: {results}"
    )
    summary = response.text
    update_summary(summary, user_date)
    
    print("\nSummary:")
    print(summary)
    return summary
    

def update_summary(summary_text, user_date):
    conn = sqlite3.connect('AiM_data.db')
    c = conn.cursor()
    c.execute("""
        UPDATE issues 
        SET dailySummary = ? 
        WHERE DATE(entDate) = ?
    """, (summary_text, user_date))
    conn.commit()
    conn.close()
