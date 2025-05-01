import pandas as pd
import numpy as np
import joblib
import sys
import json
import warnings

warnings.filterwarnings('ignore')

# Verificar que se pase el parámetro 'config_json'
if len(sys.argv) != 2:
    print("Error: El parámetro 'config_json' no ha sido proporcionado.")
    sys.exit(1)

try:
    config_json = json.loads(sys.argv[1])
except json.JSONDecodeError as e:
    print(f"Error al decodificar el JSON: {e}")
    sys.exit(1)

# ---------- 1. Cargar modelo y preprocesadores ----------
contenido = joblib.load("scripts/modelos/modelo_xgboost.pkl")

if isinstance(contenido, dict):
    model = contenido.get("model")
    encoder = contenido.get("encoder")
    imputer = contenido.get("imputer")
    column_order = contenido.get("column_order")
else:
    print("Error: El archivo del modelo no contiene los objetos necesarios.")
    sys.exit(1)

# ---------- 2. Construir input del modelo ----------
try:
    config = {
        "Eluent1": config_json['configuration']['eluent1'],
        "Eluent2": config_json['configuration']['eluent2'],
        "pH1": config_json['configuration']['ph1'],
        "pH2": config_json['configuration']['ph2'],
        "USP_Code": config_json['configuration']['column']['uspCode'],
        "Length": config_json['configuration']['column']['length'],
        "Particle_Size": config_json['configuration']['column']['particleSize'],
        "Temperature": config_json['configuration']['column']['temperature'],
        "Flow": config_json['configuration']['column']['flowrate'],
        "T0": config_json['configuration']['column']['t0'],
        "Duration": config_json['configuration']['gradient']['duration'],
        "x1": config_json['configuration']['gradient']['x1'],
        "x2": config_json['configuration']['gradient']['x2'],
        "x3": config_json['configuration']['gradient']['x3'],
        "x4": config_json['configuration']['gradient']['x4'],
        "x5": config_json['configuration']['gradient']['x5'],
        "x6": config_json['configuration']['gradient']['x6'],
        "x7": config_json['configuration']['gradient']['x7'],
        "x8": config_json['configuration']['gradient']['x8'],
        "x9": config_json['configuration']['gradient']['x9'],
        "x10": config_json['configuration']['gradient']['x10'],
        "Intercept": config_json['configuration']['gradient']['intercept'],
        "Class": config_json['family']
    }

    df_input = pd.DataFrame([config])

    # Codificar columnas categóricas
    cat_cols = ["Class", "Eluent1", "Eluent2", "USP_Code"]
    df_input[cat_cols] = encoder.transform(df_input[cat_cols])

    # Reordenar columnas
    df_input = df_input[column_order]

    # Imputar valores faltantes
    df_input_imputed = imputer.transform(df_input)

    # Realizar predicción
    y_pred_transformed = model.predict(df_input_imputed)
    y_pred_original = y_pred_transformed ** 4  # Inversa de la raíz cuarta

    # Resultado final
    result = {
        "score": float(y_pred_original[0])
    }

    print(json.dumps(result))

except Exception as e:
    print(f"Error en la predicción: {e}")
    sys.exit(1)
