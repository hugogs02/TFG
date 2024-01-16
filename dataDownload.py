import os, requests, hashlib, glob, zipfile
import pandas as pd

def get_keycloak(username, password):
    """
    Esta funcion devolve un token de autenticacion para acceder ao Dataspace Ecosystem de Copernicus
    :param username: O nome de usuario
    :param password: A contrasinal do usuario
    :return: Token de autenticacion
    """
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
            f"Erro ao crear o Keycloak token. A resposta do servidor foi: {r.json()}")

    return r.json()["access_token"]


def descargaArquivo(id, nome, directorio, token):
    headers = {"Authorization": f"Bearer {token}"}
    session = requests.Session()
    session.headers.update(headers)

    if not os.path.isfile(f"{directorio}{nome}.zip"):
        url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({id})/$value"
        response = session.get(url, headers=headers, allow_redirects=False)
        while response.status_code in (301, 302, 303, 307):
            url = response.headers['Location']
            response = session.get(url, allow_redirects=False)

        if response.status_code in (200, 308):
            file = session.get(url, headers=headers, verify=True, allow_redirects=True)
            with open(f"{directorio}{nome}.zip", 'wb') as f:
                f.write(file.content)
                f.close()
        else:
            print(f"Erro na descarga. Código de resposta do servidor: {str(response.status_code)}")


def descomprimeArquivo(directorio, nome):
    if os.path.exists(f"{directorio}{nome}.zip"):
        try:
            with zipfile.ZipFile(f"{directorio}{nome}.zip") as arquivo:
                arquivo.extractall(directorio)

            os.remove(f"{directorio}{nome}.zip")

        except zipfile.BadZipFile:
            print(f"O arquivo zip {nome} e invalido. Procederase a sua eliminacion.")
            os.remove(f"{directorio}{nome}.zip")
    else:
        print(f"O arquivo {nome} non existe no directorio {directorio}.")


def obtenArquivos(aoi, inicio, fin, parametro, directorioDescarga):
    if not os.path.exists(directorioDescarga):
        os.mkdir(directorioDescarga)
    # make the request
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T00:00:00.000Z&$top=100").json()
    df = pd.DataFrame.from_dict(jsonf['value'])

    print(f"\nDescargaranse {len(df)} arquivos.")

    for i in range(len(df)):
        prId = df.Id.values[i]
        prName = df.Name.values[i][:-5]

        print("Descargando "+prName+" ("+prId+")")

        token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')

        descargaArquivo(prId, prName, directorioDescarga, token)

        descomprimeArquivo(directorioDescarga, prName)