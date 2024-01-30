import app, time
from datetime import date
from calendar import monthrange

def getDates():
    """
    Función que, tomando como referencia o día actual, devolve o primeiro e último día do mes anterior
    :return: dúas datas (inicio e fin do mes previo)
    """
    # Obtemos a data actual
    today = date.today()
    month = today.month
    # Se o mes é xaneiro, establecémolo a decembro e restamos unha unidade ó ano
    if month == 1:
        month = 12
        year = today.year - 1
    else:
        month = month - 1
        year = today.year
    # Obtemos o último día do mes
    days = monthrange(year, month)[1]

    # Formateamos a data para que o mes teña sempre dous díxitos
    if month < 10:
        monthstr = "0"+f"{month}"
    else:
        monthstr = f"{month}"

    # Obtemos as datas e devolvémolas
    inicio = f"{year}"+"-"+ monthstr +"-"+"01"
    final = f"{year}"+"-"+ monthstr +"-"+f"{days}"
    return (inicio,final)


if __name__ == '__main__':
    # Establecemos as datas e o directorio de descarga dos datos
    inicio, fin = getDates()
    descargaEn = "data/unproc/"

    # Executamos o programa principal, para cada un dos catro parametros
    app.run("L2__NO2___", inicio, fin, descargaEn, "data/NO2/")
    app.run("L2__CO____", inicio, fin, descargaEn, "data/CO/")
    app.run("L2__SO2___", inicio, fin, descargaEn, "data/SO2/")
    app.run("L2__O3____", inicio, fin, descargaEn, "data/O3/")
