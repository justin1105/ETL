CREATE TABLE dw.fact_ventas (
    fact_venta_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INTEGER NOT NULL,
    producto_key INTEGER NOT NULL,
    cliente_key INTEGER NOT NULL,
    id_venta VARCHAR(30) NOT NULL,
    id_detalle_pedido VARCHAR(30) NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(12,2) NOT NULL,
    importe_venta NUMERIC(14,2) NOT NULL,
    FOREIGN KEY (fecha_key) REFERENCES dw.dim_fecha(fecha_key),
    FOREIGN KEY (producto_key) REFERENCES dw.dim_producto(producto_key),
    FOREIGN KEY (cliente_key) REFERENCES dw.dim_cliente(cliente_key)
);

INSERT INTO dw.fact_ventas (
    fecha_key,
    producto_key,
    cliente_key,
    id_venta,
    id_detalle_pedido,
    cantidad,
    precio_unitario,
    importe_venta
)
SELECT
    f.fecha_key,
    p.producto_key,
    c.cliente_key,
    v.id_venta,
    v.id_detalle_pedido,
    v.cantidad,
    v.precio_unitario,
    v.importe_venta
FROM public.ventas v
JOIN dw.dim_fecha f
    ON v.fecha_venta = f.fecha
JOIN dw.dim_producto p
    ON v.codigo_producto = p.codigo_producto
JOIN dw.dim_cliente c
    ON v.id_cliente = c.id_cliente;

SELECT COUNT(*) AS total_fact_ventas
FROM dw.fact_ventas;
