import zipfile
from datetime import date
import os, requests, hashlib
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

def checkmd5(filename):
    omd5=hashlib.md5(open(filename,'rb').read()).hexdigest()
    with open(filename,'rb') as f:
        nmd5=hashlib.md5(f.read()).hexdigest()

    return omd5==nmd5

def obtenArquivos(latW, latE, latS, latN, inicio, fin, parametro, directorioDescarga):
    # set your area of interest
    aoi= "POLYGON((12.655118166047592 47.44667197521409,21.39065656328509 48.347694733853245,28.334291357162826 41.877123516783655,17.47086198383573 40.35854475076158,12.655118166047592 47.44667197521409))"

    # make the request
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T00:00:00.000Z&$top=100").json()
    df = pd.DataFrame.from_dict(jsonf['value'])

    print(f"\nDescargaranse {len(df)} arquivos.")

    keycloak_token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')

    headers={"Authorization": f"Bearer {keycloak_token}"}

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
            response = session.get(url, allow_redirects=False)
            while response.status_code in (301, 302, 303, 307):
                url = response.headers['Location']
                response = session.get(url, allow_redirects=False)

            file = session.get(url, verify=False, allow_redirects=True)
            with open(f"{directorioDescarga}{prName}.zip", 'wb') as p:
                p.write(file.content)

            p.close()

