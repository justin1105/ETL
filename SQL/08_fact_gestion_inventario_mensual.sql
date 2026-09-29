DROP TABLE IF EXISTS dw.fact_gestion_inventario_mensual;

CREATE TABLE dw.fact_gestion_inventario_mensual (
    gestion_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_mes_key INTEGER NOT NULL,
    producto_key INTEGER NOT NULL,
    demanda INTEGER NOT NULL,
    unidades_atendidas INTEGER NOT NULL,
    dna INTEGER NOT NULL,
    quiebre SMALLINT NOT NULL,
    unidades_vendidas INTEGER NOT NULL,
    stock_inicial INTEGER NOT NULL,
    stock_final INTEGER NOT NULL,
    nivel_inventario NUMERIC(14,2),
    rotacion NUMERIC(14,4),
    FOREIGN KEY (fecha_mes_key) REFERENCES dw.dim_fecha(fecha_key),
    FOREIGN KEY (producto_key) REFERENCES dw.dim_producto(producto_key),
    UNIQUE (fecha_mes_key, producto_key)
);

WITH ventas_detalle AS (
    SELECT
        id_detalle_pedido,
        SUM(cantidad) AS unidades_atendidas
    FROM dw.fact_ventas
    GROUP BY id_detalle_pedido
),
pedidos_mes AS (
    SELECT
        p.producto_key,
        EXTRACT(YEAR FROM f.fecha)::INTEGER AS anio,
        EXTRACT(MONTH FROM f.fecha)::INTEGER AS mes,
        SUM(p.cantidad_solicitada)::INTEGER AS demanda,
        SUM(
            LEAST(
                p.cantidad_solicitada,
                COALESCE(v.unidades_atendidas, 0)
            )
        )::INTEGER AS unidades_atendidas
    FROM dw.fact_pedidos p
    JOIN dw.dim_fecha f
        ON p.fecha_key = f.fecha_key
    LEFT JOIN ventas_detalle v
        ON p.id_detalle_pedido = v.id_detalle_pedido
    GROUP BY
        p.producto_key,
        EXTRACT(YEAR FROM f.fecha),
        EXTRACT(MONTH FROM f.fecha)
),
ventas_mes AS (
    SELECT
        v.producto_key,
        EXTRACT(YEAR FROM f.fecha)::INTEGER AS anio,
        EXTRACT(MONTH FROM f.fecha)::INTEGER AS mes,
        SUM(v.cantidad)::INTEGER AS unidades_vendidas
    FROM dw.fact_ventas v
    JOIN dw.dim_fecha f
        ON v.fecha_key = f.fecha_key
    GROUP BY
        v.producto_key,
        EXTRACT(YEAR FROM f.fecha),
        EXTRACT(MONTH FROM f.fecha)
),
inventario_ordenado AS (
    SELECT
        i.producto_key,
        f.fecha,
        EXTRACT(YEAR FROM f.fecha)::INTEGER AS anio,
        EXTRACT(MONTH FROM f.fecha)::INTEGER AS mes,
        i.stock,
        ROW_NUMBER() OVER (
            PARTITION BY
                i.producto_key,
                EXTRACT(YEAR FROM f.fecha),
                EXTRACT(MONTH FROM f.fecha)
            ORDER BY f.fecha ASC
        ) AS rn_inicial,
        ROW_NUMBER() OVER (
            PARTITION BY
                i.producto_key,
                EXTRACT(YEAR FROM f.fecha),
                EXTRACT(MONTH FROM f.fecha)
            ORDER BY f.fecha DESC
        ) AS rn_final
    FROM dw.fact_inventario i
    JOIN dw.dim_fecha f
        ON i.fecha_key = f.fecha_key
),
inventario_mes AS (
    SELECT
        producto_key,
        anio,
        mes,
        MAX(stock) FILTER (WHERE rn_inicial = 1) AS stock_inicial,
        MAX(stock) FILTER (WHERE rn_final = 1) AS stock_final
    FROM inventario_ordenado
    GROUP BY producto_key, anio, mes
)
INSERT INTO dw.fact_gestion_inventario_mensual (
    fecha_mes_key,
    producto_key,
    demanda,
    unidades_atendidas,
    dna,
    quiebre,
    unidades_vendidas,
    stock_inicial,
    stock_final,
    nivel_inventario,
    rotacion
)
SELECT
    (i.anio * 10000 + i.mes * 100 + 1) AS fecha_mes_key,
    i.producto_key,
    COALESCE(p.demanda, 0),
    COALESCE(p.unidades_atendidas, 0),
    GREATEST(
        COALESCE(p.demanda, 0) - COALESCE(p.unidades_atendidas, 0),
        0
    ) AS dna,
    CASE
        WHEN COALESCE(p.demanda, 0) - COALESCE(p.unidades_atendidas, 0) > 0
        THEN 1
        ELSE 0
    END AS quiebre,
    COALESCE(v.unidades_vendidas, 0),
    i.stock_inicial,
    i.stock_final,
    ROUND(
        (i.stock_inicial + i.stock_final)::NUMERIC / 2,
        2
    ) AS nivel_inventario,
    CASE
        WHEN (i.stock_inicial + i.stock_final)::NUMERIC / 2 > 0
        THEN ROUND(
            COALESCE(v.unidades_vendidas, 0)::NUMERIC
            /
            ((i.stock_inicial + i.stock_final)::NUMERIC / 2),
            4
        )
        ELSE NULL
    END AS rotacion
FROM inventario_mes i
LEFT JOIN pedidos_mes p
    ON i.producto_key = p.producto_key
    AND i.anio = p.anio
    AND i.mes = p.mes
LEFT JOIN ventas_mes v
    ON i.producto_key = v.producto_key
    AND i.anio = v.anio
    AND i.mes = v.mes;

SELECT COUNT(*) AS total_gestion_mensual
FROM dw.fact_gestion_inventario_mensual;

SELECT
    f.anio,
    f.mes,
    p.codigo_producto,
    g.demanda,
    g.unidades_atendidas,
    g.dna,
    g.quiebre,
    g.unidades_vendidas,
    g.stock_inicial,
    g.stock_final,
    g.nivel_inventario,
    g.rotacion
FROM dw.fact_gestion_inventario_mensual g
JOIN dw.dim_producto p
    ON g.producto_key = p.producto_key
JOIN dw.dim_fecha f
    ON g.fecha_mes_key = f.fecha_key
ORDER BY
    f.anio,
    f.mes,
    p.codigo_producto
LIMIT 50;
