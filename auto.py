import app, time
from datetime import date
from calendar import monthrange

def getDates():
    today = date.today()
    month = today.month
    if month == 1:
        month = 12
        year = today.year - 1
    else:
        month = month - 1
        year = today.year
    days = monthrange(year, month)[1]
    if month < 10:
        monthstr = "0"+f"{month}"
    else:
        monthstr = f"{month}"
    inicio = f"{year}"+"-"+ monthstr +"-"+"01"
    final = f"{year}"+"-"+ monthstr +"-"+f"{days}"
    return (inicio,final)

    
if __name__ == '__main__':
    inicio, fin = getDates()
    descargaEn = "data/unproc/"

    app.run("L2__NO2___", inicio, fin, descargaEn, "data/NO2/")
    time.sleep(60)
    app.run("L2__CO____", inicio, fin, descargaEn, "data/CO/")
    time.sleep(60)
    app.run("L2__SO2___", inicio, fin, descargaEn, "data/SO2/")
    time.sleep(60)
    app.run("L2__O3____", inicio, fin, descargaEn, "data/O3/")