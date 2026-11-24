import pandas as pd
import sweetviz as sv

def unir(lista):
    elementos = [x.strip() for x in lista if x and x.strip()]
    return ", ".join(elementos) if elementos else None

def main():
    print("Main program")

    df = pd.read_json("data/books.json")
    df["_id"] = df["_id"].apply(lambda v: v["$oid"] if isinstance(v, dict) else str(v))
    df["authors"] = df["authors"].apply(unir)
    df["categories"] = df["categories"].apply(unir)
    df["publishedDate"] = pd.to_datetime(df["publishedDate"].apply(lambda v: v["$date"][:10] if isinstance(v, dict) else None))
    reporte = sv.analyze(df)
    reporte.show_html("reporte_books.html")

    
    df = pd.read_csv("data/Licencias_Locales_202104.csv",sep=";", decimal=",", encoding="utf-8", dtype=str)
    reporte = sv.analyze(df)
    reporte.show_html("reporte_licencias_locales.html")
    
    df = pd.read_csv("data/Locales_202104.csv", sep=";",decimal=",",encoding="latin-1",dtype=str)
    reporte = sv.analyze(df)
    reporte.show_html("reporte_locales.html")
    
    df = pd.read_csv("data/Terrazas_202104.csv", sep=";", decimal=",", encoding="latin-1", dtype=str)
    reporte = sv.analyze(df)
    reporte.show_html("reporte_terrazas.html")    

if __name__ == "__main__":
    main()