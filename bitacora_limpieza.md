# Bitácora de decisiones de limpieza

Registros de origen: **1250** · Registros limpios: **1200**

| Paso | Columna | Criterio / decisión | Filas afectadas |
|---|---|---|---|
| 1. Duplicados | (fila completa) | Se eliminan filas idénticas | 30 |
| 1. Duplicados | id_empleado | Mismo id con contenido distinto: se conserva el registro con menos nulos | 20 |
| 2. Tipos | salario_mensual | Texto con '$' y comas -> número (float) | 39 |
| 2. Tipos | fecha_ingreso | Formatos mixtos (aaaa-mm-dd y dd/mm/aaaa) -> datetime | 150 |
| 3. Categorías | ciudad | Mayúsculas/espacios/acentos -> etiqueta canónica del catálogo | 138 |
| 3. Categorías | departamento | Mayúsculas/espacios/acentos -> etiqueta canónica del catálogo | 140 |
| 3. Categorías | nivel_educativo | Mayúsculas/espacios/acentos -> etiqueta canónica del catálogo | 0 |
| 3. Categorías | genero | 'Femenino' -> 'F' (codificación única F/M) | 60 |
| 4. Rangos imposibles | edad | Edad laboral legal/razonable 18-70 -> se marca como nulo | 4 |
| 4. Rangos imposibles | horas_semanales | Jornada plausible 20-70 h/semana -> se marca como nulo | 6 |
| 4. Rangos imposibles | satisfaccion | Escala de la encuesta 1-10 -> se marca como nulo | 4 |
| 4. Rangos imposibles | salario_mensual | Piso plausible de 4,000 MXN (valores de 300-1,500 = error de captura) -> se marca como nulo | 5 |
| 5. Imputación | edad | Mediana por departamento (redondeada) | 28 |
| 4. Rangos imposibles | anios_experiencia | Fuera de 0-50 o mayor que (edad-16) -> nulo | 7 |
| 5. Imputación | nivel_educativo | Moda global (Licenciatura) | 72 |
| 5. Imputación | ciudad | Categoría explícita 'No especificada' (no se inventa ubicación) | 12 |
| 5. Imputación | evaluacion_desempeno | Mediana global (entera) | 48 |
| 5. Imputación | num_capacitaciones | Mediana global (entera) | 60 |
| 5. Imputación | horas_semanales | Mediana por departamento | 42 |
| 5. Imputación | satisfaccion | Mediana por evaluación de desempeño (variable relacionada) | 88 |
| 5. Imputación | anios_experiencia | Mediana por departamento | 67 |
| 5. Imputación | salario_mensual | Mediana por departamento x nivel educativo | 53 |
| 6. Coherencia | anios_experiencia | Tras imputar, se limita a (edad-16) | 11 |
| 7. Atípicos | salario_mensual | IQR x 1.5 por departamento; se topa (winsoriza) en la valla, sin eliminar filas | 51 |
| 8. Derivadas | rango_edad | Cortes 18-25/26-35/36-45/46-55/56-70 | 1200 |
| 8. Derivadas | antiguedad_anios | (fecha de corte 2025-06-30 - fecha_ingreso) / 365.25 | 1200 |
| 8. Derivadas | alta_satisfaccion | 1 si satisfaccion >= 8 | 1200 |
| 8. Derivadas | ratio_salario_depto | salario / mediana salarial del departamento | 1200 |
| 8. Derivadas | banda_salarial | Cortes fijos: <=15k Baja, <=22k Media, <=32k Alta, >32k Muy alta | 1200 |
