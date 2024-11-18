import os 
import gspread
from datetime import datetime
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
import base64
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Charger les informations d'identification depuis la variable d'environnement
encoded_json_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

# Vérifier si les identifiants sont présents
if not encoded_json_credentials:
    st.error("Les informations d'identification Google Sheets sont manquantes dans les variables d'environnement.")
    raise Exception("Google Sheets credentials missing.")

# Correction du padding Base64 (si nécessaire)
padding = len(encoded_json_credentials) % 4
if padding != 0:
    encoded_json_credentials += "=" * (4 - padding)

try:
    # Décoder la chaîne base64 pour obtenir le fichier JSON
    decoded_json = base64.b64decode(encoded_json_credentials)
    credentials_dict = json.loads(decoded_json)
except Exception as e:
    st.error(f"Erreur lors du décodage des informations d'identification : {e}")
    raise

# Définir les étendues (scopes) nécessaires pour accéder aux Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Charger les informations d'identification à partir du dictionnaire
credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)

# Créer le service API Google Sheets
service = build('sheets', 'v4', credentials=credentials)

# Charger l'ID de la feuille Google Sheets depuis la variable d'environnement
spreadsheet_id = os.environ.get("SPREADSHEET_ID")

if not spreadsheet_id:
    st.error("L'ID de la feuille Google Sheets est manquant dans les variables d'environnement.")
    raise Exception("Spreadsheet ID is missing.")
    
# Nom de la feuille dans le fichier Google Sheets
sheet_name = "message_de_suivis_devis"  # Nom exact de votre feuille

def enregistrer_dans_sheets(genre, nom_client, email_destinataire, modele_selectionne, courtier_nom, motif_resiliation, formule, montant_mensuel, compagnie):
    try:
        # Déterminer la date et l'heure actuelles
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Préparer les données à enregistrer
        donnees = [
            date_heure,                  # Colonne A
            genre,                       # Colonne B
            nom_client,                  # Colonne C
            email_destinataire,          # Colonne D
            modele_selectionne,          # Colonne E
            courtier_nom or "",          # Colonne F
            motif_resiliation or "",     # Colonne G
            formule or "",               # Colonne H
            montant_mensuel or "",       # Colonne I
            compagnie or ""              # Colonne J
        ]

        # Définir le corps de la requête
        body = {
            "values": [donnees]  # Les données doivent être sous forme de liste de listes
        }

        # Ajouter les données dans la feuille avec la méthode `values().append`
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",   # Plage cible (elle commence à A1, mais s'ajustera automatiquement)
            valueInputOption="USER_ENTERED",  # Les valeurs seront interprétées comme si elles étaient saisies manuellement
            body=body
        ).execute()

        # Retourner un message de confirmation
        return f"Les données ont été enregistrées avec succès dans la feuille '{sheet_name}'."
    
    except Exception as e:
        # Retourner une erreur détaillée
        return f"Erreur lors de l'enregistrement dans Google Sheets : {e}"



