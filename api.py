import json
import requests

# [!] Lancez plutôt main.py pour démarrer la simulation !
# Voir https://api.le-systeme-solaire.net/swagger/ pour les modèles de données reçues

def GetCelestialBodyDataFromId(id):
    """"""
    api_url = 'https://api.le-systeme-solaire.net/rest.php/bodies/{}'.format(id)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print(response.json()["name"] + " chargé(e)")
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None