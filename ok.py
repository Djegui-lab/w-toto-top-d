import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

import os

json_file_path = os.getenv("GOOGLE_SHEETS_JSON_PATH")
if not json_file_path or not os.path.exists(json_file_path):
    raise FileNotFoundError("Le fichier JSON est introuvable ou la variable d'environnement n'est pas définie.")

    
    # Portée de l'API Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
    
    # Autoriser l'accès via gspread
    client = gspread.authorize(creds)
    return client
# Lire les données de Google Sheets
def get_data_from_sheets(sheet_id, sheet_name):
    client = authenticate_google_sheets()
    
    # Ouvrir la feuille par son ID et son nom
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    
    # Obtenir toutes les données de la feuille
    data = sheet.get_all_records()
    
    # Convertir les données en DataFrame
    df = pd.DataFrame(data)
    return df

# Application Streamlit
def app():
    st.title("Application de Visualisation des Données Clients")

    # Demander l'ID de la feuille Google Sheets
    sheet_id = st.text_input("Entrez l'ID de votre Google Sheets:", "")

    # Demander le nom de la feuille dans le fichier Google Sheets
    sheet_name = st.text_input("Entrez le nom de la feuille (onglet) à afficher:", "Sheet1")

    if sheet_id and sheet_name:
        try:
            # Charger les données de la feuille Google Sheets
            df = get_data_from_sheets(sheet_id, sheet_name)
            st.write("Données de la feuille sélectionnée :", df)

            # Proposer une colonne pour filtrer les valeurs
            column_to_filter = st.selectbox("Choisissez la colonne pour filtrer les valeurs :", df.columns)

            # Sélectionner des valeurs spécifiques pour filtrer les données
            unique_values = df[column_to_filter].unique()
            selected_value = st.selectbox("Choisissez une valeur à afficher :", unique_values)

            # Afficher les données filtrées
            filtered_df = df[df[column_to_filter] == selected_value]
            st.write(f"Données filtrées par {column_to_filter} = {selected_value} :", filtered_df)
            
        except Exception as e:
            st.error(f"Erreur : {e}")

# Lancer l'application Streamlit
if __name__ == "__main__":
    app()



# streamlit run ok.py
# courtier-devis-automatique-e47e170f58f7.json