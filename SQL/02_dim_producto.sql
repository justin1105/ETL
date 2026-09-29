CREATE TABLE dw.dim_producto (
    producto_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_producto VARCHAR(30) NOT NULL UNIQUE,
    descripcion_producto VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    marca VARCHAR(100),
    unidad VARCHAR(50),
    cantidad_por_cajon INTEGER,
    precio_referencia NUMERIC(12,2),
    fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dw.dim_producto (
    codigo_producto,
    descripcion_producto,
    categoria,
    marca,
    unidad,
    cantidad_por_cajon,
    precio_referencia
)
SELECT
    codigo_producto,
    descripcion_producto,
    categoria,
    marca,
    unidad,
    cantidad_por_cajon,
    precio_referencia
FROM public.productos;

SELECT COUNT(*) AS total_productos
FROM dw.dim_producto;
