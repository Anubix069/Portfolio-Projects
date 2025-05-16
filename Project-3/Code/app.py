import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from wordcloud import WordCloud
import time
import warnings

# ==== CONFIGURATION GÉNÉRALE ====
st.set_page_config(page_title="Books Dashboard", layout="wide")
st.title("📚 Books Dashboard")

# === FONCTION DE CHARGEMENT CSV ===
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/clementlabois/Portfolio-Projects/main/Project-3/Data/books_data.csv"  # URL directe vers le fichier CSV brut
    df = pd.read_csv(url)
    return df

# === SIDEBAR ===
choix = st.sidebar.radio("🌐 Navigation", [
    "📜 Présentation du projet",
    "🧑‍💻 Exploration des données",
    "📊 Visualisation simple",
    "📝 Visualisation textuelle"
])

# === 1. PRÉSENTATION DU PROJET ===
if choix == "📜 Présentation du projet":
    st.subheader("📖 Présentation du projet")
    st.markdown("""
    Ce projet permet d'explorer des données sur les livres extraites du site **Books to Scrape**. 
    Les informations incluent le titre, le prix, la note, la catégorie et l'URL de chaque livre.

    Le projet utilise des outils comme **Pandas**, **Streamlit**, et **Seaborn** pour analyser et visualiser ces données.

    Vous pouvez explorer les différentes visualisations dans les sections suivantes :
    - Exploration des données : Apperçu, statistiques descriptives, valeurs manquantes
    - Visualisation simple : Statistiques et graphiques généraux
    - Visualisation textuelle : Analyse des titres de livres avec des nuages de mots et des graphiques

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
    df = load_data()
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
    df = load_data()
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
    df_filtered['Gamme de prix'] = pd.cut(df_filtered['Prix'], bins=price_bins, labels=price_labels, right=False)
    prix_count = df_filtered['Gamme de prix'].value_counts().reindex(price_labels)

    st.markdown("<h4 style='text-align: center;'>📊 Répartition des livres par gamme de prix</h4>", unsafe_allow_html=True)    
    fig1, ax1 = plt.subplots()
    bars = ax1.bar(prix_count.index, prix_count.values, color=plt.cm.coolwarm(range(len(prix_count))))
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, int(bar.get_height()), ha='center')
    ax1.set_xlabel("Gamme de prix (£)")
    ax1.set_ylabel("Nombre de livres")
    st.pyplot(fig1)

    # Distribution des prix
    st.markdown("<h4 style='text-align: center;'>📉 Distribution des prix</h4>", unsafe_allow_html=True)    
    fig2 = plt.figure()
    sns.histplot(df_filtered["Prix"], kde=True, bins=20, color="skyblue")
    st.pyplot(fig2)

    # Distribution des notes
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df_filtered['rating'] = df_filtered['rating'].map(rating_map)
    
    st.markdown("<h4 style='text-align: center;'>⭐ Répartition des notes</h4>", unsafe_allow_html=True)
    fig3 = plt.figure()
    sns.countplot(x="rating", data=df_filtered, palette="viridis")
    st.pyplot(fig3)

    # Top catégories bien notées (≥4)
    df_top = df_filtered[df_filtered['rating'] >= 4]
    if not df_top.empty:
        st.markdown("<h4 style='text-align: center;'>👍 Catégories avec livres très bien notés (≥4)</h4>", unsafe_allow_html=True)
        fig4 = plt.figure(figsize=(10, 4))
        df_top['category'].value_counts().plot(kind='bar', color='teal')
        st.pyplot(fig4)

# === 4. VISUALISATION TEXTUELLE ===
elif choix == "📝 Visualisation textuelle":
    st.subheader("🔡 Analyse des titres de livres")
    df = load_data()
    df.rename(columns={"price": "Prix"}, inplace=True)
    df['Prix'] = df['Prix'].astype(float)
    df['Rating'] = df['rating'].map({'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5})

    # FILTRE PAR PRIX ET CATEGORIE (avec option 'All')
    prix_min, prix_max = st.slider("💰 Filtrer par gamme de prix", min_value=int(df['Prix'].min()), max_value=int(df['Prix'].max()), value=(int(df['Prix'].min()), int(df['Prix'].max())))
    categorie = st.selectbox("📂 Filtrer par catégorie", ['All'] + list(df['category'].unique()))

    if categorie == 'All':
        df_filtered = df[(df['Prix'] >= prix_min) & (df['Prix'] <= prix_max)]
    else:
        df_filtered = df[(df['Prix'] >= prix_min) & (df['Prix'] <= prix_max) & (df['category'] == categorie)]

    # Analyse des mots et visualisation du nuage de mots
    stopwords = set(["the", "a", "and", "of", "to", "in", "with", "for", "an", "on", "is", "that", "by", "at"])

    def tokenize(text):
        words = re.findall(r"[A-Za-z']+", str(text).lower())
        return [w for w in words if w not in stopwords]

    records = []
    for _, row in df_filtered.iterrows():
        if isinstance(row['title'], str):
            for w in tokenize(row['title']):
                records.append((w, row['Rating']))

    words_df = pd.DataFrame(records, columns=['word', 'rating'])
    freq = Counter(words_df['word'])
    most_common = dict(freq.most_common(20))
    avg_rating = words_df[words_df['word'].isin(most_common)] \
                    .groupby('word')['rating'].mean()

    wc_df = pd.DataFrame({
        'count': most_common,
        'avg_rating': avg_rating
    }).sort_values('count', ascending=False)

    # Graphe barres 
    st.markdown("<h4 style='text-align: center;'>🔡 Mots les plus fréquents</h4>", unsafe_allow_html=True)
    fig5 = plt.figure(figsize=(10, 4))
    sns.barplot(x=wc_df.index, y=wc_df['count'])
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig5)

    # Graphe fréquence vs note moyenne
    st.markdown("<h4 style='text-align: center;'>📈 Fréquence vs Note moyenne</h4>", unsafe_allow_html=True)
    fig6 = plt.figure(figsize=(10, 4))
    plt.scatter(wc_df['count'], wc_df['avg_rating'])
    for word, row in wc_df.iterrows():
        plt.text(row['count'], row['avg_rating'], word, fontsize=9)
    plt.xlabel('Fréquence')
    plt.ylabel('Note moyenne')
    st.pyplot(fig6)

    # Word cloud
    st.markdown("<h4 style='text-align: center;'>☁️ Nuage de mots</h4>", unsafe_allow_html=True)
    fig7 = plt.figure(figsize=(10, 6))
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap='viridis')
    wordcloud.generate_from_frequencies(most_common)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig7)
