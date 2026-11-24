"""
Prepara los 4 ficheros para que Dremio pueda leerlos.
No limpia ni formatea: los valores quedan exactamente igual (incluidos
espacios de relleno, ceros, fechas 1900/9999, etc.). Solo corrige lo que
impide la lectura.
"""
import csv
import json
from pathlib import Path

ENTRADA = Path("data")
SALIDA = Path("dremio")
SALIDA.mkdir(exist_ok=True)


def leer_registros(ruta, encoding, entrecomillado):
    """Separa el fichero en filas y campos sin interpretar los valores."""
    texto = ruta.read_bytes().decode(encoding)
    # Las filas acaban en CRLF; un salto LF suelto dentro de un campo se trata igual
    filas = [f for f in texto.replace("\r\n", "\n").split("\n") if f]
    trocear = (lambda f: f[1:-1].split('";"')) if entrecomillado else (lambda f: f.split(";"))
    n = len(trocear(filas[0]))
    registros, pendiente, unidos = [], None, 0
    for fila in filas:
        # Un salto de línea dentro de un rótulo parte el registro en dos
        # líneas: se vuelven a unir (con un espacio) hasta tener todos los campos.
        if pendiente is not None:
            fila = pendiente + " " + fila
            unidos += 1
        if len(trocear(fila)) < n:
            pendiente = fila
            continue
        pendiente = None
        registros.append(trocear(fila))
    if unidos:
        print(f"{ruta.name}: {unidos} salto(s) de línea dentro de un campo sustituido(s) por espacio")
    malas = [i for i, r in enumerate(registros) if len(r) != n]
    assert not malas, f"{ruta.name}: filas con nº de campos distinto: {malas[:5]}"
    return registros


def escribir_csv(registros, nombre):
    """CSV estándar: UTF-8, separador ;, todos los campos entre comillas
    y las comillas internas escapadas duplicándolas ("")."""
    with open(SALIDA / nombre, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        w.writerows(registros)
    print(f"{nombre}: {len(registros) - 1} filas, {len(registros[0])} columnas")


# 1) Licencias: UTF-8, pero hay comillas internas sin escapar
escribir_csv(leer_registros(ENTRADA / "Licencias_Locales_202104.csv", "utf-8", True),
             "Licencias_Locales_202104.csv")

# 2) Locales: Latin-1 y comillas internas sin escapar ("GALERIA "LA ESTRELLA"")
escribir_csv(leer_registros(ENTRADA / "Locales_202104.csv", "latin-1", True),
             "Locales_202104.csv")

# 3) Terrazas: Latin-1 y campos sin comillas, pero algún rótulo empieza por "
escribir_csv(leer_registros(ENTRADA / "Terrazas_202104.csv", "latin-1", False),
             "Terrazas_202104.csv")

# 4) Libros: JSON Lines (un objeto por línea). Único cambio: _id mezcla
#    enteros (1, 2...) y objetos {"$oid": "..."}; Dremio necesita un solo tipo
#    por columna, así que todos pasan a texto con el mismo valor.
#    Sirve tanto para el original (un objeto por línea) como para la versión
#    convertida en array [ {...}, {...} ].
texto = (ENTRADA / "books.json").read_text(encoding="utf-8")
if texto.lstrip().startswith("["):
    docs = json.loads(texto)
else:
    docs = [json.loads(linea) for linea in texto.splitlines() if linea.strip()]

with open(SALIDA / "books.json", "w", encoding="utf-8") as f_out:
    for doc in docs:
        _id = doc["_id"]
        doc["_id"] = _id["$oid"] if isinstance(_id, dict) else str(_id)
        f_out.write(json.dumps(doc, ensure_ascii=False) + "\n")
print(f"books.json: {len(docs)} documentos")
