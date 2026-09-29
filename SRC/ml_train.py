import os
import joblib
import pandas as pd

from sqlalchemy import create_engine

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


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
# 2. EXTRAER DATASET
# =========================================================

query = """
SELECT *
FROM dw.vw_ml_demanda_features
WHERE demanda_lag_3 IS NOT NULL
  AND demanda_siguiente_mes IS NOT NULL
ORDER BY producto_key, fecha_mes;
"""

df = pd.read_sql(query, engine)

df["fecha_mes"] = pd.to_datetime(df["fecha_mes"])

print("=== DATASET ML ===")
print(f"Registros: {len(df)}")


# =========================================================
# 3. VARIABLES PREDICTORAS
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

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

print("\n=== SEPARACIÓN ===")
print(f"TRAIN: {len(train)}")
print(f"TEST: {len(test)}")


# =========================================================
# 5. VARIABLES CATEGÓRICAS Y NUMÉRICAS
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
# 6. PREPROCESAMIENTO
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
# 7. MODELOS
# =========================================================

modelos = {

    "Regresion_Lineal": LinearRegression(),

"Random_Forest": RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    min_samples_leaf=2,
    max_features="sqrt",
    random_state=42,
    n_jobs=1
),

    "Gradient_Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


# =========================================================
# 8. CARPETAS DE SALIDA
# =========================================================

os.makedirs("MODELS", exist_ok=True)
os.makedirs("RESULTS", exist_ok=True)


# =========================================================
# 9. BASELINE
# =========================================================
# Método simple:
# demanda del próximo mes = demanda del mes actual
#
# Los modelos ML deberían intentar superar este resultado.

baseline_pred = X_test["demanda"]

baseline_mae = mean_absolute_error(
    y_test,
    baseline_pred
)

baseline_rmse = mean_squared_error(
    y_test,
    baseline_pred
) ** 0.5

baseline_r2 = r2_score(
    y_test,
    baseline_pred
)


resultados = [

    {
        "Modelo": "Baseline_Demanda_Actual",
        "MAE": baseline_mae,
        "RMSE": baseline_rmse,
        "R2": baseline_r2
    }

]


print("\n=========================================")
print("BASELINE")
print("=========================================")

print(f"MAE:  {baseline_mae:.4f}")
print(f"RMSE: {baseline_rmse:.4f}")
print(f"R2:   {baseline_r2:.4f}")


# =========================================================
# 10. ENTRENAR MODELOS
# =========================================================

for nombre, modelo in modelos.items():

    print("\n=========================================")
    print(f"ENTRENANDO: {nombre}")
    print("=========================================")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("modelo", modelo)
        ]
    )

    # Entrenamiento
    pipeline.fit(
        X_train,
        y_train
    )

    # Predicción
    predicciones = pipeline.predict(
        X_test
    )

    # No permitimos demandas negativas
    predicciones = predicciones.clip(min=0)


    # =====================================================
    # MÉTRICAS
    # =====================================================

    mae = mean_absolute_error(
        y_test,
        predicciones
    )

    rmse = mean_squared_error(
        y_test,
        predicciones
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predicciones
    )


    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2:   {r2:.4f}")


    resultados.append(
        {
            "Modelo": nombre,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }
    )


    # Guardar modelo entrenado
    ruta_modelo = (
        f"MODELS/{nombre}.joblib"
    )

    joblib.dump(
        pipeline,
        ruta_modelo
    )

    print(
        f"Modelo guardado: {ruta_modelo}"
    )


# =========================================================
# 11. COMPARACIÓN DE MODELOS
# =========================================================

resultados_df = pd.DataFrame(
    resultados
)

resultados_df = resultados_df.sort_values(
    by="MAE",
    ascending=True
)


print("\n=========================================")
print("COMPARACIÓN FINAL")
print("=========================================")

print(
    resultados_df.to_string(
        index=False
    )
)


# =========================================================
# 12. GUARDAR RESULTADOS
# =========================================================

resultados_df.to_csv(
    "RESULTS/metricas_modelos.csv",
    index=False
)

print(
    "\nMétricas guardadas en:"
    " RESULTS/metricas_modelos.csv"
)


# =========================================================
# 13. MEJOR MODELO SEGÚN MAE
# =========================================================

mejor_modelo = resultados_df.iloc[0]

print("\n=========================================")
print("MEJOR RESULTADO SEGÚN MAE")
print("=========================================")

print(
    f"Modelo: {mejor_modelo['Modelo']}"
)

print(
    f"MAE: {mejor_modelo['MAE']:.4f}"
)

print(
    f"RMSE: {mejor_modelo['RMSE']:.4f}"
)

print(
    f"R2: {mejor_modelo['R2']:.4f}"
)