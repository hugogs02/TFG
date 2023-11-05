import sys
import dataDownload as dd
import dataTransform as dt

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____', L2__SO2___, L2__HCHO__, L2__CH4___")
        print("Formato de data: YYYY-MM-DD")
        sys.exit()

    # Coordenadas da busca
    lat_N = str(44.52157244578214)
    lat_S = str(35.55367980635542)
    lon_W = str(-10.177733302116385)
    lon_E = str(4.798831343650816)

    # Produto a descargar
    produto = sys.argv[1]

    # Filtro de datas
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    # Ruta para descarga
    ruta = sys.argv[4]

    dd.obtenArquivos(lon_W, lon_E, lat_S, lat_N, start_date, end_date, produto, 'Offline', ruta)

    dt.transformaL3(ruta, produto)
    patron = "*.nc"
    listar = []

    # os.chdir(ruta)
    # for f in os.listdir(ruta):
    #     if f.endswith(patron):
    #         listar.append(str(os.path.join(ruta, f)))

    # print("-----------------")
    # print("Rutas arquivos")
    # for i in listar:
    #    print(str(i))

    # file_path='S5P_OFFL_L2__CO_____20230501T111601_20230501T125731_28745_03_020500_20230503T010442.nc'
