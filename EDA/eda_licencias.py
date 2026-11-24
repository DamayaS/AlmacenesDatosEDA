"""
EDA del dataset Licencias_Locales_202104.csv con Sweetviz.

CSV del Ayuntamiento de Madrid: separador ';', UTF-8, coma decimal y
campos de texto con espacios de relleno.
"""
import pandas as pd
import sweetviz as sv


def main():
    df = pd.read_csv(
        "data/Licencias_Locales_202104.csv",
        sep=";",            # el separador es punto y coma, no coma
        encoding="utf-8",
        dtype=str,          # se lee todo como texto y se convierte después
    )

    # Quitar los espacios de relleno ("CENTRO              " -> "CENTRO")
    for col in df.columns:
        df[col] = df[col].str.strip().replace("", pd.NA)

    # Columnas numéricas reales (coordenadas con coma decimal)
    for col in ["coordenada_x_local", "coordenada_y_local",
                "coordenada_x_agrupacion", "coordenada_y_agrupacion"]:
        df[col] = pd.to_numeric(df[col].str.replace(",", ".", regex=False), errors="coerce")

    # Fecha en formato día/mes/año
    df["Fecha_Dec_Lic"] = pd.to_datetime(df["Fecha_Dec_Lic"], format="%d/%m/%Y", errors="coerce")

    # Con 46 columnas la matriz de correlaciones sería ilegible y muy lenta
    reporte = sv.analyze(df, pairwise_analysis="off")
    reporte.show_html("reporte_licencias.html")


if __name__ == "__main__":
    main()
