import sys
import dataDownload as dd
import dataTransform as dt

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta_descarga ruta_procesado]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____, L2__SO2___, L2__HCHO__, L2__CH4___")
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
    rutaIn = sys.argv[4]
    rutaOut = sys.argv[5]

    dd.obtenArquivos(lon_W, lon_E, lat_S, lat_N, start_date, end_date, produto, rutaIn)

    #dt.transformaL3(rutaIn, rutaOut, produto)

    #print("Data averaged correctly")