-- Esquema relacional (SQLite) — Entregable 1
-- Modelo: 2 catálogos (ciudades, departamentos) + tabla de hechos (empleados).
-- Re-ejecutable: elimina y recrea los objetos.
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS vw_empleados;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS departamentos;
DROP TABLE IF EXISTS ciudades;

CREATE TABLE ciudades (
    id_ciudad INTEGER PRIMARY KEY,
    nombre    TEXT NOT NULL UNIQUE
);

CREATE TABLE departamentos (
    id_departamento INTEGER PRIMARY KEY,
    nombre          TEXT NOT NULL UNIQUE
);

CREATE TABLE empleados (
    id_empleado          TEXT    PRIMARY KEY,
    edad                 INTEGER NOT NULL CHECK (edad BETWEEN 18 AND 70),
    genero               TEXT    NOT NULL CHECK (genero IN ('F', 'M')),
    id_ciudad            INTEGER NOT NULL REFERENCES ciudades(id_ciudad),
    id_departamento      INTEGER NOT NULL REFERENCES departamentos(id_departamento),
    nivel_educativo      TEXT    NOT NULL CHECK (nivel_educativo IN ('Preparatoria','Licenciatura','Maestría','Doctorado')),
    fecha_ingreso        TEXT    NOT NULL CHECK (fecha_ingreso GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    anios_experiencia    REAL    NOT NULL CHECK (anios_experiencia BETWEEN 0 AND 50),
    salario_mensual      REAL    NOT NULL CHECK (salario_mensual > 0),
    horas_semanales      REAL    NOT NULL CHECK (horas_semanales BETWEEN 20 AND 70),
    num_capacitaciones   INTEGER NOT NULL CHECK (num_capacitaciones >= 0),
    evaluacion_desempeno INTEGER NOT NULL CHECK (evaluacion_desempeno BETWEEN 1 AND 5),
    satisfaccion         REAL    NOT NULL CHECK (satisfaccion BETWEEN 1 AND 10),
    abandono             INTEGER NOT NULL CHECK (abandono IN (0, 1)),
    -- Variables derivadas
    rango_edad           TEXT    NOT NULL,
    antiguedad_anios     REAL    NOT NULL CHECK (antiguedad_anios >= 0),
    alta_satisfaccion    INTEGER NOT NULL CHECK (alta_satisfaccion IN (0, 1)),
    ratio_salario_depto  REAL    NOT NULL CHECK (ratio_salario_depto > 0),
    banda_salarial       TEXT    NOT NULL,
    -- Marcas de calidad (trazabilidad de la limpieza)
    salario_imputado       INTEGER NOT NULL DEFAULT 0 CHECK (salario_imputado IN (0, 1)),
    experiencia_imputada   INTEGER NOT NULL DEFAULT 0 CHECK (experiencia_imputada IN (0, 1)),
    satisfaccion_imputada  INTEGER NOT NULL DEFAULT 0 CHECK (satisfaccion_imputada IN (0, 1)),
    salario_ajustado       INTEGER NOT NULL DEFAULT 0 CHECK (salario_ajustado IN (0, 1))
);

CREATE INDEX idx_emp_departamento        ON empleados(id_departamento);
CREATE INDEX idx_emp_ciudad              ON empleados(id_ciudad);
CREATE INDEX idx_emp_departamento_ciudad ON empleados(id_departamento, id_ciudad);
CREATE INDEX idx_emp_abandono            ON empleados(abandono);

CREATE VIEW vw_empleados AS
SELECT e.*, c.nombre AS ciudad, d.nombre AS departamento
FROM empleados e
JOIN ciudades c      ON c.id_ciudad = e.id_ciudad
JOIN departamentos d ON d.id_departamento = e.id_departamento;
