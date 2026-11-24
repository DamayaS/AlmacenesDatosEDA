# 📚 books — Catálogo de libros técnicos (Manning Publications)

## Descripción general

| | |
|---|---|
| **Contenido** | Catálogo de libros de la editorial técnica Manning Publications |
| **Origen** | Exportación de una colección MongoDB (`mongoexport`, formato Extended JSON) |
| **Formato** | JSON Lines (un documento JSON por línea), UTF-8 |
| **Volumen** | 431 documentos · 11 campos |
| **Granularidad** | Un registro por libro (o edición / producto del catálogo) |
| **Clave** | `_id` |
| **Periodo cubierto** | Fechas de publicación entre 1993 y 2014 |
| **Preparación para la carga** | `_id` convertido a texto en todos los registros (en origen mezclaba enteros y objetos `{"$oid": ...}`). Ningún otro valor modificado. |

## Introducción

El dataset recoge el catálogo de libros de Manning, editorial especializada en programación y tecnología. Cada documento describe un título con su ISBN, número de páginas, fecha de publicación, estado editorial, autores, categorías temáticas, portada y descripciones.

El catálogo está claramente centrado en desarrollo de software: **Java** es la categoría dominante (97 títulos), seguida de **Internet** (42) y **Microsoft .NET** (34). El 42 % de los títulos pertenecen a la serie *«in Action»*. El 84 % de los libros están publicados (`PUBLISH`) y el resto en preventa (`MEAP`).

Al proceder de MongoDB, el esquema es flexible: no todos los documentos tienen todos los campos, y algunos campos son estructuras anidadas (`publishedDate`) o listas (`authors`, `categories`).

## Diccionario de campos

| Campo | Tipo | Descripción |
|---|---|---|
| `_id` | Texto | Identificador del documento en MongoDB. 399 registros tienen un id numérico (1–796, no consecutivo) y 32 un ObjectId de 24 caracteres hexadecimales. |
| `title` | Texto | Título del libro. |
| `isbn` | Texto | ISBN-10 (mayoritario) o ISBN-13 (4 casos). Ausente en 3 libros. |
| `pageCount` | Entero | Número de páginas. **El valor 0 significa "desconocido"**, no cero páginas. |
| `publishedDate` | Estructura `{ $date: texto }` | Fecha de publicación en formato ISO 8601 con zona horaria (`-0700` / `-0800`). Ausente en 78 libros (todos los MEAP y 10 publicados). |
| `thumbnailUrl` | Texto (URL) | URL de la imagen de portada (Amazon S3). Ausente en 20 libros. |
| `shortDescription` | Texto | Resumen breve del libro. A veces contiene citas de reseñas en lugar de un resumen. Ausente en 271 libros. |
| `longDescription` | Texto | Descripción extensa del libro. Ausente en 168 libros. |
| `status` | Texto (código) | Estado editorial. Ver tabla de códigos. |
| `authors` | Lista de texto | Autores del libro. Puede estar vacía (37 libros) o contener cadenas vacías. |
| `categories` | Lista de texto | Categorías temáticas. Vacía en 160 libros. |

### Códigos de `status`

| Valor | Significado | Registros |
|---|---|---|
| `PUBLISH` | Libro publicado | 363 |
| `MEAP` | *Manning Early Access Program*: libro en preventa, aún no publicado | 68 |

## Calidad del dato: advertencias conocidas

- **`pageCount = 0` en 166 libros (39 %).** Hay que tratarlo como nulo. Si no, la media de páginas cae de 470 a 289.
- **Registros duplicados.** *SQL Server MVP Deep Dives* aparece 3 veces, y *Jaguar Development with PowerBuilder 7* y *Android in Practice* 2 veces cada uno.
- **ISBN no válidos.** 18 ISBN tienen 9 dígitos (perdieron el 0 inicial) y 14 tienen sufijos artificiales `a-e` … `n-e` (módulos del *Jakarta Commons Online Bookshelf*). Cuatro ISBN están repetidos, dos de ellos en libros distintos.
- **Autores mal separados.** Hay nombres partidos (`Galina` + `Vlad Landres`, `Jr` o `II` como si fueran autores), varios autores en un mismo texto (`... with ...`, `... and ...`) y grafías distintas de una misma persona.
- **Categorías no normalizadas.** Hay 38 valores, con variantes de mayúsculas (`Java`/`java`), duplicados (`Microsoft .NET`/`Microsoft/.NET`) y valores truncados (`Miscella`, `S`, `P`).
- **Errores de contenido.** *SQR in PeopleSoft* tiene la descripción de *AspectJ in Action*, y la edición china de *Hibernate in Action* tiene fecha anterior a la original.
- **Texto.** 241 descripciones tienen espacios múltiples por caracteres perdidos en la codificación, y una contiene HTML.
- **Lote sin metadatos.** Los 32 registros con `_id` tipo ObjectId no tienen ni autores ni categorías.
- **Seguridad.** Las URL de `thumbnailUrl` incluyen un identificador con formato de clave de acceso de AWS. Conviene revisarlo antes de exponer el dataset.

## Notas de uso

- Para analizar autores o categorías, aplana las listas con `FLATTEN(authors)` o `FLATTEN(categories)`.
- La fecha se obtiene con `publishedDate['$date']`. Conviene quedarse solo con el día para evitar el desfase de zona horaria.
- No tiene relación con los datasets del Ayuntamiento de Madrid.
