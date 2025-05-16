import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import time
import warnings

# ==== CONFIGURATION GÉNÉRALE ====
st.set_page_config(page_title="Books to Scrape", layout="wide")
st.title("📚 Books to Scrape - Dashboard")

# ==== CHEMIN VERS LE CSV ====
CSV_PATH = Path(__file__).resolve().parent.parent / "Data" / "books_data.csv"

# === FONCTION DE CHARGEMENT CSV ===
@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

# === FONCTION DE SCRAPING ===
def run_scraping():
    if platform.system() == "Linux":
        st.error("⚠️ Le scraping Selenium n’est pas disponible sur Streamlit Cloud.")
        st.stop()

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from urllib.parse import urljoin

    start_time = time.time()
    warnings.filterwarnings("ignore")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2
    })
    service = Service(log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "https://books.toscrape.com/"
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category_links = soup.select("div.side_categories ul li ul li a")

    books = []
    for link in category_links:
        category_name = link.text.strip()
        category_url = urljoin(base_url, link['href'])
        driver.get(category_url)

        while True:
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            book_items = page_soup.select("article.product_pod")

            for book in book_items:
                title = book.h3.a["title"]
                price = book.select_one("p.price_color").text[1:]
                rating_class = book.select_one("p.star-rating")["class"][1]
                detail_url = urljoin(category_url, book.h3.a["href"])
                image_url = urljoin(category_url, book.find('img')['src'])

                books.append({
                    "title": title,
                    "price": float(price),
                    "rating": rating_class,
                    "category": category_name,
                    "url": detail_url,
                    "image_url": image_url
                })

            next_button = page_soup.select_one("li.next a")
            if next_button:
                next_url = urljoin(category_url, next_button['href'])
                driver.get(next_url)
            else:
                break

    driver.quit()
    df = pd.DataFrame(books)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False, encoding='utf-8')
    duration = time.time() - start_time
    return df, duration


# === FONCTION DE CHARGEMENT CSV ===
@st.cache_data
def load_data():
    return pd.read_csv("data/books_data.csv")

# === SIDEBAR ===
choix = st.sidebar.radio("🌐 Navigation", [
    "📜 Présentation du projet",
    "🔄 Web Scraping",
    "🧑‍💻 Exploration des données",
    "📊 Visualisation simple",
    "📝 Visualisation textuelle"
])

# === 1. PRÉSENTATION DU PROJET ===
if choix == "📜 Présentation du projet":
    st.subheader("📖 Présentation du projet")
    st.markdown("""
    Ce projet de **web scraping** permet de récupérer les informations des livres disponibles sur le site **Books to Scrape**. 
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

# === 2. WEB SCRAPING ===
elif choix == "🔄 Web Scraping":
    st.subheader("📥 Lancer le scraping")
    if st.button("🛠️ Scraper les livres"):
        df, duration = run_scraping()
        st.success(f"{len(df)} livres récupérés en {duration:.2f} secondes.")
        st.dataframe(df.head())

    elif os.path.exists("data/books_data.csv"):
        df = load_data()
        st.info("💾 Fichier existant chargé.")
        st.dataframe(df.head())

    else:
        st.warning("⚠️ Clique sur le bouton ci-dessus pour démarrer le scraping.")

# === 3. Exploration des données ===
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

# === 4. VISUALISATION SIMPLE ===
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

# === 5. VISUALISATION TEXTUELLE ===
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
