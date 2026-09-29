CREATE TABLE dw.fact_inventario (
    fact_inventario_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INTEGER NOT NULL,
    producto_key INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    FOREIGN KEY (fecha_key) REFERENCES dw.dim_fecha(fecha_key),
    FOREIGN KEY (producto_key) REFERENCES dw.dim_producto(producto_key)
);

INSERT INTO dw.fact_inventario (
    fecha_key,
    producto_key,
    stock
)
SELECT
    f.fecha_key,
    p.producto_key,
    i.stock
FROM public.inventario i
JOIN dw.dim_fecha f
    ON i.fecha = f.fecha
JOIN dw.dim_producto p
    ON i.codigo_producto = p.codigo_producto;

SELECT COUNT(*) AS total_fact_inventario
FROM dw.fact_inventario;
