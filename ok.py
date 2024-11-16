import streamlit as st

# Afficher un message de bienvenue
st.write("Bonjour !")

# Demander à l'utilisateur son nom
nom = st.text_input("Quel est ton nom ?")

# Si l'utilisateur a saisi son nom, l'afficher
if nom:
    st.write(f"Bonjour {nom} !")



