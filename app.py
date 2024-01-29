import sys
from dateutil.parser import parse

import dataDownload as dd
import dataTransform as dt

#Funcion run. Recibe como argumentos seis strings:
#   produto: o indicador que se descagara e procesara
#   start_date, end_date: as datas de inicio e fin da busca para a descarga de datos
#   rutaIn: a ruta onde se descargaran os arquivos obtidos de TROPOMI
#   rutaOut: a ruta onde se almacenaran os arquivos procesados de nivel 3
def run(produto, dataInicio, dataFin, rutaIn, rutaOut):
    try:
        parse(dataInicio)
        parse(dataFin)
    except ValueError:
        sys.exit(f"O formato de datas e incorrecto")

    if produto not in ["L2__CO____", "L2__NO2___", "L2__O3____", "L2__SO2___"]:
        sys.exit(f"O produto {produto} non e un produto valido.")
    elif parse(dataInicio)>parse(dataFin):
        sys.exit(f"A data de inicio debe ser anterior a data de fin.")


    # Area de interese da busca
    aoi= "POLYGON((-9.647785 35.912135,-9.647785 44.230843,4.916224 44.230843,4.916224 35.912135,-9.647785 35.912135))"

    dd.obtenArquivos(aoi, dataInicio, dataFin, produto, rutaIn)

    dt.transformaL3(rutaIn, rutaOut, produto)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta_descarga ruta_procesado]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____, L2__SO2___")
        print("Formato de data: YYYY-MM-DD")
        sys.exit()

    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
