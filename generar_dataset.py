"""Genera data/empleados_analitica.csv (dataset SINTÉTICO con problemas de calidad deliberados).
Semilla fija -> mismo archivo siempre. Uso: python data/generar_dataset.py"""
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
N = 1200

ciudades = ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Querétaro", "Mérida"]
p_ciudad = [0.34, 0.20, 0.20, 0.10, 0.10, 0.06]
deptos = ["Ventas", "Tecnología", "Operaciones", "Finanzas", "Recursos Humanos", "Marketing", "Logística"]
p_depto = [0.22, 0.20, 0.20, 0.09, 0.07, 0.10, 0.12]
base_sal = {"Ventas": 17000, "Tecnología": 30000, "Operaciones": 16000, "Finanzas": 24000,
            "Recursos Humanos": 19000, "Marketing": 20000, "Logística": 15000}
mult_ciudad = {"Ciudad de México": 1.15, "Guadalajara": 1.0, "Monterrey": 1.10,
               "Puebla": 0.92, "Querétaro": 1.02, "Mérida": 0.90}
educ = ["Preparatoria", "Licenciatura", "Maestría", "Doctorado"]
p_educ = [0.15, 0.62, 0.20, 0.03]

edad = np.clip(rng.normal(36, 9, N).round(), 20, 64).astype(int)
anios_exp = np.clip(edad - 22 - rng.integers(0, 6, N), 0, None) * rng.uniform(0.6, 1.0, N)
anios_exp = anios_exp.round(1)
ciudad = rng.choice(ciudades, N, p=p_ciudad)
depto = rng.choice(deptos, N, p=p_depto)
nivel = rng.choice(educ, N, p=p_educ)
bono_educ = {"Preparatoria": 0.85, "Licenciatura": 1.0, "Maestría": 1.18, "Doctorado": 1.35}
salario = np.array([base_sal[d] * mult_ciudad[c] * bono_educ[e] for d, c, e in zip(depto, ciudad, nivel)])
salario = salario * (1 + 0.025 * anios_exp) * rng.lognormal(0, 0.12, N)
salario = salario.round(2)
horas = np.clip(rng.normal(44, 5, N), 30, 60).round(1)
capac = rng.poisson(3, N)
desempeno = np.clip(np.round(rng.normal(3.4, 0.8, N)), 1, 5).astype(int)
satisf = np.clip(6.5 + 0.25 * (desempeno - 3) - 0.12 * (horas - 44) + rng.normal(0, 1.4, N), 1, 10).round(1)
dias = np.minimum((anios_exp * 365 * rng.uniform(0.3, 0.9, N)).astype(int) + rng.integers(30, 400, N), 365 * 15)
fecha_ing = pd.Timestamp("2025-06-30") - pd.to_timedelta(dias, unit="D")
logit = -1.2 - 0.55 * (satisf - 6.5) + 0.04 * (horas - 44) - 0.00004 * (salario - 22000)
abandono = (rng.uniform(size=N) < 1 / (1 + np.exp(-logit))).astype(int)

df = pd.DataFrame({
    "id_empleado": [f"E{1000 + i}" for i in range(N)],
    "edad": edad, "genero": rng.choice(["F", "M"], N, p=[0.47, 0.53]),
    "ciudad": ciudad, "departamento": depto, "nivel_educativo": nivel,
    "fecha_ingreso": fecha_ing, "anios_experiencia": anios_exp,
    "salario_mensual": salario, "horas_semanales": horas, "num_capacitaciones": capac,
    "evaluacion_desempeno": desempeno.astype(float), "satisfaccion": satisf, "abandono": abandono,
})

# ---------- Problemas de calidad deliberados ----------
df["edad"] = df["edad"].astype(float)
# 1) Formatos de fecha mixtos
df["fecha_ingreso"] = df["fecha_ingreso"].dt.strftime("%Y-%m-%d")
idx = rng.choice(N, 150, replace=False)
df.loc[idx, "fecha_ingreso"] = pd.to_datetime(df.loc[idx, "fecha_ingreso"]).dt.strftime("%d/%m/%Y")
# 2) Categorías inconsistentes
for col in ["departamento", "ciudad"]:
    idx = rng.choice(N, 140, replace=False)
    df.loc[idx, col] = [rng.choice([s.upper(), s.lower(), " " + s + " "]) for s in df.loc[idx, col]]
df.loc[rng.choice(N, 60, replace=False), "genero"] = "Femenino"
# 3) Salario como texto con símbolo en algunos registros
df["salario_mensual"] = df["salario_mensual"].astype(object)
idx = rng.choice(N, 40, replace=False)
df.loc[idx, "salario_mensual"] = ["$" + f"{float(v):,.2f}" for v in df.loc[idx, "salario_mensual"]]
# 4) Valores atípicos y errores de captura
df.loc[rng.choice(N, 8, replace=False), "salario_mensual"] = rng.uniform(150000, 400000, 8).round(2)
df.loc[rng.choice(N, 5, replace=False), "salario_mensual"] = rng.uniform(300, 1500, 5).round(2)
df.loc[rng.choice(N, 4, replace=False), "edad"] = [150, 999, 5, 17]
df.loc[rng.choice(N, 5, replace=False), "anios_experiencia"] = [-3, -1, 75, 60, 48]
df.loc[rng.choice(N, 6, replace=False), "horas_semanales"] = [0, 120, 99, 150, 5, 200]
df.loc[rng.choice(N, 4, replace=False), "satisfaccion"] = [0, 11, 15, 99]
# 5) Valores faltantes
for col, frac in {"satisfaccion": 0.07, "salario_mensual": 0.04, "anios_experiencia": 0.05,
                  "nivel_educativo": 0.06, "horas_semanales": 0.03, "num_capacitaciones": 0.05,
                  "evaluacion_desempeno": 0.04, "edad": 0.02, "ciudad": 0.01}.items():
    df.loc[rng.choice(N, int(N * frac), replace=False), col] = np.nan
# 6) Duplicados: exactos y por id (mismo empleado con un campo faltante)
exactos = df.sample(30, random_state=1)
por_id = df.sample(20, random_state=2).copy()
por_id["salario_mensual"] = np.nan
df = pd.concat([df, exactos, por_id], ignore_index=True).sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv(Path(__file__).with_name("empleados_analitica.csv"), index=False, encoding="utf-8")
print("Generado:", df.shape)
