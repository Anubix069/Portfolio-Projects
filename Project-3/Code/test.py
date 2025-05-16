import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL du site à scraper
url = 'https://books.toscrape.com/'

# Fonction de scraping
def scraper():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text[1:]  # Enlever le symbole de la devise
        rating = book.find('p', class_='star-rating')['class'][1]
        books.append({"title": title, "price": price, "rating": rating})
    
    # Convertir les données en DataFrame
    df = pd.DataFrame(books)
    return df

# Interface Streamlit
st.title("Scraping Live avec Streamlit")

# Bouton pour commencer le scraping
if st.button("Récupérer les données en direct"):
    with st.spinner("Récupération des données..."):
        # Scraper les données
        df = scraper()
        # Afficher les résultats
        st.write(df)
        # Option pour télécharger en CSV
        st.download_button(label="Télécharger les résultats", data=df.to_csv(), file_name='books_data.csv', mime='text/csv')
        
    # Pause pour simuler un délai de scraping
    time.sleep(2)
