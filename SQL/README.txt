SQL - Data Warehouse Tesis

Orden de ejecución:
1. 01_crear_schema_dw.sql
2. 02_dim_producto.sql
3. 03_dim_cliente.sql
4. 04_dim_fecha.sql
5. 05_fact_pedidos.sql
6. 06_fact_ventas.sql
7. 07_fact_inventario.sql
8. 08_fact_gestion_inventario_mensual.sql

Prerequisito:
Las tablas limpias deben existir y estar cargadas en public:
- public.productos
- public.clientes
- public.pedidos
- public.ventas
- public.inventario

Nota:
Los scripts 02-07 corresponden a la creación inicial del DW.
El script 08 regenera la capa analítica mensual.
