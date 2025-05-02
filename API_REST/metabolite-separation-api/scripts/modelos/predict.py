import optuna
import pandas as pd
import numpy as np
import joblib
import sys
import json
import optuna.logging
import logging
import warnings
import config

warnings.filterwarnings('ignore')
optuna.logging.set_verbosity(optuna.logging.ERROR)
logging.basicConfig(level=logging.ERROR)

# Verificar que se pase el parámetro 'clase_metabolito'
if len(sys.argv) != 2:
    print("Error: El parámetro 'clase_metabolito' no ha sido proporcionado.")
    sys.exit(1)

N = config.ITERATIONS #1000
CLASE_METABOLITO = sys.argv[1]

# ---------- 1. Carga del modelo entrenado y preprocesadores ----------
modelo_path = "scripts/modelos/modelo_xgboost.pkl"
contenido = joblib.load(modelo_path)

if isinstance(contenido, dict):
    model = contenido.get("model")
    encoder = contenido.get("encoder")
    imputer = contenido.get("imputer")
    column_order = contenido.get("column_order")
else:
    print("Error: El archivo del modelo no contiene los objetos necesarios.")
    sys.exit(1)

# ---------- 2. Función de optimización ----------
def objective(trial):
    config = {
        'Eluent1': trial.suggest_categorical('Eluent1', ['eluent.1.h2o 0', 'eluent.1.acn 0']),
        'Eluent2': trial.suggest_categorical('Eluent2', ['eluent.2.acn 0', 'eluent.2.meoh 0', 'eluent.2.h2o 0']),
        'pH1': trial.suggest_float('pH1', 0.0, 11.0),
        'pH2': trial.suggest_float('pH2', 0.0, 9.0),
        'USP_Code': trial.suggest_categorical('USP_Code', [
            'column.usp.code_L1', 'column.usp.code_L68', 'column.usp.code_L11',
            'column.usp.code_0', 'column.usp.code_L43', 'column.usp.code_L122',
            'column.usp.code_L114', 'column.usp.code_L7', 'column.usp.code_L3',
            'column.usp.code_L10'
        ]),
        'Length': trial.suggest_float('Length', 50.0, 250.0),
        'Particle_Size': trial.suggest_float('Particle_Size', 1.6, 100.0),
        'Temperature': trial.suggest_float('Temperature', 25.0, 65.0),
        'Flow': trial.suggest_float('Flow', 0.01, 1.0),
        'T0': trial.suggest_float('T0', 0.125, 6.67),
        'Duration': trial.suggest_float('Duration', 3.0, 135.0),

        'x1': trial.suggest_float('x1', -645, 549),
        'x2': trial.suggest_float('x2', -1028, 965),
        'x3': trial.suggest_float('x3', -569, 668),
        'x4': trial.suggest_float('x4', -219, 188),
        'x5': trial.suggest_float('x5', -38.5, 42),
        'x6': trial.suggest_float('x6', -5.1, 4.8),
        'x7': trial.suggest_float('x7', -0.38, 0.39),
        'x8': trial.suggest_float('x8', -0.0183, 0.0192),
        'x9': trial.suggest_float('x9', -0.00054, 0.00048),
        'x10': trial.suggest_float('x10', -5.4e-6, 6.3e-6),
        'Intercept': trial.suggest_float('Intercept', 0.32, 101.21),
        'Class': CLASE_METABOLITO
    }

    df = pd.DataFrame([config])

    # Codificar variables categóricas
    categorical_cols = ['Class', 'Eluent1', 'Eluent2', 'USP_Code']
    df[categorical_cols] = encoder.transform(df[categorical_cols])

    # Reordenar columnas como en el entrenamiento
    df = df[column_order]

    # Imputar valores faltantes
    df_imputed = imputer.transform(df)

    # Realizar predicción y aplicar la transformación inversa
    pred_transformado = model.predict(df_imputed)
    pred_original = pred_transformado ** 4

    return pred_original[0]

# ---------- 3. Ejecutar optimización ----------
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=N)

# ---------- 4. Mostrar resultados ----------
best_trial = study.best_trial

result = {
    "best_params": best_trial.params,
    "best_value": best_trial.value
}

print(json.dumps(result))
