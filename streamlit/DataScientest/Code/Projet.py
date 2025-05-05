import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Bandeau avec le logo en haut de page
st.markdown(
    """
    <div style="background-color:#f9f9f9; padding:10px; display:flex; align-items:center; border-bottom:1px solid #ccc;">
        <img src="https://www.solutions-ressources-humaines.com/logo/f6aacfed8f0555dlogo-2021-1.png" alt="Logo" style="height:60px; margin-right:20px;">
        <h1 style="margin:0; font-size:24px; color:#333;">Projet Température Terrestre </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# Création de la barre latérale avec des options cliquables
# -----------------------------------------------------------

menu = st.sidebar.selectbox("Navigation", 
                            ["Introduction", 
                             "Exploration des données", 
                             "Data Visualisation", 
                             "Conclusion", 
                             "Sources"], key="menu_select")

# -----------------------------------------------------------
# Section Introduction
# -----------------------------------------------------------

if menu == "Introduction":

    # Participants du projet avec liens LinkedIn
    st.markdown(
        """
        <div style="padding:10px 0 20px 0;">
            <h4 style="margin-bottom:5px; color:#555;">Participants :</h4>
            <ul style="margin-top:0; padding-left:20px; color:#333;">
                <li><a href="https://www.linkedin.com/in/quentin-dusautoir-080abb1a2/" target="_blank" style="color:#1e5a77; text-decoration:none;">Quentin Dusautoir</a></li>
                <li><a href="https://www.linkedin.com/in/clementlabois" target="_blank" style="color:#1e5a77; text-decoration:none;">Clément Labois</a></li>
                <li><a href="https://www.linkedin.com/in/nizar-mensi-325433135/" target="_blank" style="color:#1e5a77; text-decoration:none;">Nizar Mensi</a></li>
                <li><a href="https://www.linkedin.com/in/jessicarenaudet/" target="_blank" style="color:#1e5a77; text-decoration:none;">Jessica Renaudet</a></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Introduction")

    st.markdown("""  
        Récemment, l'Agence de la transition écologique (ADEME) a révélé que 25 % des Français âgés de 15 à 64 ans se déclarent éco-anxieux. 
        Cette inquiétude face aux enjeux climatiques reflète une préoccupation croissante, non seulement concernant les impacts environnementaux, 
        mais aussi les conséquences sur la santé mentale des individus. Parmi ces personnes, 2,1 millions sont fortement éco-anxieux, et 2,1 millions 
        supplémentaires sont très fortement éco-anxieux, nécessitant parfois un suivi psychologique. Il est aussi noté que 420 000 personnes présentent un 
        risque sévère de développer des troubles psychopathologiques tels que la dépression ou l'anxiété généralisée ([ADEME](https://www.ademe.fr/)).

        En 2024, la planète a enregistré un nouveau record de chaleur, accentuant ainsi les craintes liées au réchauffement climatique. 
        Ce phénomène se manifeste par une augmentation progressive des températures moyennes mondiales, un sujet qui ne cesse d'être au cœur des préoccupations 
        sociétales. En effet, les événements météorologiques extrêmes tels que les vagues de chaleur, les sécheresses, les feux de forêt et les précipitations intenses 
        se multiplient et deviennent plus fréquents, affectant les écosystèmes et les communautés humaines [GIEC, 2024](https://www.ipcc.ch/report/ar6/wg1/); [OMM](https://public.wmo.int/en)).

        Le réchauffement climatique est un phénomène qui impacte de manière irréversible certains écosystèmes, fragilisant des espèces et menaçant la biodiversité. 
        Selon le sixième rapport d'évaluation du GIEC, les impacts sur les conditions météorologiques et les écosystèmes sont déjà généralisés. Cette montée en température 
        affecte aussi la répartition des espèces, qui se déplacent vers des zones plus fraîches, ce qui perturbe l'équilibre naturel de nombreuses régions ([GIEC](https://www.ipcc.ch/sr15/)).

        L'éco-anxiété grandissante témoigne d'une prise de conscience accrue des risques liés au réchauffement climatique, notamment en ce qui concerne ses effets sur notre 
        environnement et notre quotidien. Ainsi, il devient crucial de comprendre et d'analyser les données relatives à ces phénomènes climatiques pour prendre les bonnes décisions 
        et adapter nos politiques environnementales ([ADEME](https://www.ademe.fr/)).

        ## Objectifs de l'étude

        Dans le cadre de ce projet, nous nous concentrons sur l'analyse des températures mondiales à travers des données climatiques disponibles. Bien que nous ne soyons ni climatologues ni experts en la matière, notre objectif est de rendre ces données accessibles à tous, y compris ceux qui, comme nous, n’ont pas d’expérience préalable dans ce domaine. 
        Notre étude se base sur des données provenant de la NASA et de sources publiques sur les émissions de CO2, afin de mieux comprendre l'ampleur et l’évolution du réchauffement climatique.

        ## Méthodologie et approche

        Nous avons décidé d’explorer deux aspects principaux du réchauffement climatique :
        1. **L’évolution des températures mondiales** : en utilisant les données des anomalies de température de la NASA sur une période longue, depuis 1880 jusqu’à aujourd’hui.
        2. **Les émissions de CO2** : en analysant les émissions mondiales de CO2 et leur impact, avec une attention particulière portée sur les pays et régions qui émettent le plus de gaz à effet de serre.

        Les données utilisées proviennent de la NASA pour les anomalies de température et d'OWID pour les émissions de CO2, que nous avons fusionnées avec des informations géographiques supplémentaires. En explorant ces deux dimensions, nous cherchons à donner un aperçu de l'évolution du réchauffement climatique et de ses principales causes.

        ## Contexte scientifique

        Les scientifiques suivent l’évolution du réchauffement climatique grâce à une vaste quantité de données climatiques. Ces données sont essentielles pour observer l'augmentation des températures mondiales et pour comprendre les causes sous-jacentes de ce phénomène. La mesure des anomalies de température permet de suivre les tendances sur de longues périodes, tandis que l’analyse des émissions de CO2 permet de mettre en lumière l'impact des activités humaines sur le climat.

        En résumé, ce projet vise à sensibiliser un large public aux enjeux du réchauffement climatique, en présentant des données accessibles et compréhensibles, et à fournir des informations utiles pour mieux appréhender cette problématique cruciale.
    """)

# -----------------------------------------------------------
# Section Exploration des Données
# -----------------------------------------------------------

elif menu == "Exploration des données":
    st.subheader("Exploration des données")

    # Chargement des datasets
    nasa_df = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/GLB.Ts+dSST.csv", skiprows=1)
    df = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/owid-co2-data.csv")
    df2 = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/all.csv")

    # -----------------------------------------------------------
    # Renommer les colonnes pour les saisons
    # -----------------------------------------------------------
    nasa_df = nasa_df.rename(columns={
        'DJF': 'Winter',   # DJF (Décembre-Janvier-Février) devient Winter
        'MAM': 'Spring',   # MAM (Mars-Avril-Mai) devient Spring
        'JJA': 'Summer',   # JJA (Juin-Juillet-Août) devient Summer
        'SON': 'Autumn'    # SON (Septembre-Octobre-Novembre) devient Autumn
    })

    # Définir les saisons
    saisons = ['Winter', 'Spring', 'Summer', 'Autumn']

    # Convertir les valeurs des saisons en numériques, en gérant les valeurs manquantes
    nasa_df[saisons] = nasa_df[saisons].apply(pd.to_numeric, errors='coerce')

    # -----------------------------------------------------------
    # Sous-partie Dataset NASA
    # -----------------------------------------------------------
    st.subheader("Dataset NASA (Température Mondiale)")
    st.write("Le dataset de la NASA contient des anomalies de température mondiales depuis 1880.")
    st.write("**Aperçu des données**")
    st.write(nasa_df.head())  # Affichage des premières lignes du dataset NASA

    st.write("**Statistiques descriptives du Dataset**")
    st.write(nasa_df.describe())  # Statistiques descriptives

    # Calculer le pourcentage de valeurs manquantes par colonne
    missing_data = pd.DataFrame({
        "Colonne": nasa_df.columns,
        "Pourcentage de valeurs manquantes (%)": [
         nasa_df[column].isna().sum() / len(nasa_df) * 100 for column in nasa_df.columns
        ]
    })

    # Arrondir pour un affichage plus propre
    missing_data["Pourcentage de valeurs manquantes (%)"] = missing_data["Pourcentage de valeurs manquantes (%)"].round(2)

    # Affichage du tableau dans Streamlit
    st.write("**Pourcentage de valeurs manquantes**")
    st.dataframe(missing_data)

    # -----------------------------------------------------------
    # Sous-partie Dataset Our World in Data et all.csv
    # -----------------------------------------------------------
    st.subheader("Dataset Our World in Data & Emissions de CO2")
    st.write("Ce dataset contient notamment des données sur les émissions de CO2 mondiales ainsi que des informations géographiques.")
    st.write("**Aperçu des données**")
    st.write(df.head())  # Affichage des premières lignes du dataset CO2

    st.write("**Statistiques descriptives du Dataset**")
    st.write(df.describe())  # Statistiques descriptives

    # Calcul du pourcentage de valeurs manquantes pour chaque colonne
    missing_data_df = pd.DataFrame({
        "Colonne": df.columns,
        "Pourcentage de valeurs manquantes (%)": [
         df[column].isna().sum() / len(df) * 100 for column in df.columns
        ]
    })

    # Arrondir pour un affichage lisible
    missing_data_df["Pourcentage de valeurs manquantes (%)"] = missing_data_df["Pourcentage de valeurs manquantes (%)"].round(2)

    # Trier par ordre décroissant
    missing_data_df = missing_data_df.sort_values(by="Pourcentage de valeurs manquantes (%)", ascending=False)

    # Affichage dans Streamlit
    st.write("**Pourcentage de valeurs manquantes**")
    st.dataframe(missing_data_df)

    # -----------------------------------------------------------
    # Sous-partie all.csv
    # -----------------------------------------------------------
    st.subheader("Dataset all.csv (Codes ISO et autres informations géographiques)")
    st.write("Le dataset all.csv contient des informations géographiques supplémentaires, notamment les codes ISO des pays.")
    st.write("**Aperçu des données**")
    st.write(df2.head())  # Affichage des premières lignes du dataset all.csv

    st.write("**Statistiques descriptives du Dataset**")
    st.write(df2.describe())  # Statistiques descriptives

# -----------------------------------------------------------
# Section Data Visualisation
# -----------------------------------------------------------

elif menu == "Data Visualisation":

    # Fichiers de données à charger
    nasa_df = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/GLB.Ts+dSST.csv", skiprows=1)
    df = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/owid-co2-data.csv")
    df2 = pd.read_csv("C:/Users/cleme/OneDrive/Bureau/DataScientest/Projet/all.csv")

    # -----------------------------------------------------------
    # Filtrer les données à partir de 1880 
    # ----------------------------------------------------------
    df_filtered = df[df['year'] >= 1880]

    # -----------------------------------------------------------
    # Fusion avec le df2
    # ----------------------------------------------------------
    merged_df = pd.merge(df_filtered, df2, left_on='iso_code', right_on='alpha-3', how='inner')

    # -----------------------------------------------------------
    # Visualisation des anomalies saisonnières
    # -----------------------------------------------------------
    st.subheader("Visualisation de l'évolution des Anomalies Saisonnières")

    # Renommer les colonnes pour les saisons
    # -----------------------------------------------------------
    nasa_df = nasa_df.rename(columns={
        'DJF': 'Hiver',   # DJF (Décembre-Janvier-Février) devient Hiver
        'MAM': 'Printemps',  # MAM (Mars-Avril-Mai) devient Printemps
        'JJA': 'Ete',   # JJA (Juin-Juillet-Août) devient Ete
        'SON': 'Automne',   # SON (Septembre-Octobre-Novembre) devient Automne
    })

    # Définir la liste des colonnes saisonnières
    saisons = ['Hiver', 'Printemps', 'Ete', 'Automne']

    # Convertir les valeurs des saisons en numériques, en gérant les valeurs manquantes
    nasa_df[saisons] = nasa_df[saisons].apply(pd.to_numeric, errors='coerce')

    # Réorganiser les données en format "long" pour plotly
    df_long = nasa_df.melt(id_vars='Year', value_vars=saisons, var_name='Saison', value_name='Anomalie')

    # Palette de couleurs vives pour chaque saison
    couleurs_saisons = {
        'Hiver': '#1f77b4',      # bleu vif
        'Printemps': '#2ca02c',  # vert
        'Ete': '#ff7f0e',        # orange
        'Automne': '#d62728',    # rouge
    }

    # Créer le graphique dynamique
    fig_saisons = px.line(
        df_long,
        x='Year',
        y='Anomalie',
        color='Saison',
        color_discrete_map = couleurs_saisons,
        title="Évolution des anomalies saisonnières",
        labels={'Year': 'Année', 'Anomalie': 'Anomalie (°C)', 'Saison': 'Saison'},
        template='plotly_dark'
    )   

    # Afficher dans Streamlit
    st.plotly_chart(fig_saisons)
    st.write("Ce graphique illustre l’évolution des anomalies de température saisonnières à l’échelle mondiale entre 1880 et 2024, mettant en lumière les variations spécifiques à chaque saison au fil du temps.")
   
    # -----------------------------------------------------------
    # Visualisation des Anomalies de Température (NASA)
    # -----------------------------------------------------------
    st.subheader("Visualisation des Anomalies de Température")

    # Conversion explicite des valeurs de 'J-D' en numériques (float)
    nasa_df['J-D'] = pd.to_numeric(nasa_df['J-D'], errors='coerce')  # 'coerce' convertit en NaN les valeurs invalides

    # Graphique des anomalies de température avec code couleur
    fig_temp = go.Figure()

    fig_temp.add_trace(go.Scatter(
        x=nasa_df['Year'], 
        y=nasa_df['J-D'], 
        mode='markers+lines', 
        name='Anomalie Température',
        marker=dict(
            color=nasa_df['J-D'],
            colorscale='RdBu_r',
            colorbar=dict(title="Anomalie Température (°C)"),
            size=8
        )
    ))

    fig_temp.update_layout(
        title="Évolution des Anomalies de Température Mondiale",
        xaxis_title="Année",
        yaxis_title="Anomalie Température (°C)",
        template="plotly_dark",
        showlegend=True
    )

    st.plotly_chart(fig_temp)
    st.write("Les températures mondiales montrent une hausse nette depuis les années 1940, avec une accélération notable à partir des années 1980. Depuis 2018, on enregistre régulièrement des écarts records, dépassant les +1 °C, pour atteindre environ +1,29 °C en 2024.")

    # -----------------------------------------------------------
    # Visualisation des Années les Plus Chaudes
    # -----------------------------------------------------------
    st.subheader("Les Années les Plus Chaudes")

    # Analyse des années les plus chaudes
    top_years = nasa_df.sort_values(by='J-D', ascending=False).head(10)

    fig_hot_years = go.Figure()

    fig_hot_years.add_trace(go.Bar(
        x=top_years['Year'],
        y=top_years['J-D'],
        marker=dict(
            color=top_years['J-D'],
            colorscale='YlOrRd',  # Beige à rouge foncé
            colorbar=dict(title="Anomalie Température (°C)"),
        ),
        name="Années les Plus Chaudes"
    ))

    fig_hot_years.update_layout(
        title="Les Années les Plus Chaudes (Anomalie Température)",
        xaxis_title="Année",
        yaxis_title="Anomalie Température (°C)",
        template="plotly_dark",
        showlegend=True
    )

    st.plotly_chart(fig_hot_years)
    st.write("Le graphique suivant, présenté sous forme de diagramme en barres, vient consolider cette tendance : il montre que les dix années les plus chaudes jamais enregistrées correspondent précisément aux dix dernières, de 2015 à 2024.")

    # -----------------------------------------------------------
    # Graphique de la concentration de CO2 pour les pays et les années filtrées
    # -----------------------------------------------------------
    st.subheader("Visualisation de l'évolution des émissions de CO₂")
    yearly_emissions = merged_df.groupby('year')['co2_including_luc'].sum()

    # Création d'un figure présentant les émissions de CO₂ par continent et par année
    # Nettoyage des colonnes nécessaires
    df_clean = merged_df.dropna(subset=['region', 'year', 'country', 'co2_including_luc'])

    # Calcul des top 5 pays par région et par année
    top_emitters = (
        df_clean
        .sort_values(['region', 'year', 'co2_including_luc'], ascending=[True, True, False])
        .groupby(['region', 'year'])['country']
        .apply(lambda x: ', '.join(x.head(5)))
        .reset_index(name='top_countries')
    )

    # CO₂ par continent et année
    co2_by_continent = (
        df_clean
        .groupby(['region', 'year'])['co2_including_luc']
        .sum()
        .reset_index()
    )

    # Fusion des top pays dans le DataFrame
    co2_by_continent = co2_by_continent.merge(top_emitters, on=['region', 'year'], how='left')

    fig_continent = px.line(
        co2_by_continent,
        x='year',
        y='co2_including_luc',
        color='region',
        custom_data=['top_countries'],
        labels={
            'year': 'Année',
            'co2_including_luc': 'Émissions CO₂ (Gt)',
            'region': 'Continent'
        },
        title="Évolution des émissions de CO₂ par continent",
        template='plotly_dark'
    )

    # Hover enrichi avec les top 5 pays
    fig_continent.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "Année: %{x}<br>" +
            "Émissions: %{y:.2f} Gt<br>" +
            "Top 5 pays: %{customdata[0]}<extra></extra>"
        )
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig_continent)
    st.write("Ce graphique met en évidence une hausse globale des émissions de CO₂ dans le monde. Toutefois, cette tendance mérite d’être nuancée : l’Europe et les Amériques ont pris conscience de l’enjeu climatique et ont massivement investi dans les énergies renouvelables, moins émettrices de CO₂. En revanche, on observe une augmentation marquée des émissions en Asie, portée par une industrialisation rapide et une urbanisation accélérée, en particulier depuis le début des années 2000. Face à cette dynamique, nous avons choisi de recentrer notre analyse sur l’Asie à partir de l’an 2000, afin de mieux comprendre l’impact environnemental de ces transformations et les enjeux spécifiques à cette région du monde.")
    st.write("🔍 À noter : ce graphique dynamique met en avant les cinq pays les plus émetteurs de CO₂, permettant de visualiser clairement les évolutions et écarts entre eux au fil du temps.")

