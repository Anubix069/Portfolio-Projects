# 🩻 Projet Tuberculosis X-ray Dataset 🫁

## 📌 Description
This project demonstrates the use of Structured Query Language (SQL) to explore and analyze a synthetic medical dataset containing 20,000 chest X-ray records labeled as either Normal or Tuberculosis. The dataset simulates real-world clinical data, helping evaluate potential risk factors, symptoms, and patterns associated with tuberculosis.

Through a series of analytical SQL queries, we explore demographic distributions, symptom severity, historical health records, and lifestyle factors (e.g., smoking), drawing insights that could assist in the early detection and classification of tuberculosis cases.

*🔗 Original source:* https://www.kaggle.com/datasets/miadul/tuberculosis-x-ray-dataset-synthetic/data

*📂 Raw data:* https://github.com/Anubix069/Portfolio-Projects/blob/main/sql/projects/project-01/raw_data/tuberculosis_xray_dataset.csv

*📚 File in usable format for SQL analysis:* https://github.com/Anubix069/Portfolio-Projects/blob/main/sql/projects/project-01/raw_data/tuberculosis_xray.db


## 🔍 Key Insights from the Analysis
 - **Total patients analysed** : 20,000
 - **Class distribution**: 70% Normal, 30% Tuberculosis
 - **Gender distribution** shows similar TB rates among males and females
 - **Average age** is roughly the same for both diagnostic groups (~53 years)
 - **High breathlessness and cough severity** are more prevalent in TB cases
 - **Smoking history and TB** show slightly higher ratios for former and current smokers
 - **Previous TB history** increases likelihood of a new TB diagnosis
 - **Fatigue levels** don't significantly differ between the two classes, but minor trends are observed
 - **Presence of blood in sputum** is a strong TB indicator (affecting nearly half the patients)

## 📊 Tuberculosis Data Exploration
  - Script for db creation : 
https://github.com/Anubix069/Portfolio-Projects/blob/main/sql/projects/project-01/processed_data/DB%20creation%20for%20SQL.py
  - Script for Data Analysis :
https://github.com/Anubix069/Portfolio-Projects/blob/main/sql/projects/project-01/processed_data/Script.sql

## 🛠️ Technologies Used
  - **SQL**
  - **DB Browser for SQLite** *for local database management*
  - **Pandas + SQLAlchemy (Python)** *for loading and transforming CSV into SQLite*

## 💡 Skills Demonstrated
  - Wrinting **SQL queries** *involving grouping, filtering, aggregation and conditional logic*
  - Performing **correlation-like investigations** using SQL constructs
  - Translating **medical dataset attributes into actionable insights**
  - Structuring an **end-to-end data analysis workflow**, from raw data ingestion to result synthesis



