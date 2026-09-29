import pandas as pd
from sqlalchemy import create_engine


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
# 2. EXTRAER DATASET DE ML
# =========================================================

query = """
SELECT *
FROM dw.vw_ml_demanda_features
WHERE demanda_lag_3 IS NOT NULL
  AND demanda_siguiente_mes IS NOT NULL
ORDER BY producto_key, fecha_mes;
"""

df = pd.read_sql(query, engine)

print("=== DATASET ML ===")
print(f"Registros totales: {len(df)}")

df["fecha_mes"] = pd.to_datetime(df["fecha_mes"])


# =========================================================
# 3. DEFINIR VARIABLES DEL MODELO
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
# 4. SEPARACIÓN TEMPORAL
# =========================================================

train = df[
    df["fecha_mes"] < "2025-01-01"
].copy()

test = df[
    df["fecha_mes"] >= "2025-01-01"
].copy()


# =========================================================
# 5. X E Y
# =========================================================

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]


# =========================================================
# 6. VALIDACIÓN
# =========================================================

print("\n=== DIVISIÓN TEMPORAL ===")

print(
    f"TRAIN: {train['fecha_mes'].min().date()} "
    f"hasta {train['fecha_mes'].max().date()}"
)

print(
    f"TEST: {test['fecha_mes'].min().date()} "
    f"hasta {test['fecha_mes'].max().date()}"
)

print(f"\nRegistros TRAIN: {len(train)}")
print(f"Registros TEST: {len(test)}")

print("\nVariables predictoras:")
print(features)

print("\nVariable objetivo:")
print(target)

print("\nX_train:", X_train.shape)
print("y_train:", y_train.shape)

print("X_test:", X_test.shape)
print("y_test:", y_test.shape)