# Dictionnaire des courtiers avec leurs emails, mots de passe d'application et signatures
courtiers = {
    "Frédéric KEITA": {
        "email": os.environ.get("FREDERIC_EMAIL"),
        "mot_de_passe": os.environ.get("FREDERIC_PASSWORD"),
        "signature": """
        <br><br>-- <br>
        Frédéric KEITA, Conseiller Expert en Auto, Moto & Habitation<br>
        PREVO CONSEIL ASSURANCES<br>
        9 ALL Georges Bizet 95870 Bezons FRANCE<br>
        Ligne directe : 01.89.70.85.28   WhatsApp : 07.45.88.52.25<br>
        E-Mail : <a href="mailto:f.keita@assuconseils.fr">f.keita@assuconseils.fr</a><br>
        SITE-WEB : <a href="https://prevo-conseilassurance.com/">/SITE-WEB(PREVO-CONSEIL@ASSURANCES)</a><br>
        SIRET 98416391500015 - N° d'inscription ORIAS : 24004564 – site web ORIAS : <a href="https://www.orias.fr/">orias.fr</a><br>
        """
    },
    "Iness PEREZ": {
        "email": os.environ.get("INESS_EMAIL"),
        "mot_de_passe": os.environ.get("INESS_PASSWORD"),
        "signature": """
        <br><br>-- <br>
        Iness PEREZ, Conseillère Experte en Auto, Moto & Habitation<br>
        PREVO CONSEIL ASSURANCES<br>
        9 ALL Georges Bizet 95870 Bezons FRANCE<br>
        Ligne directe : 05.54.54.05.78   WhatsApp : 07.45.88.52.25<br>
        E-Mail : <a href="mailto:i.perez@assuconseils.fr">i.perez@assuconseils.fr</a><br>
        SITE-WEB : <a href="https://prevo-conseilassurance.com/">/SITE-WEB(PREVO-CONSEIL@ASSURANCES)</a><br>
        SIRET 98416391500015 - N° d'inscription ORIAS : 24004564 – site web ORIAS : <a href="https://www.orias.fr/">orias.fr</a><br>
        """
    },
    "Jean-Claude ALLAIN": {
        "email": os.environ.get("JEAN_EMAIL"),
        "mot_de_passe": os.environ.get("JEAN_PASSWORD"),
        "signature": """
        <br><br>-- <br>
        Jean-Claude ALLAIN, Conseiller Expert en Auto, Moto & Habitation<br>
        PREVO CONSEIL ASSURANCES<br>
        9 ALL Georges Bizet 95870 Bezons FRANCE<br>
        Ligne directe : 05.54.54.64.93   WhatsApp : 07.45.88.52.25<br>
        E-Mail : <a href="mailto:jc.allain@assuconseils.fr">jc.allain@assuconseils.fr</a><br>
        SITE-WEB : <a href="https://prevo-conseilassurance.com/">/SITE-WEB(PREVO-CONSEIL@ASSURANCES)</a><br>
        SIRET 98416391500015 - N° d'inscription ORIAS : 24004564 – site web ORIAS : <a href="https://www.orias.fr/">orias.fr</a><br>
        """
    }
}

