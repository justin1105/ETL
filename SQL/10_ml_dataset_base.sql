DROP VIEW IF EXISTS dw.vw_ml_demanda_base;

CREATE VIEW dw.vw_ml_demanda_base AS

SELECT
    g.producto_key,
    p.codigo_producto,
    p.categoria,
    p.marca,

    f.fecha AS fecha_mes,
    f.anio,
    f.mes,
    f.trimestre,

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
    ON g.fecha_mes_key = f.fecha_key;