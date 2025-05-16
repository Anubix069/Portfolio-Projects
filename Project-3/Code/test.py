import streamlit as st
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

# ==== CONFIGURATION GÉNÉRALE ====
st.set_page_config(page_title="Books to Scrape", layout="wide")
st.title("📚 Books to Scrape - Dashboard")

# === FONCTION DE SCRAPING (avec cache pour éviter relances) ===
@st.cache_data(show_spinner=True)
def run_scraping():
    start_time = time.time()

    options = Options()
    options.add_argument("--headless")  # Mode headless
    options.add_argument("--no-sandbox")  # Permet l'exécution dans un environnement sécurisé
    options.add_argument("--disable-dev-shm-usage")  # Pour les systèmes de fichiers limités
    options.add_argument("--log-level=3")
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2
    })
    
    # Sélection automatique de la bonne version de chromedriver
    chromedriver_autoinstaller.install()
    
    # Utilisation de WebDriverManager pour s'assurer que le bon driver est installé
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    base_url = "https://books.toscrape.com/"
    driver.get(base_url)

    # Code de scraping ici...
    
    driver.quit()
    return df, duration
