import json
import requests

# [!] Lancez plutôt main.py pour démarrer la simulation !
# Voir https://api.le-systeme-solaire.net/swagger/ pour les modèles de données reçues
BASE_URL = "https://api.le-systeme-solaire.net/rest.php/bodies/"

def GetCelestialBodyDataFromId(id):
    """
    Récupère un json renvoyé par l'API à partir de l'ID du corps céleste (Soleil, Planète ou Satellite) passé en paramètre.
    """
    api_url = BASE_URL + id
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print(response.json()["name"] + " chargé(e)")
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None