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

"""
# Funcion que obten a lista e tamaño dos arquivos a descargar
def listaArquivos(latW, latE, latS, latN, inicio, fin, parametro):
    # Conexion a S5P Hub con credenciais de invitado
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Obtemos a lista de arquivos para unha rexion e datas especificas
    footprint = 'POLYGON((' + latW + ' ' + latS + ',' + latE + ' ' + latS + ',' + latE + ' ' + latN + ',' + latW + ' ' + latN + ',' + latW + ' ' + latS + '))'
    try:
        produtos = api.query(area=footprint, date=(inicio + 'T00:00:00Z', fin + 'T23:59:59Z'), producttype=parametro, processingmode='Offline')
    except:
        print('Error connectandose o servidor de s5phub. Execute o codigo de novo.')

    # Convertimos o resultado a dataframe para obter os nomes e tamaños dos arquivos
    produtosDF = api.to_dataframe(produtos)

    if len(produtosDF) > 0:
        nomes = produtosDF['filename'].tolist()
        tamanos = produtosDF['size'].tolist()
    else:
        nomes = []
        tamanos = []

    return nomes, tamanos, produtos


# Funcion que descarga os produtos indicados en produtos e os garda en directorio
def descargaArquivos(produtos, directorio):
    # Conexion a S5P Hub con credenciais de invitado
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Descargamos os arquivos
    try:
        api.download_all(produtos, directorio)
    except KeyboardInterrupt:
        print('\nO usuario interrompeu a descarga.')


# Funcion que imprime os arquivos a descargar
def obtenArquivos(latW, latE, latS, latN, inicio, fin, parametro, directorio):
    # Obtemos a lista de arquivos a descargar
    listaNomes, listaTamanos, produtos = listaArquivos(latW, latE, latS, latN, inicio, fin, parametro, 'Offline')

    # Imprimimos os nomes e tamaños dos arquivos
    if len(listaNomes) > 0:
        print('\nDescargaranse os seguintes ' + str(len(listaNomes)) + ' arquivos no directorio: ', directorio)
        for arq, tam in zip(listaNomes, listaTamanos):
            print(arq, ' (', tam, ')', sep='')

        # Descargamos os arquivos
        #descargaArquivos(produtos, directorio)
    else:
        print('\nNon se obtivo ningun arquivo. Por favor, intenteo de novo.')
"""

from creds import *

def obtenArquivos(latW, latE, latS, latN, inicio, fin, parametro, directorioDescarga):
    # set your area of interest
    latN = str(44.454713)
    latS = str(35.553679)
    latW = str(-9.492118)
    latE = str(4.419918)
    aoi= 'POLYGON((-9.492118 44.454713,4.419918 42.6636,5.112055 37.148517,-10.166057 35.371313,-9.492118 44.454713))'

    # make the request
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((12.655118166047592 47.44667197521409,21.39065656328509 48.347694733853245,28.334291357162826 41.877123516783655,17.47086198383573 40.35854475076158,12.655118166047592 47.44667197521409))') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T00:00:00.000Z").json()
    df = pd.DataFrame.from_dict(jsonf['value'])
    print(df)

    keycloak_token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')

    headers={"Authorization": f"Bearer {keycloak_token}"}

    session = requests.Session()
    session.headers.update(headers)

    download_dir = directorioDescarga

    for i in range(len(df)):
        pr = df.Id.values[i]
        url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({pr})/$value"
        response = session.get(url, headers=headers, stream=True)
        print(f"\nDescargando {df.Name.values[i][:-5]}.nc")
        with open(f"{download_dir}{df.Name.values[i][:-5]}.nc", 'wb') as p:
            p.write(response.content)