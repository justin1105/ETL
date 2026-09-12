from sqlalchemy import create_engine, text
from transform import transformar_datos


def cargar_datos():

    print("=== INICIANDO CARGA A POSTGRESQL ===")

    # =========================================================
    # 1. OBTENER DATOS TRANSFORMADOS
    # =========================================================

    datos = transformar_datos()

    productos = datos["productos"].copy()
    clientes = datos["clientes"].copy()
    pedidos = datos["pedidos"].copy()
    ventas = datos["ventas"].copy()
    inventario = datos["inventario"].copy()


    # =========================================================
    # 2. ADAPTAR NOMBRES DE COLUMNAS A POSTGRESQL
    # =========================================================

    productos = productos.rename(columns={
        "CodigoProducto": "codigo_producto",
        "DescripcionProducto": "descripcion_producto",
        "Categoria": "categoria",
        "Marca": "marca",
        "Unidad": "unidad",
        "CantidadPorCajon": "cantidad_por_cajon",
        "PrecioReferencia": "precio_referencia"
    })

    clientes = clientes.rename(columns={
        "IDCliente": "id_cliente",
        "TipoDocumento": "tipo_documento",
        "NombreRazonSocial": "nombre_razon_social",
        "TipoCliente": "tipo_cliente"
    })

    pedidos = pedidos.rename(columns={
        "IDPedido": "id_pedido",
        "IDDetallePedido": "id_detalle_pedido",
        "FechaPedido": "fecha_pedido",
        "IDCliente": "id_cliente",
        "CodigoProducto": "codigo_producto",
        "CantidadSolicitada": "cantidad_solicitada"
    })

    ventas = ventas.rename(columns={
        "IDVenta": "id_venta",
        "IDDetallePedido": "id_detalle_pedido",
        "FechaVenta": "fecha_venta",
        "IDCliente": "id_cliente",
        "CodigoProducto": "codigo_producto",
        "Cantidad": "cantidad",
        "PrecioUnitario": "precio_unitario",
        "ImporteVenta": "importe_venta"
    })

    inventario = inventario.rename(columns={
        "Fecha": "fecha",
        "CodigoProducto": "codigo_producto",
        "Stock": "stock"
    })


    # =========================================================
    # 3. CONEXIÓN A POSTGRESQL
    # =========================================================

    usuario = "postgres"
    password = "Tesis2026_ETL"
    host = "localhost"
    puerto = "5432"
    base_datos = "tesis_bi_ml"

    engine = create_engine(
        f"postgresql+psycopg2://{usuario}:{password}"
        f"@{host}:{puerto}/{base_datos}"
    )


    # =========================================================
    # 4. PROBAR CONEXIÓN
    # =========================================================

    with engine.connect() as conexion:

        conexion.execute(text("SELECT 1"))

        print("\nConexión a PostgreSQL exitosa.")


    # =========================================================
    # 5. CARGAR DATOS
    # =========================================================

    # Toda la carga se ejecuta dentro de una transacción.
    # Si alguna tabla falla, PostgreSQL deshace la carga completa.

    with engine.begin() as conexion:

        # -----------------------------------------------------
        # PRODUCTOS
        # -----------------------------------------------------

        print("\nCargando productos...")

        productos.to_sql(
            "productos",
            conexion,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Productos cargados: {len(productos)}")


        # -----------------------------------------------------
        # CLIENTES
        # -----------------------------------------------------

        print("\nCargando clientes...")

        clientes.to_sql(
            "clientes",
            conexion,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Clientes cargados: {len(clientes)}")


        # -----------------------------------------------------
        # PEDIDOS
        # -----------------------------------------------------

        print("\nCargando pedidos...")

        pedidos.to_sql(
            "pedidos",
            conexion,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Pedidos cargados: {len(pedidos)}")


        # -----------------------------------------------------
        # VENTAS
        # -----------------------------------------------------

        print("\nCargando ventas...")

        ventas.to_sql(
            "ventas",
            conexion,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Ventas cargadas: {len(ventas)}")


        # -----------------------------------------------------
        # INVENTARIO
        # -----------------------------------------------------

        print("\nCargando inventario...")

        inventario.to_sql(
            "inventario",
            conexion,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Inventario cargado: {len(inventario)}")


    print("\n=== CARGA COMPLETADA CORRECTAMENTE ===")


if __name__ == "__main__":
    cargar_datos()