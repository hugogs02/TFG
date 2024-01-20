import harp, os, glob

postops = ";".join([
    "bin()",
    "squash(time, (latitude, longitude))"
])

def obtenListaProdutos(rutaIn, produto):
    lista=[]
    for f in sorted(glob.glob(rutaIn+'*'+produto+'*.nc')):
        lista.append(f)

    return lista

# Funcion que transforma a nivel 3 os datos de NO2
def transformaL3_NO2(arquivos, rutaOut):
    ops= ";".join([
        "tropospheric_NO2_column_number_density_validity>75",
        "derive(tropospheric_NO2_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,tropospheric_NO2_column_number_density)"
    ])

    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    prodslist=[]
    for f in arquivos:
        print(f"Importando {f}")
        p=harp.import_product(f, operations=ops)
        prodslist.append(p)

    prods=harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    mes=arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}NO2_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}NO2_{mes}.nc exportado")


# Funcion que transforma a nivel 3 os datos de CO
def transformaL3_CO(arquivos, rutaOut):
    ops = ";".join([
        "CO_column_number_density_validity>50",
        "derive(CO_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,CO_column_number_density)"
    ])

    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}CO_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}CO_{mes}.nc exportado")


# Funcion que transforma a nivel 3 os datos de O3
def transformaL3_O3(arquivos, rutaOut):
    ops = ";".join([
        "O3_column_number_density_validity>50",
        "derive(O3_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,O3_column_number_density)"
    ])

    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}O3_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}O3_{mes}.nc exportado")

# Funcion que transforma a nivel 3 os datos de SO2
def transformaL3_SO2(arquivos, rutaOut):
    ops = ";".join([
        "SO2_column_number_density_validity>50",
        "derive(SO2_column_number_density [Pmolec/cm2])",
        "keep(latitude,longitude,latitude_bounds,longitude_bounds,SO2_column_number_density)"
    ])

    exops = ";".join([
        "bin_spatial(2001, 35, 0.005, 3001, -10, 0.005)",
        "exclude(latitude_bounds_weight,longitude_bounds_weight,weight,latitude_weight,longitude_weight)",
        "derive(latitude{latitude})",
        "derive(longitude{longitude})"
    ])

    prodslist = []
    for f in arquivos:
        print(f"Importando {f}")
        p = harp.import_product(f, operations=ops)
        prodslist.append(p)

    prods = harp.execute_operations(prodslist, operations=exops, post_operations=postops)

    mes = arquivos[0].split("_")[-1][0:6]
    harp.export_product(prods, (f"{rutaOut}SO2_{mes}.nc"), file_format="netCDF")
    print(f"{rutaOut}SO2_{mes}.nc exportado")


# Funcion xeral para transformar a nivel 3 o arquivo en 'ruta' para o produto 'produto'
def transformaL3 (rutaIn, rutaOut, produto):
    if not os.path.exists(rutaOut):
        os.mkdir(rutaOut)
    listaArquivos=obtenListaProdutos(rutaIn, produto)

    if produto == "L2__CO____":
        transformaL3_CO(listaArquivos, rutaOut)
    elif produto == "L2__NO2___":
        transformaL3_NO2(listaArquivos, rutaOut)
    elif produto == "L2__O3____":
        transformaL3_O3(listaArquivos, rutaOut)
    elif produto == "L2__SO2___":
        transformaL3_SO2(listaArquivos, rutaOut)
    else:
        print("Produto incorrecto para transformar")