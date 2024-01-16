import zipfile
from datetime import date
import os, requests, hashlib
import pandas as pd

def get_keycloak(username, password):
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        "refresh_token": "refresh_token",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token", data=data)
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Response from the server was: {r.json()}")
    return r.json()["access_token"], r.json()["refresh_token"]

def obtenArquivos(aoi, inicio, fin, parametro, directorioDescarga):
    # make the request
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T00:00:00.000Z&$top=100").json()
    df = pd.DataFrame.from_dict(jsonf['value'])

    print(f"\nDescargaranse {len(df)} arquivos.")

    keycloak_token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')
    headers = {"Authorization": f"Bearer {keycloak_token}"}

    session = requests.Session()
    session.headers.update(headers)

    download_dir = directorioDescarga
    if not os.path.exists(directorioDescarga):
        os.mkdir(directorioDescarga)

    for i in range(len(df)):
        pr = df.Id.values[i]
        prName = df.Name.values[i][:-5]

        print("Descargando "+prName+" ("+pr+")")
        if not os.path.isfile(f"{directorioDescarga}{prName}.zip"):
            url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({pr})/$value"
            response = session.get(url, headers=headers, allow_redirects=False)
            while response.status_code in (301, 302, 303, 307):
                url = response.headers['Location']
                response = session.get(url, allow_redirects=False)

            if response.status_code in (200, 308):
                file = session.get(url, headers=headers, verify=True, allow_redirects=True)
                with open(f"{directorioDescarga}{prName}.zip", 'wb') as f:
                    f.write(file.content)

            else:
                print("Unable to download. Response: " + str(response.status_code))
