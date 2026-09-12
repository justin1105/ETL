import pandas as pd
from extract import extraer_datos


def transformar_datos():

    print("=== INICIANDO TRANSFORMACIÓN ===")

    # =========================================================
    # 1. OBTENER DATOS EXTRAÍDOS
    # =========================================================

    datos = extraer_datos()


    # =========================================================
    # 2. CONSOLIDACIÓN DE DATOS
    # =========================================================

    ventas = pd.concat(
        [
            datos["ventas_2023"],
            datos["ventas_2024"],
            datos["ventas_2025"]
        ],
        ignore_index=True
    )

    pedidos = pd.concat(
        [
            datos["pedidos_2023"],
            datos["pedidos_2024"],
            datos["pedidos_2025"]
        ],
        ignore_index=True
    )

    inventario = pd.concat(
        [
            datos["inventario_2023"],
            datos["inventario_2024"],
            datos["inventario_2025"]
        ],
        ignore_index=True
    )


    print("\n=== TABLAS CONSOLIDADAS ===")

    print(f"ventas: {len(ventas)} registros")
    print(f"pedidos: {len(pedidos)} registros")
    print(f"inventario: {len(inventario)} registros")


    # =========================================================
    # 3. VALIDACIÓN INICIAL DE CALIDAD
    # =========================================================

    print("\n=== CALIDAD DE DATOS ANTES DE TRANSFORMAR ===")


    # ---------------------------------------------------------
    # PRODUCTOS
    # ---------------------------------------------------------

    print("\n--- PRODUCTOS ---")

    print("Nulos:")
    print(datos["productos"].isna().sum())

    print("\nDuplicados:")
    print(datos["productos"].duplicated().sum())

    print("\nTipos de datos:")
    print(datos["productos"].dtypes)


    # ---------------------------------------------------------
    # CLIENTES
    # ---------------------------------------------------------

    print("\n--- CLIENTES ---")

    print("Nulos:")
    print(datos["clientes"].isna().sum())

    print("\nDuplicados:")
    print(datos["clientes"].duplicated().sum())

    print("\nTipos de datos:")
    print(datos["clientes"].dtypes)


    # ---------------------------------------------------------
    # VENTAS
    # ---------------------------------------------------------

    print("\n--- VENTAS ---")

    print("Nulos:")
    print(ventas.isna().sum())

    print("\nDuplicados:")
    print(ventas.duplicated().sum())

    print("\nTipos de datos:")
    print(ventas.dtypes)


    # ---------------------------------------------------------
    # PEDIDOS
    # ---------------------------------------------------------

    print("\n--- PEDIDOS ---")

    print("Nulos:")
    print(pedidos.isna().sum())

    print("\nDuplicados:")
    print(pedidos.duplicated().sum())

    print("\nTipos de datos:")
    print(pedidos.dtypes)


    # ---------------------------------------------------------
    # INVENTARIO
    # ---------------------------------------------------------

    print("\n--- INVENTARIO ---")

    print("Nulos:")
    print(inventario.isna().sum())

    print("\nDuplicados:")
    print(inventario.duplicated().sum())

    print("\nTipos de datos:")
    print(inventario.dtypes)


    # =========================================================
    # 4. LIMPIEZA Y ESTANDARIZACIÓN
    # =========================================================

    print("\n=== LIMPIEZA Y ESTANDARIZACIÓN ===")


    # =========================================================
    # ID CLIENTE
    # =========================================================
    # El IDCliente corresponde al DNI o RUC.
    # Por ello debe manejarse como texto.

    ventas["IDCliente"] = ventas["IDCliente"].astype(str)

    pedidos["IDCliente"] = pedidos["IDCliente"].astype(str)

    datos["clientes"]["IDCliente"] = (
        datos["clientes"]["IDCliente"]
        .astype(str)
        .str.strip()
    )


    # =========================================================
    # ORIGEN DE FECHAS DE EXCEL
    # =========================================================

    origen_excel = pd.Timestamp("1899-12-30")


    # =========================================================
    # PRODUCTOS
    # =========================================================

    # ---------------------------------------------------------
    # PrecioReferencia
    # ---------------------------------------------------------
    # Excel interpretó el precio como una fecha.
    # Se convierte nuevamente a su valor decimal.

    if pd.api.types.is_datetime64_any_dtype(
        datos["productos"]["PrecioReferencia"]
    ):

        datos["productos"]["PrecioReferencia"] = (
            (
                datos["productos"]["PrecioReferencia"]
                - origen_excel
            )
            .dt.total_seconds()
            .div(86400)
            .round(2)
        )

    else:

        datos["productos"]["PrecioReferencia"] = (
            pd.to_numeric(
                datos["productos"]["PrecioReferencia"],
                errors="coerce"
            )
        )


    # ---------------------------------------------------------
    # CantidadPorCajon
    # ---------------------------------------------------------

    datos["productos"]["CantidadPorCajon"] = (
        pd.to_numeric(
            datos["productos"]["CantidadPorCajon"],
            errors="coerce"
        )
        .astype("Int64")
    )


    # ---------------------------------------------------------
    # Limpieza de textos de productos
    # ---------------------------------------------------------

    datos["productos"]["CodigoProducto"] = (
        datos["productos"]["CodigoProducto"]
        .astype(str)
        .str.strip()
    )

    datos["productos"]["DescripcionProducto"] = (
        datos["productos"]["DescripcionProducto"]
        .astype(str)
        .str.strip()
    )

    datos["productos"]["Categoria"] = (
        datos["productos"]["Categoria"]
        .astype(str)
        .str.strip()
    )

    datos["productos"]["Marca"] = (
        datos["productos"]["Marca"]
        .astype(str)
        .str.strip()
    )

    datos["productos"]["Unidad"] = (
        datos["productos"]["Unidad"]
        .astype(str)
        .str.strip()
    )


    # =========================================================
    # VENTAS
    # =========================================================

    # ---------------------------------------------------------
    # PrecioUnitario
    # ---------------------------------------------------------

    if pd.api.types.is_datetime64_any_dtype(
        ventas["PrecioUnitario"]
    ):

        ventas["PrecioUnitario"] = (
            (
                ventas["PrecioUnitario"]
                - origen_excel
            )
            .dt.total_seconds()
            .div(86400)
            .round(2)
        )

    else:

        ventas["PrecioUnitario"] = pd.to_numeric(
            ventas["PrecioUnitario"],
            errors="coerce"
        )


    # ---------------------------------------------------------
    # ImporteVenta
    # ---------------------------------------------------------

    if pd.api.types.is_datetime64_any_dtype(
        ventas["ImporteVenta"]
    ):

        ventas["ImporteVenta"] = (
            (
                ventas["ImporteVenta"]
                - origen_excel
            )
            .dt.total_seconds()
            .div(86400)
            .round(2)
        )

    else:

        ventas["ImporteVenta"] = pd.to_numeric(
            ventas["ImporteVenta"],
            errors="coerce"
        )


    # ---------------------------------------------------------
    # Cantidad
    # ---------------------------------------------------------

    ventas["Cantidad"] = pd.to_numeric(
        ventas["Cantidad"],
        errors="coerce"
    ).astype("Int64")


    # ---------------------------------------------------------
    # Limpieza de textos
    # ---------------------------------------------------------

    ventas["IDVenta"] = (
        ventas["IDVenta"]
        .astype(str)
        .str.strip()
    )

    ventas["IDDetallePedido"] = (
        ventas["IDDetallePedido"]
        .astype(str)
        .str.strip()
    )

    ventas["CodigoProducto"] = (
        ventas["CodigoProducto"]
        .astype(str)
        .str.strip()
    )

    ventas["IDCliente"] = (
        ventas["IDCliente"]
        .astype(str)
        .str.strip()
    )


    # =========================================================
    # PEDIDOS
    # =========================================================

    pedidos["CantidadSolicitada"] = pd.to_numeric(
        pedidos["CantidadSolicitada"],
        errors="coerce"
    ).astype("Int64")


    pedidos["IDPedido"] = (
        pedidos["IDPedido"]
        .astype(str)
        .str.strip()
    )

    pedidos["IDDetallePedido"] = (
        pedidos["IDDetallePedido"]
        .astype(str)
        .str.strip()
    )

    pedidos["CodigoProducto"] = (
        pedidos["CodigoProducto"]
        .astype(str)
        .str.strip()
    )

    pedidos["IDCliente"] = (
        pedidos["IDCliente"]
        .astype(str)
        .str.strip()
    )


    # =========================================================
    # INVENTARIO
    # =========================================================

    inventario["Stock"] = pd.to_numeric(
        inventario["Stock"],
        errors="coerce"
    ).astype("Int64")


    inventario["CodigoProducto"] = (
        inventario["CodigoProducto"]
        .astype(str)
        .str.strip()
    )


    # =========================================================
    # 5. ELIMINACIÓN DE DUPLICADOS
    # =========================================================

    datos["productos"] = datos["productos"].drop_duplicates()

    datos["clientes"] = datos["clientes"].drop_duplicates()

    ventas = ventas.drop_duplicates()

    pedidos = pedidos.drop_duplicates()

    inventario = inventario.drop_duplicates()


    # =========================================================
    # 6. VALIDACIÓN DE INTEGRIDAD REFERENCIAL
    # =========================================================

    print("\n=== VALIDACIÓN DE RELACIONES ===")


    # ---------------------------------------------------------
    # PRODUCTOS VÁLIDOS
    # ---------------------------------------------------------

    productos_validos = set(
        datos["productos"]["CodigoProducto"]
    )


    ventas_producto_invalidos = ventas[
        ~ventas["CodigoProducto"].isin(productos_validos)
    ]


    pedidos_producto_invalidos = pedidos[
        ~pedidos["CodigoProducto"].isin(productos_validos)
    ]


    inventario_producto_invalidos = inventario[
        ~inventario["CodigoProducto"].isin(productos_validos)
    ]


    # ---------------------------------------------------------
    # CLIENTES VÁLIDOS
    # ---------------------------------------------------------

    clientes_validos = set(
        datos["clientes"]["IDCliente"]
    )


    ventas_cliente_invalidos = ventas[
        ~ventas["IDCliente"].isin(clientes_validos)
    ]


    pedidos_cliente_invalidos = pedidos[
        ~pedidos["IDCliente"].isin(clientes_validos)
    ]


    # ---------------------------------------------------------
    # DETALLES DE PEDIDO VÁLIDOS
    # ---------------------------------------------------------

    detalles_pedido_validos = set(
        pedidos["IDDetallePedido"]
    )


    ventas_pedido_invalidos = ventas[
        ~ventas["IDDetallePedido"].isin(
            detalles_pedido_validos
        )
    ]


    # ---------------------------------------------------------
    # MOSTRAR RESULTADOS
    # ---------------------------------------------------------

    print(
        "Productos inválidos en ventas:",
        len(ventas_producto_invalidos)
    )

    print(
        "Productos inválidos en pedidos:",
        len(pedidos_producto_invalidos)
    )

    print(
        "Productos inválidos en inventario:",
        len(inventario_producto_invalidos)
    )

    print(
        "Clientes inválidos en ventas:",
        len(ventas_cliente_invalidos)
    )

    print(
        "Clientes inválidos en pedidos:",
        len(pedidos_cliente_invalidos)
    )

    print(
        "Ventas sin detalle de pedido válido:",
        len(ventas_pedido_invalidos)
    )


    # =========================================================
    # 7. VALIDACIÓN DESPUÉS DE TRANSFORMAR
    # =========================================================

    print(
        "\n=== CALIDAD DE DATOS DESPUÉS DE TRANSFORMAR ==="
    )


    # ---------------------------------------------------------
    # PRODUCTOS
    # ---------------------------------------------------------

    print("\n--- PRODUCTOS ---")

    print("Nulos:")
    print(datos["productos"].isna().sum())

    print("\nDuplicados:")
    print(datos["productos"].duplicated().sum())

    print("\nTipos de datos:")
    print(datos["productos"].dtypes)


    # ---------------------------------------------------------
    # CLIENTES
    # ---------------------------------------------------------

    print("\n--- CLIENTES ---")

    print("Nulos:")
    print(datos["clientes"].isna().sum())

    print("\nDuplicados:")
    print(datos["clientes"].duplicated().sum())

    print("\nTipos de datos:")
    print(datos["clientes"].dtypes)


    # ---------------------------------------------------------
    # VENTAS
    # ---------------------------------------------------------

    print("\n--- VENTAS ---")

    print("Nulos:")
    print(ventas.isna().sum())

    print("\nDuplicados:")
    print(ventas.duplicated().sum())

    print("\nTipos de datos:")
    print(ventas.dtypes)


    # ---------------------------------------------------------
    # PEDIDOS
    # ---------------------------------------------------------

    print("\n--- PEDIDOS ---")

    print("Nulos:")
    print(pedidos.isna().sum())

    print("\nDuplicados:")
    print(pedidos.duplicated().sum())

    print("\nTipos de datos:")
    print(pedidos.dtypes)


    # ---------------------------------------------------------
    # INVENTARIO
    # ---------------------------------------------------------

    print("\n--- INVENTARIO ---")

    print("Nulos:")
    print(inventario.isna().sum())

    print("\nDuplicados:")
    print(inventario.duplicated().sum())

    print("\nTipos de datos:")
    print(inventario.dtypes)


    # =========================================================
    # 8. ARMAR DATASETS TRANSFORMADOS
    # =========================================================

    datos_transformados = {

        "productos": datos["productos"],

        "clientes": datos["clientes"],

        "ventas": ventas,

        "pedidos": pedidos,

        "inventario": inventario
    }


    print(
        "\n=== TRANSFORMACIÓN COMPLETADA CORRECTAMENTE ==="
    )


    return datos_transformados


if __name__ == "__main__":

    transformar_datos()