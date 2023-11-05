from sentinelsat import SentinelAPI

# Funcion que obten a lista e tamaño dos arquivos a descargar
def listaArquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia):
    # Conexion a S5P Hub con credenciais de invitado
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Obtemos a lista de arquivos para unha rexion e datas especificas
    footprint = 'POLYGON((' + latW + ' ' + latS + ',' + latE + ' ' + latS + ',' + latE + ' ' + latN + ',' + latW + ' ' + latN + ',' + latW + ' ' + latS + '))'
    try:
        produtos = api.query(area=footprint, date=(inicio + 'T00:00:00Z', fin + 'T23:59:59Z'),
                             producttype=parametro, processingmode=latencia)
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
