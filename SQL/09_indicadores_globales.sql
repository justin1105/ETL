SELECT
    f.anio,
    f.mes,

    COUNT(*) AS productos_evaluados,

    SUM(g.quiebre) AS productos_con_quiebre,

    ROUND(
        SUM(g.quiebre)::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS qs_porcentaje,

    ROUND(
        AVG(g.nivel_inventario),
        2
    ) AS nig,

    ROUND(
        AVG(g.rotacion),
        4
    ) AS rig

FROM dw.fact_gestion_inventario_mensual g

JOIN dw.dim_fecha f
    ON g.fecha_mes_key = f.fecha_key

GROUP BY
    f.anio,
    f.mes

ORDER BY
    f.anio,
    f.mes;