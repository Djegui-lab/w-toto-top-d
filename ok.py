import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Fonction pour charger les données depuis Google Sheets
def load_data(sheet_name="Sheet1"):
    try:
        # Définissez les autorisations et l'accès au fichier JSON de clé d'API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("test-wague-9a205da3c6ca.json", scope)

        # Authentification avec les informations d'identification
        gc = gspread.authorize(credentials)

        # Ouvrir la feuille de calcul par son nom ou URL
        worksheet = gc.open(sheet_name).sheet1

        # Lire les données de la feuille de calcul
        data = worksheet.get_all_values()

        # Convertir les données en un DataFrame pandas
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None


# Application principale Streamlit
st.title("Application web pour l'analyse de données (en temps réel)")

# Entrée pour sélectionner le nom de la feuille Google Sheets
sheet_name = st.text_input("Entrez le nom de la feuille Google Sheets :", "message_de_suivis_devis")

# Charger et afficher les données si le nom de la feuille est fourni
if sheet_name:
    data = load_data(sheet_name)

    if data is not None:
        st.write("Données chargées avec succès !")

        # Afficher les données dans une table interactive
        st.dataframe(data)

        # Sélectionner une colonne à filtrer
        if not data.empty:
            column_to_filter = st.selectbox("Choisissez une colonne pour filtrer :", data.columns)

            # Afficher les valeurs uniques de la colonne et permettre de filtrer
            unique_values = data[column_to_filter].unique()
            selected_value = st.selectbox("Choisissez une valeur à afficher :", unique_values)

            # Filtrer les données et afficher les résultats
            filtered_data = data[data[column_to_filter] == selected_value]
            st.write(f"Données filtrées par {column_to_filter} = {selected_value} :", filtered_data)

# Auteur
st.write("AUTEUR : DJEGUI-WAUE")


