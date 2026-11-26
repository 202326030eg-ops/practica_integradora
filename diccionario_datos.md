# Diccionario de datos — `empleados`

| Variable | Tipo | Descripción | Valores / rango | Notas de calidad |
|---|---|---|---|---|
| id_empleado | TEXT (PK) | Identificador único del empleado | E1000-E2199 | Duplicados por id resueltos conservando el registro más completo. |
| edad | INTEGER | Edad en años cumplidos | 18-70 | Valores imposibles (5, 17, 150, 999) -> nulo -> mediana por departamento. |
| genero | TEXT | Género registrado | F, M | 'Femenino' unificado a 'F'. |
| ciudad | TEXT (FK) | Ciudad de la sede | Ciudad de México, Guadalajara, Monterrey, Puebla, Querétaro, Mérida, No especificada | Formato normalizado; nulos -> 'No especificada'. |
| departamento | TEXT (FK) | Departamento al que pertenece | Ventas, Tecnología, Operaciones, Finanzas, Recursos Humanos, Marketing, Logística | Formato normalizado (mayúsculas/espacios). |
| nivel_educativo | TEXT | Máximo nivel de estudios | Preparatoria, Licenciatura, Maestría, Doctorado | Nulos imputados con la moda. |
| fecha_ingreso | TEXT (ISO aaaa-mm-dd) | Fecha de ingreso a la organización | 2010-2025 | Dos formatos de origen unificados. |
| anios_experiencia | REAL | Años de experiencia laboral total | 0 - (edad-16), máx. 50 | Negativos y > edad-16 -> nulo -> mediana por departamento. |
| salario_mensual | REAL | Salario mensual bruto en MXN | > 4,000 (acotado por IQR por departamento) | Texto con '$' convertido; <4,000 -> imputado; extremos topados por IQR. |
| horas_semanales | REAL | Horas trabajadas por semana | 20-70 | Valores 0, 5, 99, 120, 150, 200 -> imputados por mediana de departamento. |
| num_capacitaciones | INTEGER | Cursos de capacitación en el último año | >= 0 | Nulos -> mediana global. |
| evaluacion_desempeno | INTEGER | Evaluación de desempeño | 1-5 | Nulos -> mediana global. |
| satisfaccion | REAL | Satisfacción laboral (encuesta) | 1-10 | Valores 0, 11, 15, 99 -> nulo; imputada por mediana según desempeño. |
| abandono | INTEGER | 1 si el empleado dejó la organización, 0 si continúa | 0, 1 | Variable objetivo candidata para el Entregable 3. Sin nulos en origen. |
| rango_edad | TEXT | DERIVADA: grupo etario | 18-25, 26-35, 36-45, 46-55, 56-70 | Calculada tras limpiar edad. |
| antiguedad_anios | REAL | DERIVADA: años en la organización a la fecha de corte 2025-06-30 | >= 0 | Fecha de corte fija para reproducibilidad. |
| alta_satisfaccion | INTEGER | DERIVADA: 1 si satisfaccion >= 8 | 0, 1 | Indicador binario. |
| ratio_salario_depto | REAL | DERIVADA: salario / mediana salarial de su departamento | > 0 (1 = en la mediana) | Permite comparar entre departamentos. |
| banda_salarial | TEXT | DERIVADA: banda por cortes fijos de salario | Baja, Media, Alta, Muy alta | Cortes: 15k / 22k / 32k. |
| salario_imputado | INTEGER | MARCA: salario imputado (faltante o inválido) | 0, 1 | Útil para análisis de sensibilidad. |
| experiencia_imputada | INTEGER | MARCA: experiencia imputada | 0, 1 |  |
| satisfaccion_imputada | INTEGER | MARCA: satisfacción imputada | 0, 1 |  |
| salario_ajustado | INTEGER | MARCA: salario topado por la regla IQR | 0, 1 | Salario original extremo no se conserva; ver bitácora. |
