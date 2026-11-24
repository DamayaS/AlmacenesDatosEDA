# Calidad y gobernanza de datos: de ficheros en bruto a catálogo en Dremio

Análisis exploratorio (EDA), limpieza y catalogación de cuatro datasets heterogéneos para dejarlos **fiables, documentados y trazables** en una plataforma de datos corporativa (Dremio).

> Proyecto de la asignatura *Gobierno del dato y toma de decisiones* del Máster en Análisis y Visualización de Datos Masivos (2026).

---

## Objetivos

- Evaluar la estructura y la calidad de los datos mediante un EDA automatizado.
- Resolver los problemas que impiden cargar y usar los datos.
- Integrar los datasets en Dremio, documentarlos y transformarlos de forma controlada.
- Relacionar los hallazgos con las buenas prácticas de calidad y gobernanza del dato.

## Tecnologías

| Área | Herramientas |
| --- | --- |
| Carga y transformación | Python, pandas |
| Perfilado de calidad | Sweetviz |
| Catálogo y vistas | Dremio (SQL) |
| Entorno | Docker |

## Datasets

| Fichero | Formato | Contenido |
| --- | --- | --- |
| `books.json` | JSON | Catálogo de libros (431 registros) |
| `Licencias_Locales_202104.csv` | CSV | Licencias de actividad de locales |
| `Locales_202104.csv` | CSV | Censo de locales |
| `Terrazas_202104.csv` | CSV | Terrazas asociadas a locales |

Los tres datasets de locales se relacionan entre sí a través de `id_local`.

## Estructura del repositorio

```
├── data/
│   └── raw/                # Ficheros originales (sin modificar)
├── notebooks/
│   └── eda.ipynb           # Carga, normalización y EDA
├── reports/
│   └── sweetviz/           # Informes HTML de Sweetviz por dataset
├── sql/
│   └── dremio_views.sql    # Vistas virtuales creadas en Dremio
├── docs/
│   └── informe.pdf         # Informe completo con capturas
├── requirements.txt
└── README.md
```

## Cómo ejecutarlo

```bash
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
pip install -r requirements.txt
jupyter notebook notebooks/eda.ipynb
```

Para replicar la parte de Dremio:

```bash
docker pull dremio/dremio-oss
docker run -p 9047:9047 dremio/dremio-oss
```

Después, abre `http://localhost:9047`, crea una cuenta y sube los ficheros de `data/raw/`.

## 1. Problemas de carga resueltos

Ningún fichero se podía cargar con la configuración por defecto de pandas:

| Dataset | Problema | Solución |
| --- | --- | --- |
| `books.json` | JSON inválido: faltan los corchetes de la lista y las comas entre objetos | Reconstruir la lista de objetos |
| `books.json` | Campos anidados (`authors`, `categories`, `_id`) que Sweetviz no procesa | Listas a cadena con `join`, extracción del id numérico y tipado a `string`; `publishedDate` a `datetime` |
| CSV de licencias | Separador `;` | `sep=";"` |
| CSV de locales y terrazas | Codificación Latin-1 y coma decimal | `encoding="latin-1"`, `decimal=","` |

## 2. Hallazgos de calidad

### Libros
- **39 % de los libros tienen `pageCount = 0`**: un valor imposible que en realidad indica ausencia de dato y distorsiona la media y la mediana.
- **ISBN duplicados**: 424 valores distintos sobre 428 informados, así que hay 4 duplicados.
- **ISBN mal formados**: existen valores con menos dígitos de los esperados.
- **Hora irrelevante** añadida a todas las fechas de publicación.

### Licencias, locales y terrazas
- **Coordenadas a 0** en locales y agrupaciones, que de nuevo indican ausencia de dato.
- **9 % de fechas de licencia el 01/01/1900**, usada como *placeholder*; también aparecen fechas de 9999.
- **94 % de valores ausentes** en la agrupación: la mayoría de locales no pertenece a ninguna.
- **Columnas vacías** (`cod_barrio_local`, `id_seccion_censal_local`, `id_tipo_acceso_local`, `id_vial_edificio`, `id_vial_acceso`) o **constantes** (`id_clase_ndp_edificio`, `id_clase_ndp_acceso`, `nom_edificio`, entre otras), que no aportan información.
- **Categorías duplicadas** por errores tipográficos y de codificación. Por ejemplo, el mismo concepto aparece como `ROTULO NO INFORMADO`, `Rótulo no informado`, `RÃ³TULO NO INFORMADO`, `R0TULO NO INFORMADO`, `SR` o `S/R`.
- **Formatos inconsistentes** en el campo `planta` (`1`, `01`, `PB`, `sin planta`).
- **Nombres de columna distintos para el mismo dato** entre datasets (`coordenada_y_agrup` frente a `coordenada_y_agrupacion`).

## 3. Integración en Dremio

1. **Carga y verificación.** Se suben los cuatro ficheros con el formato correcto (JSON, separador `;`) y se comprueba que el número de filas y columnas, así como los caracteres especiales (ñ, tildes), son los esperados.
2. **Documentación.** Cada dataset tiene una página wiki con su origen, la definición de todos sus campos y las limitaciones de calidad detectadas en el EDA.
3. **Espacios de trabajo.** Se organizan las vistas virtuales en *spaces*, separadas de los datos originales.
4. **Vistas personalizadas.** Se crean vistas en SQL que limpian los datos sin modificar el origen. Por ejemplo, esta vista despliega los autores y categorías de cada libro en filas individuales:

```sql
SELECT title, isbn, pageCount, publishedDate, thumbnailUrl,
       shortDescription, longDescription, status,
       FLATTEN(authors)    AS authors,
       FLATTEN(categories) AS categories
FROM (
    SELECT title, isbn, pageCount, publishedDate, thumbnailUrl,
           shortDescription, longDescription, status, authors, categories
    FROM "@damaya".datasets.books AS books
    WHERE isbn IS NOT NULL
) nested_0;
```

## Conclusiones

- **El EDA define la estrategia de carga.** Los datos no se pueden integrar tal cual: hay que corregir el formato, la codificación y los separadores antes de cargarlos, y anticipar en Dremio el tratamiento de valores atípicos y campos multivalor.
- **Los ceros y las fechas imposibles no son datos.** Convertirlos a nulos es imprescindible para que los estadísticos y los análisis posteriores sean fiables.
- **Gobernanza por capas.** Los originales se conservan intactos para mantener la trazabilidad, la limpieza se aplica en vistas virtuales documentadas, y los datasets relacionados se pueden unir por `id_local` sobre datos ya limpios.

## Próximos pasos

- Unificar las categorías de `rotulo` y `planta` con un diccionario de equivalencias.
- Unir locales, licencias y terrazas por `id_local` para analizar la actividad comercial por tipo y zona.
- Publicar un dashboard en Power BI sobre los datos limpios.

---

**Autor:** Daniel Amaya Segura · [LinkedIn](https://www.linkedin.com/in/daniel-amaya-segura-6198504a/) · daniamaya77@gmail.com
