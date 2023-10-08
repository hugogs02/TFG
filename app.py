import sys

from sentinelsat import SentinelAPI
import os
import harp

# Funcion que obten a lista e tamaño dos arquivos a descargar
def lista_arquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia):
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
def descarga_arquivos(produtos, directorio):
    # Conexion a S5P Hub con credenciais de invitado
    api = SentinelAPI('s5pguest', 's5pguest', 'https://s5phub.copernicus.eu/dhus')

    # Descargamos os arquivos
    try:
        api.download_all(produtos, directorio)
    except KeyboardInterrupt:
        print('\nO usuario interrompeu a descarga.')


# Funcion que imprime os arquivos a descargar
def obten_arquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia, directorio):
    # Obtemos a lista de arquivos a descargar
    listaNomes, listaTamanos, produtos = lista_arquivos(latW, latE, latS, latN, inicio, fin, parametro, latencia)

    # Imprimimos os nomes e tamaños dos arquivos
    if len(listaNomes) > 0:
        print('\nDescargaranse os seguintes ' + str(len(listaNomes)) + ' arquivos no directorio: ', directorio)
        for arq, tam in zip(listaNomes, listaTamanos):
            print(arq, ' (', tam, ')', sep='')
        descarga_arquivos(produtos, directorio)
    else:
        print('\nNon se obtivo ningun arquivo. Por favor, intenteo de novo.')

def transforma_a_L3 (ruta,producto):

    return None

if __name__ == '__main__':
    if len(sys.argv)!=5:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____', L2__SO2___, L2__HCHO__")
        sys.exit()

    # Coordenadas da busca
    lat_N = str(44.52157244578214)
    lat_S = str(35.55367980635542)
    lon_W = str(-10.177733302116385)
    lon_E = str(4.798831343650816)

    # Produto a descargar
    #produto = 'L2__CO____'
    #produto = 'L2__NO2___'
    #produto = 'L2__O3____'
    #produto = 'L2__SO2___'
    #produto = 'L2__HCHO__'
    produto=sys.argv[1]

    # Filtro de datas
    #start_date = '2023-05-01'
    #end_date = '2023-06-05'
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    # Ruta para descarga
    #ruta = "data/HCHO"
    ruta=sys.argv[4]

    obten_arquivos(lon_W, lon_E, lat_S, lat_N, start_date, end_date, produto, 'Offline', ruta)

    transforma_a_L3(ruta,produto)
    # qa>0.5
    patron = "*.nc"
    listar = []

    # os.chdir(ruta)
    # for f in os.listdir(ruta):
    #     if f.endswith(patron):
    #         listar.append(str(os.path.join(ruta, f)))

    # print("-----------------")
    # print("Rutas arquivos")
    #for i in listar:
    #    print(str(i))

    #file_path='S5P_OFFL_L2__CO_____20230501T111601_20230501T125731_28745_03_020500_20230503T010442.nc'


operations = ";".join([
    "tropospheric_NO2_column_number_density_validity>75",
    "derive(surface_wind_speed {time} [m/s])",
     "surface_wind_speed<5",
    "keep(latitude_bounds,longitude_bounds,datetime_start,datetime_length,tropospheric_NO2_column_number_density, surface_wind_speed)",
    "derive(datetime_start {time} [days since 2000-01-01])",
    "derive(datetime_stop {time}[days since 2000-01-01])",
    "exclude(datetime_length)",
    "bin_spatial(51,33.50,0.02,51,-118.5,0.02)",
    "derive(tropospheric_NO2_column_number_density [Pmolec/cm2])",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    "count>0"
])

reduce_operations=";".join([
    "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds))",
    "bin()"
])

#files_in="S5P_OFFL_L2__NO2____202110*.nc"
files_in="S5P_OFFL_L2__CO_____20230601T113651_20230601T131821_29185_03_020500_20230603T073706.nc"
print(files_in)
mean_no2=harp.import_product(files_in, operations, post_operations=reduce_operations)

harp.export_product(mean_no2, 's5p-NO2_L3_averaged_11-17_Oct2021.nc')

no2 = mean_no2.tropospheric_NO2_column_number_density.data
no2_description = mean_no2.tropospheric_NO2_column_number_density.description
no2_units = mean_no2.tropospheric_NO2_column_number_density.unit

gridlat = np.append(mean_no2.latitude_bounds.data[:,0], mean_no2.latitude_bounds.data[-1,1])
gridlon = np.append(mean_no2.longitude_bounds.data[:,0], mean_no2.longitude_bounds.data[-1,1])

colortable = cm.roma_r
vmin = 0
vmax = 14

# Setting basemap

boundaries=[-118.5, -117.5, 33.5, 34.0]

fig = plt.figure(figsize=(10,10))
bmap=cimgt.Stamen(style='toner-lite')
ax = plt.axes(projection=bmap.crs)
ax.set_extent(boundaries,crs = ccrs.PlateCarree())

zoom = 10
ax.add_image(bmap, zoom)

# Adding NO2 data

img = plt.pcolormesh(gridlon, gridlat, no2[0,:,:], vmin=vmin, vmax=vmax, cmap=colortable, transform=ccrs.PlateCarree(),alpha = 0.55)
ax.coastlines()

cbar = fig.colorbar(img, ax=ax,orientation='horizontal', fraction=0.04, pad=0.1)
cbar.set_label(f'{no2_description} [{no2_units}]')
cbar.ax.tick_params(labelsize=14)

plt.show()"""