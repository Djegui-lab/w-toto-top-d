import os

# Récupérer le chemin du fichier JSON à partir de l'environnement
json_file_path = os.getenv("GOOGLE_SHEETS_JSON_PATH")

if not json_file_path:
    raise FileNotFoundError("Le chemin de la variable d'environnement GOOGLE_SHEETS_JSON_PATH n'est pas défini.")
    
# Vérifiez si le fichier existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"Le fichier JSON est introuvable à l'emplacement : {json_file_path}")
else:
    print(f"Le fichier JSON a été trouvé à l'emplacement : {json_file_path}")
