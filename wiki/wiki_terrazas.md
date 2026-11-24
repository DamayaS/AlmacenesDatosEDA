# Terrazas_202104

## Descripción general

| | |
|---|---|
| **Contenido** | Terrazas de veladores autorizadas en la vía pública y en espacios privados del municipio de Madrid |
| **Origen** | Portal de Datos Abiertos del Ayuntamiento de Madrid (Censo de Locales y Actividades: terrazas) |
| **Fecha de corte** | Abril de 2021 |
| **Formato** | CSV, separador `;`, coma decimal. En origen estaba en **Latin-1 (ISO-8859-1)** y sin comillas; la versión cargada en Dremio está en UTF-8 y con todos los campos entre comillas. |
| **Volumen** | 6.275 registros · 57 campos |
| **Granularidad** | **Una fila por terraza**. Cada local tiene como máximo una terraza. |
| **Clave** | `id_terraza` (única). `id_local` también es único en este dataset. |
| **Periodo cubierto** | Fechas de resolución entre 2014 y 2021 |
| **Preparación para la carga** | Conversión de Latin-1 a UTF-8 y entrecomillado de todos los campos (un rótulo empezaba por comillas). Ningún valor modificado. |

## Introducción

El dataset recoge las terrazas de hostelería (bares, restaurantes, cafeterías) autorizadas por el Ayuntamiento. Para cada terraza incluye los datos del local al que pertenece (ubicación, dirección, situación, rótulo) y las condiciones de la autorización: periodo (anual o estacional), superficie, número de mesas y sillas, horarios y tipo de ubicación (acera, calle peatonal, zona de estacionamiento…).

Muchos campos aparecen duplicados con dos sufijos:
- **`_es` → periodo estacional**: la temporada de terrazas.
- **`_ra` → resto del año**: fuera de temporada. Vacíos en las terrazas que solo funcionan en temporada.

En los horarios, **`LJ`** significa de lunes a jueves y **`VS`** viernes y sábados.

Centro, Chamberí y Salamanca concentran más de un tercio de las terrazas. El 75 % son anuales. Una terraza típica (mediana) ocupa 25,6 m² con 8 mesas y 24 sillas, y el 70 % están en acera.

## Diccionario de campos

### Identificación

| Campo | Tipo | Descripción |
|---|---|---|
| `id_terraza` | Código | Identificador único de la terraza. |
| `id_local` | Código | Identificador del local al que pertenece la terraza. Clave de relación con `Locales_202104` y `Licencias_Locales_202104`. |

### Ubicación y dirección del local

| Campo | Tipo | Descripción |
|---|---|---|
| `id_distrito_local` | Código | Código del distrito (1–21). |
| `desc_distrito_local` | Texto | Nombre del distrito. |
| `id_barrio_local` | Código | Código del barrio (distrito + número de barrio). |
| `desc_barrio_local` | Texto | Nombre del barrio. |
| `id_ndp_edificio` | Código | Identificador del número de policía (dirección postal) del edificio del local. |
| `id_clase_ndp_edificio` | Código | Clase de número de policía. Valor constante (`1`). |
| `id_vial_edificio` | Código | Código de la vía del edificio. |
| `clase_vial_edificio` | Texto | Tipo de vía (CALLE, AVENIDA, PLAZA…). |
| `desc_vial_edificio` | Texto | Nombre de la vía. |
| `nom_edificio` | Código | Tipo de numeración. Valor constante (`NUM`). |
| `num_edificio` | Texto | Número de portal. |
| `Cod_Postal` | Código | Código postal del local (55 códigos, todos `280xx`). |
| `coordenada_x_local` | Decimal | Coordenada X del local (UTM ETRS89, huso 30N, en metros, coma decimal). **0 = sin dato.** |
| `coordenada_y_local` | Decimal | Coordenada Y del local. **0 = sin dato.** |
| `id_tipo_acceso_local` | Código | Tipo de acceso al local. Ver tabla de códigos. |
| `desc_tipo_acceso_local` | Texto | Descripción del tipo de acceso. |
| `id_situacion_local` | Código | Situación del local: `1` Abierto, `4` Cerrado, `9` Baja Reunificación. |
| `desc_situacion_local` | Texto | Descripción de la situación del local. |
| `secuencial_local_PC` | Entero | Número secuencial del local dentro de la misma puerta de calle. |
| `Escalera` | Texto | Escalera del local. Vacío en el 99,9 % de los casos. |
| `id_planta_agrupado` | Texto | Planta del local (casi siempre `PB`, planta baja). |
| `id_local_agrupado` | Texto | Identificador del local dentro de su agrupación, si la tiene. |
| `coordenada_x_agrupacion` | Decimal | Coordenada X de la agrupación, si la tiene. |
| `coordenada_y_agrupacion` | Decimal | Coordenada Y de la agrupación, si la tiene. |
| `rotulo` | Texto | Nombre comercial del local. |

### Autorización de la terraza

| Campo | Tipo | Descripción |
|---|---|---|
| `id_periodo_terraza` | Código | Periodo de funcionamiento: `1` Anual, `2` Estacional. |
| `desc_periodo_terraza` | Texto | Descripción del periodo. |
| `id_situacion_terraza` | Código | Situación de la terraza: `1` Abierta, `8` Suspensión temporal. |
| `desc_situacion_terraza` | Texto | Descripción de la situación. |
| `Superficie_ES` | Decimal (m²) | Superficie autorizada en el periodo estacional. |
| `Superficie_RA` | Decimal (m²) | Superficie autorizada en el resto del año. Vacía en terrazas solo estacionales. |
| `Fecha_confir_ult_decreto_resol` | Fecha (`dd/mm/aaaa`) | Fecha de confirmación del último decreto o resolución de la autorización. **`31/12/9999` = sin fecha.** |

