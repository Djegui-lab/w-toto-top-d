import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Application Drag & Drop - Lecture de fichiers Excel 📂")

# Zone pour glisser-déposer le fichier
uploaded_file = st.file_uploader("Glissez-déposez un fichier Excel ici :", type=["xlsx", "xls"])

# Vérifier si un fichier a été téléchargé
if uploaded_file is not None:
    try:
        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(uploaded_file)

        # Afficher un aperçu des données
        st.write("Aperçu des données :")
        st.dataframe(df)

        # Bouton pour télécharger les données au format CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger en CSV",
            data=csv,
            file_name='export.csv',
            mime='text/csv',
        )
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez glisser-déposer un fichier Excel pour l'afficher.")
