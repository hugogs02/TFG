import harp, os, glob

# Funcion que transforma a nivel 3 os datos de CO
def transformaL3_CO(rutaIn, rutaOut):
    return None

# Funcion que transforma a nivel 3 os datos de NO2
def transformaL3_NO2(rutaIn, rutaOut):
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
    """files_in="S5P_OFFL_L2__CO_____20230601T113651_20230601T131821_29185_03_020500_20230603T073706.nc"
    print(files_in)
    mean_no2=harp.import_product(files_in, operations, post_operations=reduce_operations)

    harp.export_product(mean_no2, 's5p-NO2_L3_averaged_11-17_Oct2021.nc')

    no2 = mean_no2.tropospheric_NO2_column_number_density.data
    no2_description = mean_no2.tropospheric_NO2_column_number_density.description
    no2_units = mean_no2.tropospheric_NO2_column_number_density.unit"""

    """gridlat = np.append(mean_no2.latitude_bounds.data[:,0], mean_no2.latitude_bounds.data[-1,1])
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

# Funcion que transforma a nivel 3 os datos de O3
def transformaL3_O3(rutaIn, rutaOut):
    return None

# Funcion que transforma a nivel 3 os datos de SO2
def transformaL3_SO2(rutaIn, rutaOut):
    operations=";".join([
        #"SO2_column_number_density_validity>50",
        #"count>0"
    ])
    reduce_operations = ";".join([
        "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds))",
        "bin()"
    ])
    input_path='data/unproc/SO2/'
    export_path='/data/SO2/'
    list_files = sorted(os.listdir(input_path))
    files_input = sorted(glob.glob(input_path+'S5P_OFFL_*.nc'))
    for file in list_files:
        if file.startswith("S5P_OFFL_") == False:
            list_files.remove(file)

    for i in range(len(files_input)):
        Converted_SO2 = harp.import_product(files_input[i], operations=operations, reduce_operations=reduce_operations)

    print("All files imported")
    harp.export_product(Converted_SO2, ('2023-09-w1.nc'), file_format="netCDF")
    #harp.export_product(Converted_SO2, 'S5P_SO2_L3_averaged_31Jul-07Aug2023.nc',file_format="net")

    return None

# Funcion que transforma a nivel 3 os datos de HCHO
def transformaL3_HCHO(rutaIn, rutaOut):
    return None

# Funcion que transforma a nivel 3 os datos de CH4
def transformaL3_CH4(rutaIn, rutaOut):
    return None



# Funcion xeral para transformar a nivel 3 o arquivo en 'ruta' para o produto 'produto'
def transformaL3 (rutaIn, rutaOut, produto):
    if produto == "L2__CO____":
        transformaL3_CO(rutaIn, rutaOut)
    elif produto == "L2__NO2___":
        transformaL3_NO2(rutaIn, rutaOut)
    elif produto == "L2__O3____":
        transformaL3_O3(rutaIn, rutaOut)
    elif produto == "L2__SO2___":
        transformaL3_SO2(rutaIn, rutaOut)
    elif produto == "L2__HCHO__":
        transformaL3_HCHO(rutaIn, rutaOut)
    elif produto == ("L2__CH4___"):
        transformaL3_CH4(rutaIn, rutaOut)
    else:
        print("Produto incorrecto para transformar")