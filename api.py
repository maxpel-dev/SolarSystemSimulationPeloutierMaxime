import json
import requests

# [!] Lancez plutôt main.py pour démarrer la simulation !
# Voir https://api.le-systeme-solaire.net/swagger/ pour les modèles de données reçues

#Utilisé pour les planètes et le soleil
def GetCelestialBodyDataFromId(id):
    api_url = 'https://api.le-systeme-solaire.net/rest.php/bodies/{}'.format(id)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print(response.json()["name"] + " chargé(e)")
    else:
        print("Error:", response.status_code, response.text)
    return response.json()

# 
def GetCelestialBodyDataFromUrl(url):
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        print(response.json()["name"] + " chargé(e)")
    else:
        print("Error:", response.status_code, response.text)
    return response.json()

# Seulement du code de test à partir de ce commentaire
response = GetCelestialBodyDataFromId("Mars")
print(json.dumps(response, indent=2))
moons = response["moons"]
print(json.dumps(moons, indent=2))
firstMoonUrl = moons[0]["rel"]
moonData = GetCelestialBodyDataFromUrl(firstMoonUrl)
print(json.dumps(moonData, indent=2))
