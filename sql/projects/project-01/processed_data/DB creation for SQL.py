import pandas as pd
from sqlalchemy import create_engine

# Chemin du fichier CSV
chemin_csv = r"C:\your_path\tuberculosis_xray_dataset.csv"

# Lire le fichier CSV
df = pd.read_csv(chemin_csv)

# Créer la base de données SQLite dans "Documents"
engine = create_engine(r'sqlite:///C:/your_path/Documents/tuberculosis_xray.db')

# Insérer les données dans la table
df.to_sql("xray_data", con=engine, if_exists="replace", index=False)

print("✅ Fichier .db créé avec succès dans Documents.")