# Configuration de l'expéditeur
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# Modèles de messages
modeles_messages = {
    "Envoi de devis": """
    <p>Bonjour {{genre}} {{nom_client}},</p>

    <p>Veuillez trouver ci-joint le devis pour l'assurance de votre véhicule, comme convenu lors de notre conversation téléphonique.</p>

    <p>Voici un récapitulatif des éléments discutés :</p>

    <ul>
        <li>Formule choisie : <strong>{{formule}}</strong>.</li>
        <li>Tarif mensuel : <strong>{{montant_mensuel}} €</strong></li>
    </ul>

    <p>Le devis détaillé est inclus en pièce jointe. Celui-ci comprend les informations sur la couverture proposée, les garanties incluses et les éventuelles options supplémentaires.</p>

    <p>N'hésitez pas à prendre le temps de le consulter attentivement et à me contacter si vous avez des questions ou des préoccupations. Je suis à votre disposition pour vous fournir toute information complémentaire.</p>

    <p>Je vous remercie pour votre confiance.</p>

    <p>Bien sincèrement,</p>
    <p>{{ signature_courtier }}</p>

    """,
    "Envoi de carte verte": """
    <p>Bonjour {{genre}} {{nom_client}},</p>

<p>C'est avec un grand plaisir que je vous annonce l'envoi de votre Carte Verte d'Assurance pour votre véhicule.</p>

<p>Cette carte verte atteste de votre couverture complète au sein de notre cabinet d'assurance et deviendra votre compagnon de confiance lors de vos trajets.</p>

<p>En plus de votre carte verte en annexe, j'ai le plaisir de vous remettre votre carte de prestations d'assistance, soigneusement élaborée pour vous garantir une tranquillité d'esprit tout au long de vos déplacements.</p>

<p>Ces avantages exclusifs sont conçus pour vous accompagner dans toutes les situations. N'hésitez pas à la consulter pour découvrir en détail comment nous pouvons vous assister.</p>

<p>Si vous avez des questions ou souhaitez obtenir des informations supplémentaires, je vous invite à me contacter.</p>

<p>Je reste à votre entière disposition pour vous apporter toute l'assistance nécessaire et vous remercie vivement pour votre confiance.</p>

<p>En vous souhaitant une conduite sûre et agréable, avec la sérénité que procure cette couverture complète.</p>

<p>Bien sincèrement,</p>
<p>{{ signature_courtier }}</p>

    """,
    "Message de suivi de devis": """
    <p>Bonjour {{ genre }} {{ nom_client }},</p>
    <p>Nous souhaitons faire un point sur votre demande de devis pour l'assurance de votre véhicule.</p>

    <!-- Personnalisation du message en fonction du motif de résiliation -->
    {% if motif_resiliation == "Non-paiement des cotisations" %}
    <p>Nous avons constaté l'interruption de votre contrat d'assurance, qui peut être liée à un défaut de paiement de vos cotisations, ou à une augmentation de votre cotisation auprès de votre précédente compagnie d'assurance. Nous comprenons que des difficultés financières peuvent survenir, et nous souhaitons vous apporter toute l'aide nécessaire pour régulariser votre situation.</p>
    <p>Nous proposons des solutions personnalisées et adaptées à vos besoins actuels, y compris des alternatives compétitives pour vous permettre de rétablir votre couverture d'assurance, même après une interruption liée à un non-paiement ou à une hausse des cotisations.</p>
    <p>Si vous avez rencontré une augmentation de votre cotisation auprès de votre précédent assureur, nous avons des options plus abordables qui répondront à vos besoins tout en vous offrant une protection complète.</p>
    <p>Pour toute question ou pour discuter des options qui s'offrent à vous, n'hésitez pas à nous contacter. Nous sommes là pour vous accompagner et vous aider à trouver la meilleure solution pour vos besoins.</p>
    <p>Nous vous remercions pour la confiance que vous nous accordez et restons à votre disposition pour toute information complémentaire.</p>
    
    {% elif motif_resiliation == "Fréquences de sinistres" %}
    <p>Nous avons bien pris en compte votre situation liée aux sinistres fréquents. Nous comprenons que cela puisse affecter votre couverture actuelle.</p>
    <p>Nous proposons des solutions adaptées pour vous offrir une assurance sur-mesure, même après plusieurs incidents. Nos garanties spécifiques sont conçues pour vous permettre de reprendre la route en toute sérénité, avec une couverture alignée à vos besoins.</p>
    <p>Contactez-nous pour découvrir nos options et trouver la meilleure couverture pour votre véhicule.</p>
    

    {% elif motif_resiliation == "Fausses déclarations" %}
    <p>Il semble que votre assurance ait été interrompue en raison de l'absence ou du retard dans l'envoi de certains documents justificatifs. Cela a pu entraîner un malentendu sur votre couverture et votre situation.</p>
    <p>Nous souhaitons vous aider à régulariser votre dossier en clarifiant vos besoins actuels. Nous vous proposons une solution sur mesure, transparente et parfaitement adaptée à votre profil.</p>
    <p>Nous restons à votre disposition pour recevoir les documents manquants et réévaluer votre couverture, afin de vous garantir une protection complète et conforme.</p>

    {% elif motif_resiliation == "Suspension de permis" %}
    <p>Suite à la suspension de votre permis, nous proposons des options qui tiennent compte de votre historique et vous offrent une couverture adéquate.</p>

    {% elif motif_resiliation == "Annulation de permis" %}
    <p>Après une annulation de permis, nous comprenons que vous souhaitez repartir sur de nouvelles bases. Nous disposons de solutions d’assurance adaptées à votre profil.</p>
    {% endif %}

    <p>Veuillez nous contacter pour compléter les informations nécessaires. Je vous remercie pour votre confiance.</p>
    <p>Bien cordialement,</p>
    <p>{{ signature_courtier }}</p>
    """,
    "Message de demande de documents": """
    <p>Bonjour {{genre}} {{nom_client}},</p>
    <p>Nous faisons suite à votre récente demande de devis d'assurance effectuée sur le site comparateur en ligne, et nous vous remercions de l'intérêt que vous portez à notre cabinet.</p>

<p>Nous avons entrepris des démarches pour vous contacter par téléphone afin de discuter de votre demande et de vous fournir les informations nécessaires pour une assurance parfaitement adaptée à vos besoins.</p>

<p>Afin de progresser dans le processus, nous avons besoin des éléments suivants :</p>

<ul>
    <li>Copie recto verso de votre permis de conduire.</li>
    <li>Copie recto verso de la carte grise de votre véhicule.</li>
    <li>Relevé d'informations.</li>
    <li>Pièce d'identité recto-verso.</li>
    <li>Le cas échéant, une copie de tout jugement ou infraction en rapport avec la conduite.</li>
</ul>

<p>Nous comprenons que votre temps est précieux, mais nous vous serions reconnaissants de bien vouloir nous transmettre ces documents dès que possible afin que nous puissions avancer dans le processus et répondre à vos besoins en matière d'assurance automobile.</p>

<p>Si vous avez des questions ou des préoccupations, n'hésitez pas à me contacter par e-mail ou par téléphone.</p>

<p>Je vous remercie pour votre attention et votre coopération.</p>

<p>Bien sincèrement,</p>
<p>{{ signature_courtier }}</p>

    """,
    "Message de rappel d'injoignabilité": """
 <p>Bonjour {{genre}} {{nom_client}},</p>

<p>Je me permets de vous contacter au sujet de votre demande de devis pour l'assurance de votre véhicule.</p>

<p>À ce jour, nous avons tenté à plusieurs reprises de vous contacter par téléphone pour discuter des détails de votre assurance automobile, mais malheureusement, nous n'avons pas réussi à vous joindre.</p>

<p>Il est essentiel que nous puissions communiquer avec vous afin de finaliser votre demande de devis et de vous offrir la meilleure solution d'assurance possible. Sans ces informations, nous sommes dans l'incapacité de procéder et cela pourrait entraîner des retards dans la mise en place de votre assurance.</p>

<p>Afin de progresser dans le processus, nous avons besoin des éléments suivants :</p>

<ul>
    <li>Copie recto verso de votre permis de conduire.</li>
    <li>Copie recto verso de la carte grise de votre véhicule.</li>
    <li>Relevé d'informations.</li>
    <li>Le cas échéant, une copie de tout jugement ou infraction en rapport avec la conduite.</li>
</ul>

<p>Nous comprenons que votre temps est précieux, mais nous vous serions reconnaissants de bien vouloir nous transmettre ces documents dès que possible afin que nous puissions avancer dans le processus et répondre à vos besoins en matière d'assurance automobile.</p>

<p>Si vous avez des questions ou des préoccupations, n'hésitez pas à me contacter par e-mail ou par téléphone.</p>

<p>Je vous remercie pour votre attention et votre coopération.</p>

<p>Cordialement,</p>
<p>{{ signature_courtier }}</p>
    """
}





