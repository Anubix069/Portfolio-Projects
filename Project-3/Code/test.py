import streamlit as st
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

# ==== CONFIGURATION ====
st.set_page_config(page_title="Books to Scrape", layout="wide")
st.title("📚 Web Scraping en Live")

# ==== FONCTION DE SCRAPING ====
def run_scraping():
    start_time = time.time()

    # Installer automatiquement le bon driver
    chromedriver_autoinstaller.install()

    # Configurer Selenium pour travailler en mode headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Lancer Chrome avec Selenium
    driver = webdriver.Chrome(options=chrome_options)

    base_url = "https://books.toscrape.com/"
    driver.get(base_url)

    # Scraper la page avec BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category_links = soup.select("div.side_categories ul li ul li a")

    books = []
    for link in category_links:
        category_name = link.text.strip()
        category_url = link['href']
        driver.get(category_url)

        while True:
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            book_items = page_soup.select("article.product_pod")

            for book in book_items:
                title = book.h3.a["title"]
                price = book.select_one("p.price_color").text[1:]
                rating_class = book.select_one("p.star-rating")["class"][1]
                detail_url = base_url + book.h3.a["href"]
                image_url = base_url + book.find('img')['src']

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
                next_url = base_url + next_button['href']
                driver.get(next_url)
            else:
                break

    driver.quit()
    df = pd.DataFrame(books)
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

# === 2. WEB SCRAPING ===
if choix == "🔄 Web Scraping":
    st.subheader("📥 Lancer le scraping")
    if st.button("🛠️ Scraper les livres"):
        df, duration = run_scraping()
        st.success(f"{len(df)} livres récupérés en {duration:.2f} secondes.")
        st.dataframe(df.head())

    else:
        st.warning("⚠️ Clique sur le bouton ci-dessus pour démarrer le scraping.")
