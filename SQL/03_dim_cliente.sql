CREATE TABLE dw.dim_cliente (
    cliente_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente VARCHAR(11) NOT NULL UNIQUE,
    tipo_documento VARCHAR(10) NOT NULL,
    nombre_razon_social VARCHAR(255) NOT NULL,
    tipo_cliente VARCHAR(30),
    fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dw.dim_cliente (
    id_cliente,
    tipo_documento,
    nombre_razon_social,
    tipo_cliente
)
SELECT
    id_cliente,
    tipo_documento,
    nombre_razon_social,
    tipo_cliente
FROM public.clientes;

SELECT COUNT(*) AS total_clientes
FROM dw.dim_cliente;
