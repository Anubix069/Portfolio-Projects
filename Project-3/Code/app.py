import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import time
import warnings
import requests

# ==== CONFIGURATION GÉNÉRALE ====
st.set_page_config(page_title="Books to Scrape", layout="wide")
st.title("📚 Books to Scrape - Dashboard")

# === FONCTION DE CHARGEMENT CSV (depuis GitHub) ===
@st.cache_data
def load_data_from_github():
    url = "https://raw.githubusercontent.com/clementlabois/Portfolio-Projects/main/Project-3/Data/books_data.csv"
    df = pd.read_csv(url)
    return df

# === SIDEBAR ===
choix_browser = st.sidebar.selectbox("🔧 Sélectionner le navigateur", ["chrome"])

choix = st.sidebar.radio("🌐 Navigation", [
    "📜 Présentation du projet",
    "🧑‍💻 Exploration des données",
    "📊 Visualisation simple",
    "📝 Visualisation textuelle"
])

# === 1. PRÉSENTATION DU PROJET ===
if choix == "📜 Présentation du projet":
    st.subheader("📖 Présentation du projet")
    st.markdown(""" Ce projet de **web scraping** permet de récupérer les informations des livres disponibles sur le site **Books to Scrape**. 
    L'objectif est de récupérer des données telles que le titre, le prix, la note, la catégorie et l'URL de chaque livre dans différentes catégories.

    Le projet utilise la bibliothèque **Selenium** pour naviguer sur le site web et récupérer les pages dynamiques, 
    et **BeautifulSoup** pour parser et extraire les données pertinentes. Ensuite, les données sont analysées et visualisées via **Streamlit**.

    Vous pouvez explorer les différentes visualisations de ces données dans les sections suivantes :
    - Exploration des données : Apperçu, statistiques descriptives, valeurs manquantes
    - Visualisation simple : Statistiques et graphiques généraux
    - Visualisation textuelle : Analyse des titres des livres avec des nuages de mots et des graphiques

    Le lien vers la source du site de livres : [Books to Scrape](https://books.toscrape.com/)
    """)

    st.markdown(
        """
        <div style="padding:10px 0 20px 0;">
            <h4 style="margin-bottom:5px; color:#555;">Créateur :</h4>
            <ul style="margin-top:0; padding-left:20px; color:#333;">
                <li><a href="https://www.linkedin.com/in/clementlabois" target="_blank" style="color:#1e5a77; text-decoration:none;">Clément Labois</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# === 2. Exploration des données ===
elif choix == "🧑‍💻 Exploration des données":
    st.subheader("🔍 Apperçu des données")
    df = load_data_from_github()
    st.write(df.head(10))

    column_df = pd.DataFrame(df.columns, columns=["Nom des Colonnes"])
    st.write(column_df)

    st.subheader("📊 Statistiques descriptives du Dataset")
    st.write(df["title"].describe())
    st.write(df["price"].describe())
    st.write(df["rating"].describe())
    st.write(df["category"].describe())

    # Calculer le pourcentage de valeurs manquantes par colonne
    st.subheader("Valeurs manquantes")
    missing_data = pd.DataFrame({
        "Colonne" : df.columns,
        "Pourcentage de valeur manquantes (%)" : [
        df[column].isna().sum() / len(df) * 100 for column in df.columns    
        ]
    })

    st.write(missing_data)

# === 3. VISUALISATION SIMPLE ===
elif choix == "📊 Visualisation simple":
    st.subheader("📈 Visualisations générales")
    df = load_data_from_github()
    df.rename(columns={"price": "Prix"}, inplace=True)

    # FILTRE PAR PRIX ET CATEGORIE (avec option 'All')
    prix_min, prix_max = st.slider("💰 Filtrer par gamme de prix", min_value=int(df['Prix'].min()), max_value=int(df['Prix'].max()), value=(int(df['Prix'].min()), int(df['Prix'].max())))
    categorie = st.selectbox("📂 Filtrer par catégorie", ['All'] + list(df['category'].unique()))

    if categorie == 'All':
        df_filtered = df[(df['Prix'] >= prix_min) & (df['Prix'] <= prix_max)]
    else:
        df_filtered = df[(df['Prix'] >= prix_min) & (df['Prix'] <= prix_max) & (df['category'] == categorie)]

    # Graphique par gamme de prix
    price_bins = [0, 5, 10, 15, 20, 25, 30, 40, 50, 100]
    price_labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-40", "40-50", "50+"]
    df_filtered['Price_Bin'] = pd.cut(df_filtered['Prix'], bins=price_bins, labels=price_labels, right=False)

    st.subheader("🔍 Répartition des livres par prix")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df_filtered, x='Price_Bin', palette="viridis", ax=ax)
    ax.set_title("Répartition des livres par gamme de prix")
    st.pyplot(fig)

    # Distribution des prix
    st.subheader("📉 Distribution des prix")
    fig2 = plt.figure()
    sns.histplot(df_filtered["Prix"], kde=True, bins=20, color="skyblue")
    st.pyplot(fig2)

    # Distribution des notes
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df_filtered['rating'] = df_filtered['rating'].map(rating_map)
    
    st.subheader("⭐ Répartition des notes")
    fig3 = plt.figure()
    sns.countplot(x="rating", data=df_filtered, palette="viridis")
    st.pyplot(fig3)

    # Top catégories bien notées (≥4)
    df_top = df_filtered[df_filtered['rating'] >= 4]
    if not df_top.empty:
        st.subheader("👍 Catégories avec livres très bien notés (≥4)")
        fig4 = plt.figure(figsize=(10, 4))
        df_top['category'].value_counts().plot(kind='bar', color='teal')
        st.pyplot(fig4)

# === 4. VISUALISATION TEXTUELLE ===
elif choix == "📝 Visualisation textuelle":
    st.subheader("🔡 Analyse des titres de livres")
    df = load_data_from_github()
    df.rename(columns={"price": "Prix"}, inplace=True)
    df['Prix'] = df['Prix'].astype(float)
    df['Rating'] = df['rating'].map({'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5})

    # FILTRE PAR PRIX ET CATEGORIE (avec option 'All')
    prix_min, prix_max = st.slider("💰 Filtrer par gamme de prix", min_value=int(df['Prix'].min()), max_value=int(df['Prix'].max()), value=(int(df['Prix'].min()), int(df['Prix'].max())))
    categorie = st.selectbox("📂 Filtrer par catégorie", ['All'] + list(df['category'].unique()))

    if categorie == 'All':
        df_filtered = df[(df['Prix'] >= prix_min) & (df['Prix'] <= prix_max)]
    else:
        df_filtered = df[(df['Prix'] >= prix