# Fonction pour envoyer l'email avec pièces jointes
def envoyer_email(destinataire, sujet, message, courtier, fichier_joint=None, nom_fichier_joint=""):
    try:
        

        serveur = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        serveur.starttls()
        serveur.login(courtier["email"], courtier["mot_de_passe"])

        email = MIMEMultipart()
        email["From"] = courtier["email"]
        email["To"] = destinataire
        email["Subject"] = sujet
        email.attach(MIMEText(message, "html"))

        # Ajout du fichier joint si disponible
        if fichier_joint:
            piece_jointe = MIMEBase("application", "octet-stream")
            piece_jointe.set_payload(fichier_joint.read())
            encoders.encode_base64(piece_jointe)
            piece_jointe.add_header("Content-Disposition", f"attachment; filename={nom_fichier_joint}")
            email.attach(piece_jointe)

        serveur.sendmail(courtier["email"], destinataire, email.as_string())
        serveur.quit()
  
        return f"Email envoyé avec succès à {genre} {nom_client} par {courtier_nom}"


    except Exception as e:
        return f"Erreur lors de l'envoi de l'email: {e}"

# Interface Streamlit
st.title("Envoi d'email aux clients")

# Sélection du courtier
courtier_nom = st.selectbox("Sélectionnez le courtier", ["Frédéric KEITA", "Iness PEREZ", "Jean-Claude ALLAIN"])
courtier = courtiers[courtier_nom]

# Saisie du genre, du nom du client et de l'adresse email
genre = st.selectbox("Sélectionnez le genre du client", ("Monsieur", "Madame"))
nom_client = st.text_input("Nom du client")
email_destinataire = st.text_input("Adresse email du client")


# Sélection du modèle de message
modele_selectionne = st.selectbox("Sélectionnez le modèle de message", list(modeles_messages.keys()))
sujet = f"Votre demande d'assurance auto 🚗- {modele_selectionne}"

# Champs spécifiques pour certains modèles
fichier_joint = None
nom_fichier_joint = ""
message = ""
motif_resiliation = ""
formule=""
montant_mensuel=""
compagnie=""

# Personnalisation du message en fonction du modèle sélectionné
if modele_selectionne == "Envoi de devis":
    formule = st.selectbox("Sélectionnez la formule d'assurance", ["Formule Essentielle", "Formule Confort", "Formule Premium"])
    montant_mensuel = st.number_input("Montant mensuel (€)", min_value=0, step=1)
    compagnie = st.selectbox("Sélectionnez l'extranet du devis", ["maxance", "april", "zephir","ami 3f"])
    
    # Chargement du fichier obligatoire (acceptant plusieurs formats)
    fichier_joint = st.file_uploader("Déposez le fichier de devis (PDF, Image ou Capture d'écran)", type=["pdf", "jpg", "jpeg", "png"])
    
    # Vérification de la présence d'un fichier
    if fichier_joint is None:
        st.error("Veuillez télécharger un fichier de devis au format PDF ou image (jpg, jpeg, png) avant de procéder.")

    else:
        # Utilisation du nom d'origine du fichier téléchargé
        nom_fichier_joint = fichier_joint.name
        
        # Préparation du modèle de message
        message_template = modeles_messages[modele_selectionne]
        template = Template(message_template)
        
        # Génération du message
        message = template.render(
            genre=genre, 
            nom_client=nom_client, 
            formule=formule, 
            montant_mensuel=montant_mensuel,
            signature_courtier=courtier['signature']
        )

