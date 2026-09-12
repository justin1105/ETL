import pandas as pd
from pathlib import Path


# Ruta raíz del proyecto ETL
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde están los Excel originales
RAW_DIR = BASE_DIR / "DATA" / "RAW"


def extraer_datos():

    print("=== INICIANDO EXTRACCIÓN ===")

    # Tablas maestras
    productos = pd.read_excel(RAW_DIR / "Productos.xlsx")
    clientes = pd.read_excel(RAW_DIR / "Clientes.xlsx")

    # Ventas
    ventas_2023 = pd.read_excel(RAW_DIR / "Ventas_2023.xlsx")
    ventas_2024 = pd.read_excel(RAW_DIR / "Ventas_2024.xlsx")
    ventas_2025 = pd.read_excel(RAW_DIR / "Ventas_2025.xlsx")

    # Pedidos
    pedidos_2023 = pd.read_excel(RAW_DIR / "Pedidos_2023.xlsx")
    pedidos_2024 = pd.read_excel(RAW_DIR / "Pedidos_2024.xlsx")
    pedidos_2025 = pd.read_excel(RAW_DIR / "Pedidos_2025.xlsx")

    # Inventario
    inventario_2023 = pd.read_excel(RAW_DIR / "Inventario_2023.xlsx")
    inventario_2024 = pd.read_excel(RAW_DIR / "Inventario_2024.xlsx")
    inventario_2025 = pd.read_excel(RAW_DIR / "Inventario_2025.xlsx")

    datos = {
        "productos": productos,
        "clientes": clientes,

        "ventas_2023": ventas_2023,
        "ventas_2024": ventas_2024,
        "ventas_2025": ventas_2025,

        "pedidos_2023": pedidos_2023,
        "pedidos_2024": pedidos_2024,
        "pedidos_2025": pedidos_2025,

        "inventario_2023": inventario_2023,
        "inventario_2024": inventario_2024,
        "inventario_2025": inventario_2025
    }

    print("\n=== ARCHIVOS EXTRAÍDOS ===")

    for nombre, dataframe in datos.items():
        print(f"{nombre}: {len(dataframe)} registros")

    print("\nExtracción completada correctamente.")

    return datos


if __name__ == "__main__":
    extraer_datos()
