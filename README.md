# Práctica integradora — Analítica de la fuerza laboral

Sistema de analítica de extremo a extremo (limpieza → BD → exploración → modelo → app).
**Estado:** Entregable 1 completo.

## Estructura
```
data/        empleados_analitica.csv (crudo) · empleados_limpio.csv · empleados.db · generar_dataset.py
notebooks/   01_limpieza_y_bd.ipynb
sql/         schema.sql
docs/        diccionario_datos.md · bitacora_limpieza.md
models/  app/   (Entregables 3 y 4)
```

## Regenerar todo (Entregable 1)
```bash
pip install pandas numpy jupyter
python data/generar_dataset.py          # solo si no tienes el CSV original (genera uno sintético, semilla 42)
cd notebooks && jupyter nbconvert --to notebook --execute 01_limpieza_y_bd.ipynb --inplace
```
Ejecutar el notebook en orden reconstruye `data/empleados_limpio.csv`, `data/empleados.db`
y los documentos de `docs/`. Verificación: la huella SHA-256 del CSV limpio impresa al final
(`d2cb8276ceb620e0`) debe coincidir en cada ejecución.

## Consulta rápida
```bash
sqlite3 data/empleados.db "SELECT departamento, COUNT(*), ROUND(AVG(salario_mensual)) FROM vw_empleados GROUP BY 1;"
```