### Dirección de la terraza

Ubicación de la terraza en la vía pública. Puede ser distinta de la del local, por ejemplo una terraza en la plaza de enfrente.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ndp_terraza` | Código | Identificador del número de policía donde se sitúa la terraza. |
| `id_clase_ndp_terraza` | Código | Clase de número de policía. Valor constante (`1`). |
| `ID_VIAL` | Código | Código de la vía donde se sitúa la terraza. |
| `DESC_CLASE` | Texto | Tipo de vía de la terraza. |
| `DESC_NOMBRE` | Texto | Nombre de la vía de la terraza. |
| `nom_terraza` | Código | Tipo de numeración. Valor constante (`NUM`). |
| `num_terraza` | Texto | Número de portal de referencia de la terraza. |
| `cal_terraza` | Texto | Calificador del número (A, B…). |
| `desc_ubicacion_terraza` | Texto | Tipo de espacio que ocupa la terraza. Ver tabla. |

### Horarios

Formato `hh:mm:ss`. Las horas de cierre posteriores a medianoche (01:00, 02:30…) corresponden a la madrugada del día siguiente.

| Campo | Descripción |
|---|---|
| `hora_ini_LJ_es` / `hora_fin_LJ_es` | Apertura y cierre de lunes a jueves, periodo estacional. |
| `hora_ini_LJ_ra` / `hora_fin_LJ_ra` | Apertura y cierre de lunes a jueves, resto del año. |
| `hora_ini_VS_es` / `hora_fin_VS_es` | Apertura y cierre viernes y sábados, periodo estacional. |
| `hora_ini_VS_ra` / `hora_fin_VS_ra` | Apertura y cierre viernes y sábados, resto del año. |

### Mobiliario

| Campo | Tipo | Descripción |
|---|---|---|
| `mesas_aux_es` | Entero | Mesas auxiliares autorizadas, periodo estacional. |
| `mesas_aux_ra` | Entero | Mesas auxiliares autorizadas, resto del año. |
| `mesas_es` | Entero | Mesas autorizadas, periodo estacional. |
| `mesas_ra` | Entero | Mesas autorizadas, resto del año. |
| `sillas_es` | Entero | Sillas autorizadas, periodo estacional. |
| `sillas_ra` | ⚠️ Texto | **Dato corrupto en origen.** Debería contener las sillas del resto del año, pero contiene letras (A, B, C…) que coinciden con `cal_terraza` en el 95 % de las filas. **No usar.** |

## Tablas de códigos

**Tipo de acceso (`id_tipo_acceso_local`)**

| Código | Descripción | Registros |
|---|---|---|
| 0 | Agrupado | 92 |
| 1 | Puerta Calle | 6.158 |
| 3 | Interior | 17 |
| 4 | Situado Aislado | 2 |
| 9 | Edificio | 4 |
| 12 | PC Asociado | 2 |

**Ubicación de la terraza (`desc_ubicacion_terraza`)**

| Valor | Registros |
|---|---|
| Acera | 4.416 |
| Zona de estacionamiento | 516 |
| Calle peatonal | 362 |
| Plaza peatonal | 344 |
| Otros | 260 |
| Superficie en parcela privada | 187 |
| Bulevar | 109 |
| Plaza con bandas permanentes de circulación rodada | 76 |
| Calle sin salida | 5 |

## Calidad del dato: advertencias conocidas

- **`sillas_ra` perdida.** Error estructural de la exportación: no es posible calcular el aforo fuera de temporada.
- **Fechas ficticias.** 6 terrazas con fecha `31/12/9999`.
- **Valores atípicos imposibles.** Una terraza declara 715 mesas y 0 sillas en 12 m² (rótulo `ROTULO SIN INFORMAR`). Hay 92 terrazas con 0 mesas y 13 con menos sillas que mesas.
- **Coordenadas a 0.** 101 terrazas (1,6 %).
- **Incoherencias de estado.** 71 terrazas abiertas pertenecen a locales cerrados o dados de baja.
- **Incoherencias de periodo.** 97 terrazas estacionales tienen datos de resto del año, y 43 tienen superficie fuera de temporada pero no número de mesas.
- **Horarios sospechosos.** 47 cierres a las 12:00 fuera de temporada (probablemente 00:00), aperturas a las 0:00 y horas como 10:24 o 00:24.
- **Rótulos sin nombre.** Más de 60 terrazas con variantes de "no informado" (`RÓTULO NO INFORMADO`, `ROTULO SIN INFORMAR`, `SR`), 4 con codificación corrupta.
- **Columnas sin información.** `id_clase_ndp_edificio`, `id_clase_ndp_terraza`, `nom_edificio` y `nom_terraza` son constantes; `Escalera` está casi vacía.
- **Nombres de columnas inconsistentes.** `ID_VIAL`, `DESC_CLASE` y `DESC_NOMBRE` en mayúsculas, y `Cod_Postal`, `Superficie_ES` con mayúscula inicial.

## Relación con otros datasets

- **`Locales_202104`**: relación 1:1 por `id_local`. 23 terrazas no tienen su local en el censo, y 12 tienen una situación del local distinta de la que figura en el censo.
- **`Licencias_Locales_202104`**: relación por `id_local` con las licencias del local.
