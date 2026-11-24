"""
EDA del dataset Locales_202104.csv con Sweetviz.

CSV del Ayuntamiento de Madrid: separador ';', codificación Latin-1
(no UTF-8), coma decimal y campos de texto con espacios de relleno.
"""
import pandas as pd
import sweetviz as sv


def main():
    df = pd.read_csv(
        "data/Locales_202104.csv",
        sep=";",               # separador punto y coma
        encoding="latin-1",    # este fichero NO está en UTF-8
        dtype=str,             # se lee todo como texto y se convierte después
    )

    # Quitar los espacios de relleno ("CALLE      " -> "CALLE")
    for col in df.columns:
        df[col] = df[col].str.strip().replace("", pd.NA)

    # Columnas numéricas reales (coordenadas con coma decimal)
    for col in ["coordenada_x_local", "coordenada_y_local",
                "coordenada_x_agrupacion", "coordenada_y_agrup"]:
        df[col] = pd.to_numeric(df[col].str.replace(",", ".", regex=False), errors="coerce")

    reporte = sv.analyze(df, pairwise_analysis="off")
    reporte.show_html("reporte_locales.html")


if __name__ == "__main__":
    main()
