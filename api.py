import json
import requests

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


