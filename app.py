import sys, glob, zipfile
import dataDownload as dd
import dataTransform as dt

#Funcion run. Recibe como argumentos seis strings:
#   produto: o indicador que se descagara e procesara
#   start_date, end_date: as datas de inicio e fin da busca para a descarga de datos
#   rutaIn: a ruta onde se descargaran os arquivos obtidos de TROPOMI
#   rutaOut: a ruta onde se almacenaran os arquivos procesados de nivel 3
def run(produto, start_date, end_date, rutaIn, rutaOut):
    # Area de interese da busca
    aoi= "POLYGON((12.655118166047592 47.44667197521409,21.39065656328509 48.347694733853245,28.334291357162826 41.877123516783655,17.47086198383573 40.35854475076158,12.655118166047592 47.44667197521409))"

    dd.obtenArquivos(aoi, start_date, end_date, produto, rutaIn)

    for f in glob.glob('*.zip'):
        print(f"{f}.zip")
        try:
            with zipfile.ZipFile(f"{f}.zip", 'r') as e:
                e.extractall(rutaIn)
                a='a'
        except zipfile.BadZipfile:
            print(f"Warning: Encountered a BadZipFile exception, but attempting extraction anyway.")

    #dt.transformaL3(rutaIn, rutaOut, produto)

    #print("Data averaged correctly")

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta_descarga ruta_procesado]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____, L2__SO2___, L2__CH4___")
        print("Formato de data: YYYY-MM-DD")
        sys.exit()

    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])