from sentinelsat import SentinelAPI
from sentinel5dl import search, download

# Funcion que obten a lista e tamaño dos arquivos a descargar
def listaArquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia):
    # Conexion a S5P Hub con credenciais de invitado
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Obtemos a lista de arquivos para unha rexion e datas especificas
    footprint = 'POLYGON((' + latW + ' ' + latS + ',' + latE + ' ' + latS + ',' + latE + ' ' + latN + ',' + latW + ' ' + latN + ',' + latW + ' ' + latS + '))'
    try:
        produtos = api.query(area=footprint, date=(inicio + 'T00:00:00Z', fin + 'T23:59:59Z'), producttype=parametro, processingmode=latencia)
        """produtos=search(polygon='POLYGON((7.8 49.3,13.4 49.3,13.4 52.8,7.8 52.8,7.8 49.3))',
        begin_ts=inicio + 'T00:00:00Z',
        end_ts=fin + 'T23:59:59Z',
        product=parametro,
        processing_level='L2',
        processing_mode=latencia)
        print(produtos)"""
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
def obtenArquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia, directorio):
    # Obtemos a lista de arquivos a descargar
    listaNomes, listaTamanos, produtos = listaArquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia)

    # Imprimimos os nomes e tamaños dos arquivos
    if len(listaNomes) > 0:
        print('\nDescargaranse os seguintes ' + str(len(listaNomes)) + ' arquivos no directorio: ', directorio)
        for arq, tam in zip(listaNomes, listaTamanos):
            print(arq, ' (', tam, ')', sep='')

        # Descargamos os arquivos
        #descargaArquivos(produtos, directorio)
    else:
        print('\nNon se obtivo ningun arquivo. Por favor, intenteo de novo.')
