"""
EDA del dataset books.json con Sweetviz.

El fichero es una exportación de MongoDB: algunos campos son diccionarios
({"$date": ...}, {"$oid": ...}) y otros listas (authors, categories).
Sweetviz no admite esas estructuras, así que se convierten en valores simples
antes de generar el informe.
"""
import pandas as pd
import sweetviz as sv


def cargar(ruta):
    # El original es JSON Lines (un objeto por línea); si se ha convertido
    # en un array [ {...}, {...} ], se lee sin lines=True.
    with open(ruta, encoding="utf-8") as f:
        es_array = f.read(1024).lstrip().startswith("[")
    return pd.read_json(ruta, lines=not es_array)


def unir(lista):
    """["A", "", "B"] -> "A, B"; lista vacía -> valor ausente."""
    elementos = [x.strip() for x in lista if x and x.strip()]
    return ", ".join(elementos) if elementos else None


def main():
    df = cargar("data/books.json")

    # _id: {"$oid": "53c2..."} -> 53c2... ; 1 -> "1"
    df["_id"] = df["_id"].apply(lambda v: v["$oid"] if isinstance(v, dict) else str(v))

    # publishedDate: {"$date": "2009-04-01T00:00..."} -> fecha 2009-04-01
    df["publishedDate"] = pd.to_datetime(
        df["publishedDate"].apply(lambda v: v["$date"][:10] if isinstance(v, dict) else None)
    )

    # authors y categories: listas -> texto separado por comas
    df["authors"] = df["authors"].apply(unir)
    df["categories"] = df["categories"].apply(unir)

    reporte = sv.analyze(df)
    reporte.show_html("reporte_books.html")


if __name__ == "__main__":
    main()