elif modele_selectionne == "Envoi de carte verte":
    fichier_joint = st.file_uploader("Déposez le fichier de carte verte", type=["pdf"])
    nom_fichier_joint = "Carte_Verte.pdf"
    message_template = modeles_messages[modele_selectionne]
    template = Template(message_template)
    message = template.render(
        genre=genre, 
        nom_client=nom_client,
        signature_courtier=courtier['signature']
    )

elif modele_selectionne == "Message de suivi de devis":
    motif_resiliation = st.selectbox("Motif de résiliation", [
        "Non-paiement des cotisations",
        "Fréquences de sinistres",
        "Fausses déclarations",
        "Suspension de permis",
        "Annulation de permis"
    ])
    message_template = modeles_messages[modele_selectionne]
    template = Template(message_template)
    message = template.render(
        genre=genre, 
        nom_client=nom_client, 
        motif_resiliation=motif_resiliation,
        signature_courtier=courtier['signature']
    )

else:
    message_template = modeles_messages[modele_selectionne]
    template = Template(message_template)
    message = template.render(
        genre=genre, 
        nom_client=nom_client,
        signature_courtier=courtier['signature']
    )

# Affichage du message personnalisé
st.markdown("**Message de suivi personnalisé :**")
st.write(message, unsafe_allow_html=True)


# Bouton pour envoyer l'email
if st.button("Envoyer l'email"):
    
    # Vérifier si toutes les informations nécessaires sont remplies
    if email_destinataire and nom_client and message:
        
        # Vérifier que le fichier a été téléchargé pour le modèle "Envoi de devis"
        if modele_selectionne == "Envoi de devis" and fichier_joint is None:
            st.error("Veuillez télécharger un fichier de devis au format PDF ou image (jpg, jpeg, png) avant de procéder.")
        else:
            try:
                # Enregistrer dans Google Sheets
                resulta_sheet = enregistrer_dans_sheets( 
                    genre, 
                    nom_client, 
                    email_destinataire, 
                    modele_selectionne, 
                    courtier_nom, 
                    motif_resiliation, 
                    formule, 
                    montant_mensuel, 
                    compagnie
                )
                st.success(resulta_sheet)  # Affiche un message de succès pour l'enregistrement dans Google Sheets
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement dans Google Sheets: {e}")  # Affiche l'erreur en cas de problème d'enregistrement

            try:
                # Obtenir le nom du fichier joint si disponible
                nom_fichier_joint = fichier_joint.name if fichier_joint else None

                # Envoyer l'email
                resultat_mail = envoyer_email(email_destinataire, sujet, message, courtier, fichier_joint, nom_fichier_joint)
                st.success(resultat_mail)  # Affiche un message de succès après l'envoi de l'email
            except Exception as e:
                st.error(f"Erreur lors de l'envoi de l'email: {e}")  # Affiche l'erreur en cas de problème d'envoi d'email
                
    else:
        st.error("Veuillez remplir tous les champs.")  # Message d'erreur si des champs sont manquants





def app():
    st.title("Tableau de bord principal")

    # Autres fonctionnalités de votre deuxième application
    st.write("Voici votre tableau de bord pour gérer vos données et fonctionnalités.")

    # Ajoutez ici votre bouton avec le lien stylé
    st.markdown(
        """
        <div style='text-align: center; margin-top: 20px;'>
            <a href="https://assurgestions-95ce048d8f69.herokuapp.com/" target="_blank" style="
                text-decoration: none; 
                background-color: #4CAF50; 
                color: white; 
                padding: 10px 20px; 
                font-size: 18px; 
                font-weight: bold; 
                border-radius: 8px; 
                display: inline-block;
                transition: all 0.3s ease;">
                🚀 Suivi des performances courtiers 🚀
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        """
        🌟 Cliquez sur le bouton ci-dessus pour accéder au tableau de suivi des performances des courtiers 
        en assurance auto. Visualisez et analysez facilement les données ! 🌟
        """
    )

if __name__ == "__main__":
    app()

