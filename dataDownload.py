from sentinelsat import SentinelAPI
from sentinel5dl import search, download
from datetime import date
import os, requests
import pandas as pd

def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token", data=data)
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Response from the server was: {r.json()}")
    return r.json()["access_token"]


def obtenArquivos(latW, latE, latS, latN, inicio, fin, parametro, directorioDescarga):
    # set your area of interest
    latN = str(44.454713)
    latS = str(35.553679)
    latW = str(-9.492118)
    latE = str(4.419918)
    aoi= "POLYGON((-9.492118 44.454713,4.419918 42.6636,5.112055 37.148517,-10.166057 35.371313,-9.492118 44.454713))"

    # make the request
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((12.655118166047592 47.44667197521409,21.39065656328509 48.347694733853245,28.334291357162826 41.877123516783655,17.47086198383573 40.35854475076158,12.655118166047592 47.44667197521409))') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T00:00:00.000Z").json()
    df = pd.DataFrame.from_dict(jsonf['value'])
    print(f"\nDescargaranse {len(df)} arquivos.")

    keycloak_token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')

    headers={"Authorization": f"Bearer {keycloak_token}"}

    session = requests.Session()
    session.headers.update(headers)

    download_dir = directorioDescarga

    for i in range(len(df)):
        pr = df.Id.values[i]
        prName = df.Name.values[i][:-5]

        url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({pr})/$value"
        response = session.get(url, allow_redirects=False)
        while response.status_code in (301, 302, 303, 307):
            url = response.headers['Location']
            response = session.get(url, allow_redirects=False)

        file = session.get(url, verify=False, allow_redirects=True)
        print("Descargando "+prName)
        with open(f"{download_dir}{prName}.zip", 'wb') as p:
            p.write(file.content)