# -----------------------------------------------------------
# Section Conclusion
# -----------------------------------------------------------

elif menu == "Conclusion":
    st.subheader("Conclusion")
    st.markdown("""
    Ce modeste projet met en lumière l'évolution du réchauffement climatique à travers les anomalies de température et les émissions de CO2. Il est évident que le réchauffement climatique a un impact significatif sur la planète, et les émissions de CO2 restent un facteur clé dans ce phénomène. Depuis les années 80, une accélération de ces anomalies a été observée, en corrélation avec une hausse des émissions de CO2, surtout dans les pays en développement. Cependant, des efforts notables ont été réalisés dans certaines régions, notamment en Europe et aux États-Unis, pour favoriser la transition vers des énergies renouvelables et réduire l'empreinte carbone.

    La mise en place de politiques de réduction des émissions de gaz à effet de serre est essentielle pour freiner cette tendance et limiter les dégâts à long terme. Ces initiatives, bien que bénéfiques à long terme, n'ont pas encore montré de résultats immédiats. L'Asie, notamment, reste un défi majeur en raison de sa dépendance aux énergies fossiles, en particulier le charbon. Toutefois, la Chine et d'autres pays asiatiques ont fixé des objectifs ambitieux pour intégrer les énergies renouvelables et réduire les émissions de CO2.

    Les données que nous avons explorées fournissent une base solide pour comprendre les défis climatiques mondiaux, et il est crucial de continuer à surveiller les évolutions climatiques avec des données actualisées. Cette vigilance permettra non seulement d'ajuster les stratégies environnementales à l'échelle mondiale, mais aussi d'anticiper les impacts des changements climatiques sur les sociétés et les écosystèmes.

    """)

# -----------------------------------------------------------
# Section Sources
# -----------------------------------------------------------

elif menu == "Sources":
    st.subheader("Sources")
    st.markdown("""
        - **NASA Global Temperature Dataset** : https://data.giss.nasa.gov/gistemp/
        - **Our World in Data** : https://ourworldindata.org/co2-emissions
        - **Dataset des pays et régions**(https://ourworldindata.org/geography)
        - **Temperature change on land(FAOSTAT)**(https://www.fao.org/faostat/en/#data/ET/metadata)
        - **[Rapport du GIEC]**(https://www.ipcc.ch)
        - [**Télécharger le fichier Power BI**](https://drive.google.com/file/d/1vgJfv9_-daa6k4LvFgufUfYuhLUhpBif/view?usp=sharing)
    """)

    
