import pandas as pd
import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "JSON", "AiM-Phases-Last-3-Months.json")

df = pd.read_json(file_path)
print(df.head())
