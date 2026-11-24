# Licencias_Locales_202104

## Descripción general

| | |
|---|---|
| **Contenido** | Licencias urbanísticas y declaraciones responsables asociadas a los locales del municipio de Madrid |
| **Origen** | Portal de Datos Abiertos del Ayuntamiento de Madrid (Censo de Locales y Actividades) |
| **Fecha de corte** | Abril de 2021 |
| **Formato** | CSV, separador `;`, todos los campos entre comillas, UTF-8, coma decimal |
| **Volumen** | 132.171 registros · 46 campos |
| **Granularidad** | **Una fila por licencia**. Un mismo local puede tener varias licencias (hasta 53). |
| **Clave** | `ref_licencia` + `id_local` (`ref_licencia` sola no es única) |
| **Periodo cubierto** | Fechas de licencia hasta el 30/04/2021 |
| **Preparación para la carga** | Comillas internas escapadas según el estándar CSV y 2 saltos de línea dentro de rótulos sustituidos por un espacio. Ningún otro valor modificado (se conservan los espacios de relleno). |

## Introducción

El dataset registra los títulos habilitantes que permiten ejercer una actividad en un local de Madrid: licencias urbanísticas, licencias de funcionamiento, declaraciones responsables y transmisiones de licencia (cambios de titular). Cada licencia está vinculada a un local del censo y hereda su ubicación: distrito, barrio, sección censal, dirección postal, coordenadas y, si procede, la agrupación comercial a la que pertenece (centro comercial, mercado, galería…).

Cubre 70.537 locales distintos. Predominan las **declaraciones responsables** (36 %), seguidas de las **transmisiones de licencia** (33 %) y las **licencias urbanísticas** (22 %). El volumen anual crece desde 2007, se estabiliza en unas 13.000 licencias al año entre 2015 y 2019, y cae a la mitad en 2020. **Centro** es el distrito con más licencias (15.810).

## Diccionario de campos

### Identificación y ubicación administrativa del local

| Campo | Tipo | Descripción |
|---|---|---|
| `id_local` | Código | Identificador del local en el Censo de Locales. Se repite cuando un local tiene varias licencias. Clave para relacionarlo con `Locales_202104` y `Terrazas_202104`. |
| `id_distrito_local` | Código | Código del distrito municipal (1–21). |
| `desc_distrito_local` | Texto | Nombre del distrito. |
| `id_barrio_local` | Código | Código del barrio: código de distrito + número de barrio (p. ej. `103` = distrito 1, barrio 3). |
| `desc_barrio_local` | Texto | Nombre del barrio (131 barrios). |
| `cod_barrio_local` | Código | Número del barrio dentro de su distrito (1–9). |
| `id_seccion_censal_local` | Código | Código completo de la sección censal (distrito + sección). |
| `desc_seccion_censal_local` | Código | Número de la sección censal dentro del distrito. |
| `coordenada_x_local` | Decimal | Coordenada X del local (UTM ETRS89, huso 30N, en metros, coma decimal). **0 = sin dato.** |
| `coordenada_y_local` | Decimal | Coordenada Y del local (UTM ETRS89, huso 30N, en metros, coma decimal). **0 = sin dato.** |
| `id_tipo_acceso_local` | Código | Tipo de acceso al local. Ver tabla de códigos. |
| `desc_tipo_acceso_local` | Texto | Descripción del tipo de acceso. |
| `id_situacion_local` | Código | Situación del local en el censo. Ver tabla de códigos. |
| `desc_situacion_local` | Texto | Descripción de la situación del local. |

### Dirección del edificio

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ndp_edificio` | Código | Identificador del número de policía (dirección postal) del edificio. |
| `id_clase_ndp_edificio` | Código | Clase de número de policía. Valor constante (`1`). |
| `id_vial_edificio` | Código | Código de la vía del edificio en el callejero municipal. |
| `clase_vial_edificio` | Texto | Tipo de vía (CALLE, AVENIDA, PLAZA, PASEO…). |
| `desc_vial_edificio` | Texto | Nombre de la vía. |
| `nom_edificio` | Código | Tipo de numeración: `NUM` (número de portal) o `KM.` (punto kilométrico). |
| `num_edificio` | Texto | Número de portal o punto kilométrico. |
| `cal_edificio` | Texto | Calificador del número (A, B, C…). Vacío en la mayoría de los casos. |
| `secuencial_local_PC` | Entero | Número secuencial del local dentro de la misma puerta de calle (10, 20, 30…). |

### Dirección del acceso

Dirección por la que se accede al local. Puede ser distinta de la del edificio, por ejemplo en locales en esquina.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ndp_acceso` | Código | Identificador del número de policía del acceso. |
| `id_clase_ndp_acceso` | Código | Clase de número de policía del acceso. Valor constante (`1`). |
| `id_vial_acceso` | Código | Código de la vía de acceso. |
| `clase_vial_acceso` | Texto | Tipo de vía de acceso. |
| `desc_vial_acceso` | Texto | Nombre de la vía de acceso. |
| `nom_acceso` | Código | Tipo de numeración del acceso (`NUM` / `KM.`). |
| `num_acceso` | Texto | Número del acceso. |
| `cal_acceso` | Texto | Calificador del número del acceso. |

### Agrupación

Solo aplica a locales situados dentro de un centro comercial, mercado, galería, etc.

