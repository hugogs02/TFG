import sys
from dateutil.parser import parse

import dataDownload as dd
import dataTransform as dt

def run(produto, dataInicio, dataFin, rutaIn, rutaOut):
    """
    Esta función executa a busca, descarga e procesado dos arquivos
    :param produto: produto a descargar (debe ser L2__CO____, L2__NO2___, L2__O3____ ou L2__SO2___)
    :param dataInicio: data de inicio da busca
    :param dataFin: data de fin da busca
    :param rutaIn: ruta na que se descargan os arquivos
    :param rutaOut: ruta na que se gardan os arquivos procesados
    """
    # Comprobamos que o formato das datas é correcto
    try:
        parse(dataInicio)
        parse(dataFin)
    except ValueError:
        sys.exit(f"O formato de datas e incorrecto")

    # En caso de que o produto non estea na lista ou a data de inicio da busca sexa posterior á de fin, saímos do programa
    # (isto está pensado para a execución por liña de comandos)
    if produto not in ["L2__CO____", "L2__NO2___", "L2__O3____", "L2__SO2___"]:
        sys.exit(f"O produto {produto} non e un produto valido.")
    elif parse(dataInicio) > parse(dataFin):
        sys.exit(f"A data de inicio debe ser anterior a data de fin.")


    # Definimos a área de interese da busca
    aoi= "POLYGON((-9.647785 35.912135,-9.647785 44.230843,4.916224 44.230843,4.916224 35.912135,-9.647785 35.912135))"

    # Buscamos, descargamos e transformamos os arquivos
    dd.obtenArquivos(aoi, dataInicio, dataFin, produto, rutaIn)
    dt.transformaL3(rutaIn, rutaOut, produto)

# Con isto, permitimos a execución por liña de comandos
if __name__ == '__main__':
    # O número de argumentos debe ser 6 (o nome do script e os 5 parámetros); se non, saímos
    if len(sys.argv) != 6:
        print("Numero incorrecto de argumentos. [python3 app.py produto data_inicio data_fin ruta_descarga ruta_procesado]")
        print("Produtos: L2__CO____, L2__NO2___, L2__O3____, L2__SO2___")
        print("Formato de data: YYYY-MM-DD")
        sys.exit()

    # Executamos a función principal
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
