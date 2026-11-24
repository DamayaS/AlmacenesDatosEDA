"""
EDA del dataset Terrazas_202104.csv con Sweetviz.

CSV del Ayuntamiento de Madrid: separador ';', codificación Latin-1
(no UTF-8), coma decimal y campos de texto con espacios de relleno.
"""
import pandas as pd
import sweetviz as sv


def main():
    df = pd.read_csv(
        "data/Terrazas_202104.csv",
        sep=";",               # separador punto y coma
        encoding="latin-1",    # este fichero NO está en UTF-8
        dtype=str,             # se lee todo como texto y se convierte después
    )

    # Quitar los espacios de relleno ("CALLE      " -> "CALLE")
    for col in df.columns:
        df[col] = df[col].str.strip().replace("", pd.NA)

    # Columnas numéricas reales: coordenadas, superficies, mesas y sillas.
    # sillas_ra no se incluye: en origen contiene letras (A, B, C...), no números.
    numericas = ["coordenada_x_local", "coordenada_y_local",
                 "coordenada_x_agrupacion", "coordenada_y_agrupacion",
                 "Superficie_ES", "Superficie_RA",
                 "mesas_aux_es", "mesas_aux_ra", "mesas_es", "mesas_ra", "sillas_es"]
    for col in numericas:
        df[col] = pd.to_numeric(df[col].str.replace(",", ".", regex=False), errors="coerce")

    # Fecha en formato día/mes/año; 31/12/9999 significa "sin fecha"
    fecha = df["Fecha_confir_ult_decreto_resol"].replace("31/12/9999", pd.NA)
    df["Fecha_confir_ult_decreto_resol"] = pd.to_datetime(fecha, format="%d/%m/%Y", errors="coerce")

    reporte = sv.analyze(df, pairwise_analysis="off")
    reporte.show_html("reporte_terrazas.html")


if __name__ == "__main__":
    main()