| Campo | Tipo | Descripción |
|---|---|---|
| `coordenada_x_agrupacion` | Decimal | Coordenada X de la agrupación (UTM ETRS89 30N). Vacía si el local no está agrupado. |
| `coordenada_y_agrupacion` | Decimal | Coordenada Y de la agrupación. Vacía si el local no está agrupado. |
| `id_agrupacion` | Código | Identificador de la agrupación. `-1` = sin agrupación. |
| `nombre_agrupacion` | Texto | Nombre de la agrupación (p. ej. `CENTRO COMERCIAL LA VAGUADA`). `SIN AGRUPACION` si no aplica. |
| `id_tipo_agrup` | Código | Tipo de agrupación. Ver tabla de códigos. |
| `desc_tipo_agrup` | Texto | Descripción del tipo de agrupación. |
| `id_planta_agrupado` | Texto | Planta en la que está el local (`PB` = planta baja, `1`, `2`…, `SO` = sótano, `SS` = semisótano, `-1`…). Formato heterogéneo. |
| `id_local_agrupado` | Texto | Identificador del local dentro de la agrupación (p. ej. número de puesto en un mercado). |
| `rotulo` | Texto | Nombre comercial que aparece en el rótulo del local. |

### Licencia

| Campo | Tipo | Descripción |
|---|---|---|
| `ref_licencia` | Texto | Referencia del expediente de la licencia, con formato `órgano/año/número` (p. ej. `500/2014/02133`). |
| `id_tipo_licencia` | Código | Tipo de licencia. Ver tabla de códigos. |
| `desc_tipo_licencia` | Texto | Descripción del tipo de licencia. |
| `id_tipo_situacion_licencia` | Código | Estado de tramitación de la licencia. Ver tabla de códigos. |
| `desc_tipo_situacion_licencia` | Texto | Descripción del estado de la licencia. |
| `Fecha_Dec_Lic` | Fecha (`dd/mm/aaaa`) | Fecha de la declaración o concesión de la licencia. **`01/01/1900` = sin fecha.** |

## Tablas de códigos

**Tipo de licencia (`id_tipo_licencia`)**

| Código | Descripción | Registros |
|---|---|---|
| 0 | Licencia recogida en el trabajo de campo | 6.145 |
| 1 | Declaración Responsable | 47.758 |
| 2 | Licencia Urbanística | 29.527 |
| 3 | Licencia de Funcionamiento | 5.012 |
| 4 | Transmisión de licencia Urbanística | 43.729 |

**Situación de la licencia (`id_tipo_situacion_licencia`)**

| Código | Descripción | Registros |
|---|---|---|
| -1 | VALOR NULO EN ORIGEN | 6.176 |
| 01 | En tramitación | 43.013 |
| 02 | Concedida | 41.836 |
| 03 | Denegada | 11.010 |
| 04 | Tramitando Transmisión de Licencia | 22.173 |
| 05 | Transmisión de Licencia Concedida | 7.579 |
| 06 | Transmisión de Licencia Denegada | 384 |

**Situación del local (`id_situacion_local`)**

| Código | Descripción | Registros |
|---|---|---|
| 1 | Abierto | 127.639 |
| 4 | Cerrado | 3.344 |
| 5 | Uso vivienda | 50 |
| 7 | En obras | 43 |
| 8 | Baja | 189 |
| 9 | Baja Reunificación | 905 |
| 10 | Baja PC Asociado | 1 |

**Tipo de acceso (`id_tipo_acceso_local`)**

| Código | Descripción | Registros |
|---|---|---|
| 0 | Agrupado | 8.174 |
| 1 | Puerta Calle | 123.722 |
| 12 | PC Asociado | 275 |

**Tipo de agrupación (`id_tipo_agrup`)**

| Código | Descripción | Código | Descripción |
|---|---|---|---|
| -1 | Sin agrupación | 10 | Aeropuerto |
| 1 | Centro Comercial | 12 | Mercado Municipal |
| 4 | Galería de Alimentación | 13 | Pasaje comercial |
| 7 | Intercambiador de transportes | 15 | Agrupación no comercial |
| 8 | Estación de tren | 16 | Recinto ferial |
| | | 17 | Mercamadrid |

## Calidad del dato: advertencias conocidas

- **Fechas ficticias.** 11.903 licencias (9 %) tienen fecha `01/01/1900`, entre ellas todas las *recogidas en el trabajo de campo*. Deben tratarse como nulas.
- **Coordenadas a 0.** 4.495 registros tienen X = Y = 0 (sin ubicación).
- **Nulos codificados como texto.** `VALOR NULO EN ORIGEN` (6.176), `RÓTULO NO INFORMADO` y `ROTULO NO INFORMADO` (5.429), y `SR` (sin rótulo, 1.162).
- **Espacios de relleno.** Los campos de texto tienen longitud fija (p. ej. `"CENTRO              "`). Hay que aplicar `TRIM` antes de agrupar o cruzar datos.
- **Codificación.** 95 rótulos tienen caracteres corruptos (`RÃ³TULO NO INFORMADO`).
- **Valores no normalizados.** Hay variantes con y sin tilde (`ALIMENTACION`/`ALIMENTACIÓN`) y plantas con formatos distintos (`1`/`01`, `-1`/`- 1`).
- **`ref_licencia` repetida en locales distintos.** Ocurre en 991 casos.
- **Columnas constantes.** `id_clase_ndp_edificio` e `id_clase_ndp_acceso` no aportan información.

## Relación con otros datasets

- **`Locales_202104`**: relación N:1 por `id_local`. Los 70.537 locales con licencia existen en el censo de locales.
- **`Terrazas_202104`**: relación por `id_local` (solo los locales que tienen terraza).
- Diferencias de esquema con `Locales_202104`: cambian el orden de las columnas y algunos nombres (`coordenada_y_agrupacion` frente a `coordenada_y_agrup`), y las descripciones tienen tildes aquí y no en el otro dataset.
