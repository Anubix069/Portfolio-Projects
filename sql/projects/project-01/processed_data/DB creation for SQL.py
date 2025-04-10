import pandas as pd
from sqlalchemy import create_engine

# Path of CSV file
chemin_csv = r"C:\your_path\tuberculosis_xray_dataset.csv"

# Reading of CSV file
df = pd.read_csv(chemin_csv)

# Creation of DataBase SQLite in "Documents"
engine = create_engine(r'sqlite:///C:/your_path/Documents/tuberculosis_xray.db')

# Insert data in the table
df.to_sql("xray_data", con=engine, if_exists="replace", index=False)

print("✅ Fichier .db successfully created in Documents.")