import os, requests, zipfile, shutil, glob
import pandas as pd

def get_keycloak(username, password):
    """
    Esta funcion devolve un token de autenticación para acceder ao Dataspace Ecosystem de Copernicus
    :param username: O nome de usuario
    :param password: A contrasinal do usuario
    :return: Token de autenticacion
    """
    # Definimos os datos cos que realizar a petición de autenticación
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        }
    # Obtemos o token
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token", data=data)
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Erro ao crear o Keycloak token. A resposta do servidor foi: {r.json()}")

    # Devolvemos o token
    return r.json()["access_token"]


def descargaArquivo(id, nome, directorio):
    """
    Esta función descarga o arquivo con nome "nome" e identificador "id" no directorio
    :param id: o id do arquivo a descargar
    :param nome: o nome do arquivo a descargar
    :param directorio: o directorio no que se descargará o arquivo
    """
    # Obtemos o token de autenticación
    token = get_keycloak('hugo.gomez.sabucedo@rai.usc.es', 'Hugotfg&2023')
    # Creamos un obxecto Session para realizar as peticións ó servidor
    session = requests.Session()
    # Actualizamos os headers do obxecto Session co token de autenticación
    headers = {"Authorization": f"Bearer {token}"}
    session.headers.update(headers)

    # Definimos a url dende a que descargaremos o arquivo, empregando para iso o identificador, e facemos un get par aobter o arquivo
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({id})/$value"
    response = session.get(url, headers=headers, allow_redirects=False)
    # Se o código de estado é 301 (Moved permanently), 302 (Found), 303(See Other) ou 307 (Temporary redirect),
    # volvemos facer a petición, cambiando a URL pola indicada no campo "Location" do header da resposta
    while response.status_code in (301, 302, 303, 307):
        url = response.headers['Location']
        response = session.get(url, allow_redirects=False)

    # Se o código de estado é 200 (OK) ou 308 (Permanent redirect), descargaremos directamente o arquivo; se non, mostramos o código de error
    if response.status_code in (200, 308):
        file = session.get(url, headers=headers, verify=True, allow_redirects=True)
        # Abrimos o arquivo en formato zip e modo write+binary, escribimos o seu contido e pechamos o arquivo
        with open(f"{directorio}{nome}.zip", 'wb') as f:
            f.write(file.content)
            f.close()
    else:
        print(f"Erro na descarga. Código de resposta do servidor: {str(response.status_code)}")


def descomprimeArquivo(directorio, nome):
    """
    Esta función descomprime o arquivo "nome" que se atopa na carpeta "directorio"
    :param directorio: directorio no que se atopa o arquivo a descomprimir
    :param nome: nome do arquivo a descomprimir
    """
    # Comprobamos que o arquivo existe; se non, imprimimos unha mensaxe de erro
    if os.path.exists(f"{directorio}{nome}.zip"):
        # Extramos o arquivo zip no directorio
        try:
            with zipfile.ZipFile(f"{directorio}{nome}.zip") as arquivo:
                arquivo.extractall(directorio)

            # Unha vez descomprimido, eliminamos o arquivo zip
            os.remove(f"{directorio}{nome}.zip")

        # Capturamos a excepción BadZipFile (para ver se o arquivo está corrupto), e eliminamos o arquivo
        except zipfile.BadZipFile:
            print(f"O arquivo zip {nome} e invalido. Procederase a sua eliminacion.")
            os.remove(f"{directorio}{nome}.zip")
    else:
        print(f"O arquivo {nome} non existe no directorio {directorio}.")


def obtenArquivos(aoi, inicio, fin, parametro, directorioDescarga):
    """
    Esta función busca no dataspace de COPERNICUS para obter os arquivos que corresponden co parametro "parametro", na área "aoi",
    entre a data "inicio" e "fin"; e executa a descarga a descompresión dos mesmos
    :param aoi: área de interese da busca, que debe ser de tipo POLYGON
    :param inicio: data de inicio da busca, en formato AAAA-MM-DD
    :param fin: data de fin da busca, en formato AAAA-MM-DD
    :param parametro: o parámetro para o que queremos facer a busca
    :param directorioDescarga: o diretorio onde se descargarán os arquivos
    """
    # Se non existe o directorio de descarga, creámolo
    if not os.path.exists(directorioDescarga):
        os.mkdir(directorioDescarga)

    # Facemos a petición ó servidor para obter os datos dos arquivos que coincidan cos criterios de busca, e convertímolos
    # nun dataframe de pandas para traballar máis facilmente con eles
    jsonf=requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and Collection/Name eq 'SENTINEL-5P' and contains(Name,'S5P_OFFL_{parametro}') and ContentDate/Start gt {inicio}T00:00:00.000Z and ContentDate/Start lt {fin}T23:59:59.000Z&$top=100").json()
    df = pd.DataFrame.from_dict(jsonf['value'])

    print(f"\nDescargaranse {len(df)} arquivos.")

    # Iteramos pola lista de arquivos para descargalos e transformalos
    for i in range(len(df)):
        # Obtemos o nome e identificador do arquivo
        prId = df.Id.values[i]
        prName = df.Name.values[i][:-5]

        print("Descargando "+prName+" ("+prId+")")

        # Se o arquivo non existe (ben sexa en formato zip ou extraído xa e en formato nc), descargámolo
        if not (os.path.isfile(f"{directorioDescarga}{prName}.zip") or len(glob.glob(f"{directorioDescarga}{prName}*.nc"))!=0):
            descargaArquivo(prId, prName, directorioDescarga)

        # Se existe o arquivo en formato zip (por non terse descomprimido), descomprimímolo
        if os.path.isfile(f"{directorioDescarga}{prName}.zip"):
            descomprimeArquivo(directorioDescarga, prName)

    # Obtemos a lista de tódolos arquivos e movémolos dos subdirectorios ó directorio principal
    for f in glob.glob(directorioDescarga+'**/*.nc', recursive=True):
        if directorioDescarga != os.path.dirname(f)+'/':
            shutil.move(f, directorioDescarga)
            shutil.rmtree(os.path.dirname(f))

