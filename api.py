import json
import requests
import urllib3

# Distance du soleil : "semimajorAxis"
# Rayon : "meanRadius"
# Jours par orbite = "sideralOrbit"
# Jours par rotation sur elle-même = "sideralRotation"

API_KEY = "etrZR7MXfRfCcjthCdlFnmeRAZBXfzzbrckyE8ad"

def GetCelestailBodyData(name):
    api_url = 'https://api.le-systeme-solaire.net/rest.php/bodies/{}'.format(name)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        #print(response.text)
        print(name + " chargé(e)")
    else:
        print("Error:", response.status_code, response.text)
    return response.json()

response = GetCelestailBodyData("Mercury")

print(json.dumps(response, indent=2))


