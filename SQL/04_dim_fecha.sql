CREATE TABLE dw.dim_fecha (
    fecha_key INTEGER PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    nombre_mes VARCHAR(20) NOT NULL,
    trimestre INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    nombre_dia VARCHAR(20) NOT NULL
);

INSERT INTO dw.dim_fecha (
    fecha_key,
    fecha,
    dia,
    mes,
    nombre_mes,
    trimestre,
    anio,
    dia_semana,
    nombre_dia
)
SELECT
    TO_CHAR(fecha, 'YYYYMMDD')::INTEGER,
    fecha,
    EXTRACT(DAY FROM fecha)::INTEGER,
    EXTRACT(MONTH FROM fecha)::INTEGER,
    TRIM(TO_CHAR(fecha, 'Month')),
    EXTRACT(QUARTER FROM fecha)::INTEGER,
    EXTRACT(YEAR FROM fecha)::INTEGER,
    EXTRACT(ISODOW FROM fecha)::INTEGER,
    TRIM(TO_CHAR(fecha, 'Day'))
FROM generate_series(
    DATE '2023-01-01',
    DATE '2025-12-31',
    INTERVAL '1 day'
) AS t(fecha);

SELECT COUNT(*) AS total_fechas
FROM dw.dim_fecha;
