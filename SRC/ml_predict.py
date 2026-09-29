import os
import joblib
import pandas as pd

from sqlalchemy import create_engine

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression


# =========================================================
# 1. CONEXIÓN A POSTGRESQL
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
# 2. VARIABLES DEL MODELO
# =========================================================

features = [
    "producto_key",
    "mes",
    "trimestre",

    "demanda",
    "demanda_lag_1",
    "demanda_lag_2",
    "demanda_lag_3",

    "promedio_demanda_3m",
    "promedio_demanda_6m",

    "ventas_lag_1",
    "stock_final_lag_1",
    "quiebre_lag_1",
    "rotacion_lag_1"
]

target = "demanda_siguiente_mes"


# =========================================================
# 3. DATASET PARA ENTRENAMIENTO FINAL
# =========================================================

query_train = """
SELECT *
FROM dw.vw_ml_demanda_features
WHERE demanda_lag_3 IS NOT NULL
  AND demanda_siguiente_mes IS NOT NULL
ORDER BY producto_key, fecha_mes;
"""

train = pd.read_sql(
    query_train,
    engine
)

train["fecha_mes"] = pd.to_datetime(
    train["fecha_mes"]
)

print("=== ENTRENAMIENTO FINAL ===")
print(f"Registros disponibles: {len(train)}")


# =========================================================
# 4. DATOS MÁS RECIENTES PARA PREDICCIÓN
# =========================================================
# Diciembre 2025 es el último mes conocido.
# Sus variables se utilizarán para predecir Enero 2026.

query_prediccion = """
SELECT *
FROM dw.vw_ml_demanda_features
WHERE fecha_mes = DATE '2025-12-01'
  AND demanda_lag_3 IS NOT NULL
ORDER BY producto_key;
"""

futuro = pd.read_sql(
    query_prediccion,
    engine
)

futuro["fecha_mes"] = pd.to_datetime(
    futuro["fecha_mes"]
)

print(
    f"Productos a predecir: {len(futuro)}"
)


# =========================================================
# 5. PREPARAR X E Y
# =========================================================

X_train = train[features]
y_train = train[target]

X_futuro = futuro[features]


# =========================================================
# 6. VARIABLES CATEGÓRICAS Y NUMÉRICAS
# =========================================================

categorical_features = [
    "producto_key",
    "mes",
    "trimestre"
]

numeric_features = [
    "demanda",
    "demanda_lag_1",
    "demanda_lag_2",
    "demanda_lag_3",

    "promedio_demanda_3m",
    "promedio_demanda_6m",

    "ventas_lag_1",
    "stock_final_lag_1",
    "quiebre_lag_1",
    "rotacion_lag_1"
]


# =========================================================
# 7. PREPROCESAMIENTO
# =========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categoricas",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        ),

        (
            "numericas",
            "passthrough",
            numeric_features
        )
    ]
)


# =========================================================
# 8. MODELO FINAL
# =========================================================

modelo_final = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "modelo",
            LinearRegression()
        )
    ]
)


# =========================================================
# 9. ENTRENAR CON TODO EL HISTÓRICO DISPONIBLE
# =========================================================

print("\nEntrenando modelo final...")

modelo_final.fit(
    X_train,
    y_train
)

print("Modelo final entrenado correctamente.")


# =========================================================
# 10. GENERAR PREDICCIÓN
# =========================================================

predicciones = modelo_final.predict(
    X_futuro
)

# Evitar demandas negativas
predicciones = predicciones.clip(
    min=0
)

# La demanda se maneja en unidades enteras
predicciones = predicciones.round().astype(int)


# =========================================================
# 11. CREAR RESULTADO
# =========================================================

resultado = pd.DataFrame({

    "producto_key":
        futuro["producto_key"],

    "codigo_producto":
        futuro["codigo_producto"],

    "fecha_origen":
        futuro["fecha_mes"],

    "fecha_prediccion":
        pd.Timestamp("2026-01-01"),

    "demanda_actual":
        futuro["demanda"],

    "demanda_predicha":
        predicciones,

    "modelo":
        "Regresion_Lineal"

})


# =========================================================
# 12. MOSTRAR RESULTADOS
# =========================================================

print("\n=========================================")
print("PREDICCIÓN DEMANDA - ENERO 2026")
print("=========================================")

print(
    resultado.head(20).to_string(
        index=False
    )
)

print(
    f"\nTotal productos predichos: "
    f"{len(resultado)}"
)


# =========================================================
# 13. GUARDAR MODELO FINAL
# =========================================================

os.makedirs(
    "MODELS",
    exist_ok=True
)

joblib.dump(
    modelo_final,
    "MODELS/Regresion_Lineal_Final.joblib"
)

print(
    "\nModelo guardado en:"
    " MODELS/Regresion_Lineal_Final.joblib"
)


# =========================================================
# 14. GUARDAR PREDICCIONES EN CSV
# =========================================================

os.makedirs(
    "RESULTS",
    exist_ok=True
)

resultado.to_csv(
    "RESULTS/predicciones_enero_2026.csv",
    index=False
)

print(
    "Predicciones guardadas en:"
    " RESULTS/predicciones_enero_2026.csv"
)