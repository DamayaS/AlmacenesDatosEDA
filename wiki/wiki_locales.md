# Locales_202104

## Descripción general

| | |
|---|---|
| **Contenido** | Censo de todos los locales (comerciales, de oficinas, garajes, etc.) del municipio de Madrid |
| **Origen** | Portal de Datos Abiertos del Ayuntamiento de Madrid (Censo de Locales y Actividades) |
| **Fecha de corte** | Abril de 2021 |
| **Formato** | CSV, separador `;`, todos los campos entre comillas, coma decimal. En origen estaba en **Latin-1 (ISO-8859-1)**; la versión cargada en Dremio está en UTF-8. |
| **Volumen** | 148.216 registros · 40 campos |
| **Granularidad** | **Una fila por local**, sin duplicados |
| **Clave** | `id_local` (único) |
| **Preparación para la carga** | Conversión de Latin-1 a UTF-8, comillas internas escapadas según el estándar CSV y 2 saltos de línea dentro de rótulos sustituidos por un espacio. Ningún otro valor modificado (se conservan los espacios de relleno). |

## Introducción

Es el censo municipal de locales: cada fila es un espacio físico con acceso propio (o dentro de una agrupación) en el que puede desarrollarse una actividad. Para cada local se registra su ubicación administrativa (distrito, barrio, sección censal), su dirección postal (la del edificio y la del acceso), sus coordenadas, su situación (abierto, cerrado, uso vivienda, baja…), su rótulo y, si procede, la agrupación a la que pertenece.

Es el **dataset maestro** de los tres del Ayuntamiento: licencias y terrazas se relacionan con él por `id_local`. El 69 % de los locales están abiertos y el 22,5 % cerrados. **Centro**, **Carabanchel** y **Ciudad Lineal** son los distritos con más locales. El 9,6 % de los locales están en una agrupación; la mayor es el Centro Comercial La Vaguada, con 300 locales. **El 52 % de los locales (77.679) no tiene ninguna licencia** en el dataset de licencias.

## Diccionario de campos

### Identificación y ubicación administrativa

| Campo | Tipo | Descripción |
|---|---|---|
| `id_local` | Código | Identificador único del local en el censo. Clave de relación con licencias y terrazas. |
| `id_distrito_local` | Código | Código del distrito municipal (1–21). |
| `desc_distrito_local` | Texto | Nombre del distrito. |
| `id_barrio_local` | Código | Código del barrio: código de distrito + número de barrio. |
| `desc_barrio_local` | Texto | Nombre del barrio (131 barrios). |
| `cod_barrio_local` | Código | ⚠️ **Vacío en todo el dataset.** |
| `id_seccion_censal_local` | Código | ⚠️ **Vacío en todo el dataset.** |
| `desc_seccion_censal_local` | Código | Número de la sección censal dentro del distrito. |
| `coordenada_x_local` | Decimal | Coordenada X del local (UTM ETRS89, huso 30N, en metros, coma decimal). **0 = sin dato.** |
| `coordenada_y_local` | Decimal | Coordenada Y del local (UTM ETRS89, huso 30N, en metros, coma decimal). **0 = sin dato.** |
| `id_tipo_acceso_local` | Código | ⚠️ **Vacío en todo el dataset.** Usar `desc_tipo_acceso_local`. |
| `desc_tipo_acceso_local` | Texto | Tipo de acceso: `Puerta Calle`, `Agrupado` o `PC Asociado`. |
| `id_situacion_local` | Código | Situación del local. Ver tabla de códigos. |
| `desc_situacion_local` | Texto | Descripción de la situación del local. |

### Dirección del edificio

| Campo | Tipo | Descripción |
|---|---|---|
| `id_vial_edificio` | Código | ⚠️ **Vacío en todo el dataset.** |
| `clase_vial_edificio` | Texto | Tipo de vía (CALLE, AVENIDA, PLAZA, PASEO…). |
| `desc_vial_edificio` | Texto | Nombre de la vía. |
| `id_ndp_edificio` | Código | Identificador del número de policía (dirección postal) del edificio. |
| `id_clase_ndp_edificio` | Código | Clase de número de policía. Valor constante (`1`). |
| `nom_edificio` | Código | Tipo de numeración: `NUM` (número de portal) o `KM.` (punto kilométrico). |
| `num_edificio` | Texto | Número de portal o punto kilométrico. |
| `cal_edificio` | Texto | Calificador del número (A, B, C…). Vacío en el 95 % de los casos. |
| `secuencial_local_PC` | Entero | Número secuencial del local dentro de la misma puerta de calle (10, 20, 30…). |

### Dirección del acceso

