import streamlit as st
import pandas as pd

# Application Streamlit
def app():
    st.title("Application de Visualisation des Données Clients")

    # Demander à l'utilisateur de télécharger un fichier CSV ou Excel
    uploaded_file = st.file_uploader("Téléchargez votre fichier (CSV ou Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            # Détecter le type de fichier téléchargé (CSV ou Excel)
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)

            st.write("Données du fichier téléchargé :", df)

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

