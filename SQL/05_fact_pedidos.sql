CREATE TABLE dw.fact_pedidos (
    fact_pedido_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INTEGER NOT NULL,
    producto_key INTEGER NOT NULL,
    cliente_key INTEGER NOT NULL,
    id_pedido VARCHAR(30) NOT NULL,
    id_detalle_pedido VARCHAR(30) NOT NULL,
    cantidad_solicitada INTEGER NOT NULL,
    FOREIGN KEY (fecha_key) REFERENCES dw.dim_fecha(fecha_key),
    FOREIGN KEY (producto_key) REFERENCES dw.dim_producto(producto_key),
    FOREIGN KEY (cliente_key) REFERENCES dw.dim_cliente(cliente_key)
);

INSERT INTO dw.fact_pedidos (
    fecha_key,
    producto_key,
    cliente_key,
    id_pedido,
    id_detalle_pedido,
    cantidad_solicitada
)
SELECT
    f.fecha_key,
    p.producto_key,
    c.cliente_key,
    pe.id_pedido,
    pe.id_detalle_pedido,
    pe.cantidad_solicitada
FROM public.pedidos pe
JOIN dw.dim_fecha f
    ON pe.fecha_pedido = f.fecha
JOIN dw.dim_producto p
    ON pe.codigo_producto = p.codigo_producto
JOIN dw.dim_cliente c
    ON pe.id_cliente = c.id_cliente;

SELECT COUNT(*) AS total_fact_pedidos
FROM dw.fact_pedidos;