| Campo | Tipo | Descripción |
|---|---|---|
| `id_vial_acceso` | Código | ⚠️ **Vacío en todo el dataset.** |
| `clase_vial_acceso` | Texto | Tipo de vía de acceso. |
| `desc_vial_acceso` | Texto | Nombre de la vía de acceso. |
| `id_ndp_acceso` | Código | Identificador del número de policía del acceso. |
| `id_clase_ndp_acceso` | Código | Clase de número de policía del acceso. Valor constante (`1`). |
| `nom_acceso` | Código | Tipo de numeración del acceso (`NUM` / `KM.`). |
| `num_acceso` | Texto | Número del acceso. |
| `cal_acceso` | Texto | Calificador del número del acceso. |

### Agrupación y rótulo

| Campo | Tipo | Descripción |
|---|---|---|
| `coordenada_x_agrupacion` | Decimal | Coordenada X de la agrupación (UTM ETRS89 30N). Vacía si el local no está agrupado; 0 = sin dato. |
| `coordenada_y_agrup` | Decimal | Coordenada Y de la agrupación. Mismo criterio. *(En otros datasets se llama `coordenada_y_agrupacion`.)* |
| `id_agrupacion` | Código | Identificador de la agrupación. Vacío si no aplica. |
| `nombre_agrupacion` | Texto | Nombre de la agrupación (p. ej. `MERCADO MUNICIPAL MARAVILLAS`). |
| `id_tipo_agrup` | Código | Tipo de agrupación. Ver tabla de códigos. |
| `desc_tipo_agrup` | Texto | Descripción del tipo de agrupación. |
| `id_planta_agrupado` | Texto | Planta del local (`PB` = planta baja, `1`, `2`…, `SO` = sótano, `SS` = semisótano, `-1`…). Formato heterogéneo. |
| `id_local_agrupado` | Texto | Identificador del local dentro de la agrupación (p. ej. número de puesto). |
| `rotulo` | Texto | Nombre comercial del local. `SIN ACTIVIDAD` indica un local sin actividad, no un nombre. |

## Tablas de códigos

**Situación del local (`id_situacion_local`)**

| Código | Descripción | Registros |
|---|---|---|
| 1 | Abierto | 102.442 |
| 4 | Cerrado | 33.358 |
| 5 | Uso vivienda | 6.351 |
| 7 | En obras | 752 |
| 8 | Baja | 2.248 |
| 9 | Baja Reunificación | 3.049 |
| 10 | Baja PC Asociado | 16 |

**Tipo de agrupación (`id_tipo_agrup`)**

| Código | Descripción | Registros |
|---|---|---|
| 1 | Centro Comercial | 4.001 |
| 4 | Galería de Alimentación | 3.766 |
| 7 | Intercambiador de transportes | 286 |
| 8 | Estación de tren | 191 |
| 9 | Estación de metro | 22 |
| 10 | Aeropuerto | 238 |
| 12 | Mercado Municipal | 3.479 |
| 13 | Pasaje comercial | 558 |
| 15 | Agrupación no comercial | 691 |
| 16 | Recinto ferial | 92 |
| 17 | Mercamadrid | 895 |
| *(vacío)* | Sin agrupación | 133.997 |

## Calidad del dato: advertencias conocidas

- **Cinco columnas totalmente vacías.** `cod_barrio_local`, `id_seccion_censal_local`, `id_tipo_acceso_local`, `id_vial_edificio` e `id_vial_acceso` no tienen ningún valor (en `Licencias_Locales_202104` sí lo tienen). Es un fallo de la exportación de origen.
- **Columnas constantes.** `id_clase_ndp_edificio` e `id_clase_ndp_acceso`.
- **Coordenadas a 0.** 9.863 locales (6,7 %), de ellos 6.032 abiertos, y 1.074 coordenadas de agrupación.
- **Rótulos que no son nombres.** `SIN ACTIVIDAD` (40.752), y variantes de "sin dato": `SR` (2.306), `ROTULO NO INFORMADO` (1.822), `R0TULO NO INFORMADO` escrito con un cero (1.647), `SIN ROTULO`, `NO INFORMADO`, `S/R`.
- **Contradicciones.** 1.819 locales figuran como `Abierto` con rótulo `SIN ACTIVIDAD`.
- **Codificación.** 24 rótulos con caracteres corruptos (`PÃ‚TISSERIE`).
- **Espacios de relleno.** Los campos de texto tienen longitud fija; hay que aplicar `TRIM`.
- **Plantas.** Formatos inconsistentes (`1`/`01`, `0`/`PB`, `-1`/`- 1`) y 2.483 locales sin planta.
- **Agrupaciones.** 5 nombres de agrupación tienen más de un identificador.

## Relación con otros datasets

- **`Licencias_Locales_202104`**: relación 1:N por `id_local`. 70.537 locales tienen al menos una licencia; 77.679 no tienen ninguna.
- **`Terrazas_202104`**: relación 1:0..1 por `id_local`. 23 terrazas tienen un `id_local` que no existe en este censo.
- Diferencias de esquema con licencias: cambian el orden y algunos nombres de columnas, y aquí las descripciones no llevan tildes (`Baja Reunificacion`, `Galeria de Alimentacion`).
