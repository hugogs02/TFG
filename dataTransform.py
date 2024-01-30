import harp, os, glob

# Definimos as postoperacións a aplicar con HARP, que serán comúns a tódolos parámetros
postops = ";".join([
    "bin()",
    "squash(time, (latitude, longitude))"
])

def obtenListaProdutos(rutaIn, produto):
    """
    Esta función obtén a lista de arquivos en rutaIn que sexan do produto "produto"
    :param rutaIn: ruta na que buscar os arquivos
    :param produto: produto que se quere buscar
    :return: lista de arquivos na ruta que coincidan co parámetro
    """
    lista=[]
    for f in sorted(glob.glob(rutaIn+'*'+produto+'*.nc')):
        lista.append(f)

    return lista


def transformaL3_NO2(arquivos, rutaOut):
    """
    Esta función transforma a nivel L3 os produtos de NO2 de "arquivos" e gárdaos en rutaOut
    :param arquivos: arquivos a transformar
    :param rutaOut: ruta onde se almacena o arquivo procesado
    """
    # Definimos as operacións que aplicaremos ó importar os arquivos
    ops= ";".join([
        "tropospheric_NO2_column_number_density_validity>75",
        "derive(tropospheric_NO2_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,tropospheric_NO2_column_number_density)"
    ])

    # Definimos as operacións que aplicaremos ós produtos unha vez importados
    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    # Creamos unha lista vacía, na que gardaremos os produtos segundo os vaiamos importando-
    prodslist=[]
    for f in arquivos:
        print(f"Importando {f}")
        p=harp.import_product(f, operations=ops)
        prodslist.append(p)

    # Executamos as operacions e postoperacions sobre os arquivos importados
    prods=harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    # Para obter o nome do arquivo, concatenaremos o produto (NO2) cun _, o ano e o mes. Esta data podémola obter dun dos nomes dos ficheiros que se importan
    mes=arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}NO2_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}NO2_{mes}.nc exportado")


def transformaL3_CO(arquivos, rutaOut):
    """
    Esta función transforma a nivel L3 os produtos de CO de "arquivos" e gárdaos en rutaOut
    :param arquivos: arquivos a transformar
    :param rutaOut: ruta onde se almacena o arquivo procesado
    """
    # Definimos as operacións que aplicaremos ó importar os arquivos
    ops = ";".join([
        "CO_column_number_density_validity>50",
        "derive(CO_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,CO_column_number_density)"
    ])

    # Definimos as operacións que aplicaremos ós produtos unha vez importados
    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    # Creamos unha lista vacía, na que gardaremos os produtos segundo os vaiamos importando-
    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    # Executamos as operacions e postoperacions sobre os arquivos importados
    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    # Para obter o nome do arquivo, concatenaremos o produto (CO) cun _, o ano e o mes. Esta data podémola obter dun dos nomes dos ficheiros que se importan
    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}CO_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}CO_{mes}.nc exportado")


def transformaL3_O3(arquivos, rutaOut):
    """
    Esta función transforma a nivel L3 os produtos de O3 de "arquivos" e gárdaos en rutaOut
    :param arquivos: arquivos a transformar
    :param rutaOut: ruta onde se almacena o arquivo procesado
    """
    # Definimos as operacións que aplicaremos ó importar os arquivos
    ops = ";".join([
        "O3_column_number_density_validity>50",
        "derive(O3_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,O3_column_number_density)"
    ])

    # Definimos as operacións que aplicaremos ós produtos unha vez importados
    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    # Creamos unha lista vacía, na que gardaremos os produtos segundo os vaiamos importando-
    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    # Executamos as operacions e postoperacions sobre os arquivos importados
    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    # Para obter o nome do arquivo, concatenaremos o produto (O3) cun _, o ano e o mes. Esta data podémola obter dun dos nomes dos ficheiros que se importan
    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}O3_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}O3_{mes}.nc exportado")


def transformaL3_SO2(arquivos, rutaOut):
    """
    Esta función transforma a nivel L3 os produtos de SO2 de "arquivos" e gárdaos en rutaOut
    :param arquivos: arquivos a transformar
    :param rutaOut: ruta onde se almacena o arquivo procesado
    """
    # Definimos as operacións que aplicaremos ó importar os arquivos
    ops = ";".join([
        "SO2_column_number_density_validity>50",
        "derive(SO2_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,SO2_column_number_density)"
    ])

    # Definimos as operacións que aplicaremos ós produtos unha vez importados
    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    # Creamos unha lista vacía, na que gardaremos os produtos segundo os vaiamos importando-
    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    # Executamos as operacions e postoperacions sobre os arquivos importados
    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    # Para obter o nome do arquivo, concatenaremos o produto (SO2) cun _, o ano e o mes. Esta data podémola obter dun dos nomes dos ficheiros que se importan
    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}SO2_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}SO2_{mes}.nc exportado")


def transformaL3 (rutaIn, rutaOut, produto):
    """
    Función xenérica para transforma a L3 os arquivos de produto en rutaIn, e almacenar o resultante en rutaOut
    :param rutaIn:
    :param rutaOut:
    :param produto:
    """
    # Creamos o directorio de saída, se non existe, e obtemos a lista de arquivos a transformar
    if not os.path.exists(rutaOut):
        os.mkdir(rutaOut)
    listaArquivos=obtenListaProdutos(rutaIn, produto)

    # En función do produto, chamamos á función correspondente
    if   produto == "L2__CO____":
        transformaL3_CO(listaArquivos, rutaOut)
    elif produto == "L2__NO2___":
        transformaL3_NO2(listaArquivos, rutaOut)
    elif produto == "L2__O3____":
        transformaL3_O3(listaArquivos, rutaOut)
    elif produto == "L2__SO2___":
        transformaL3_SO2(listaArquivos, rutaOut)
    else:
        print("Produto incorrecto para transformar")

    # Eliminamos os arquivos empregados
    for f in listaArquivos:
        os.remove(f)

