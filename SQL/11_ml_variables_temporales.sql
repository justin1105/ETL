DROP VIEW IF EXISTS dw.vw_ml_demanda_features;

CREATE VIEW dw.vw_ml_demanda_features AS

SELECT
    producto_key,
    codigo_producto,
    categoria,
    marca,

    fecha_mes,
    anio,
    mes,
    trimestre,

    -- Datos del mes actual
    demanda,
    unidades_atendidas,
    dna,
    quiebre,
    unidades_vendidas,
    stock_inicial,
    stock_final,
    nivel_inventario,
    rotacion,

    -- Demanda de meses anteriores
    LAG(demanda, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS demanda_lag_1,

    LAG(demanda, 2) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS demanda_lag_2,

    LAG(demanda, 3) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS demanda_lag_3,

    -- Promedios móviles
    ROUND(
        AVG(demanda) OVER (
            PARTITION BY producto_key
            ORDER BY fecha_mes
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS promedio_demanda_3m,

    ROUND(
        AVG(demanda) OVER (
            PARTITION BY producto_key
            ORDER BY fecha_mes
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS promedio_demanda_6m,

    -- Comportamiento anterior
    LAG(unidades_vendidas, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS ventas_lag_1,

    LAG(stock_final, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS stock_final_lag_1,

    LAG(quiebre, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS quiebre_lag_1,

    LAG(rotacion, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS rotacion_lag_1,

    -- VARIABLE OBJETIVO
    LEAD(demanda, 1) OVER (
        PARTITION BY producto_key
        ORDER BY fecha_mes
    ) AS demanda_siguiente_mes

FROM dw.vw_ml_demanda_base;