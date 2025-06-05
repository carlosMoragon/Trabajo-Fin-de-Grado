import optuna
import pandas as pd
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
contenido = joblib.load("./modelo.pkl")


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
        'eluent_1': trial.suggest_categorical('eluent_1', ['h2o', 'acn']),
        'eluent_2': trial.suggest_categorical('eluent_2', ['acn', 'meoh', 'h2o']),
        'eluent_1_ph': trial.suggest_float('eluent_1_ph', 0.0, 11.0),
        'eluent_2_ph': trial.suggest_float('eluent_2_ph', 0.0, 9.0),
        'column_usp_code': trial.suggest_categorical('column_usp_code', [
            'L1', 'L68', 'L11',
            '0', 'L43', 'L122',
            'L114', 'L7', 'L3',
            'L10'
        ]),
        'column_length': trial.suggest_float('column_length', 50.0, 250.0),
        'particle_size': trial.suggest_float('particle_size', 1.6, 100.0),
        'column_temperature': trial.suggest_float('column_temperature', 25.0, 65.0),
        'column_flowrate': trial.suggest_float('column_flowrate', 0.01, 1.0),
        'dead_time': trial.suggest_float('dead_time', 0.125, 6.67),
        'duration': trial.suggest_float('duration', 3.0, 135.0),

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
        'x0': trial.suggest_float('x0', 0.32, 101.21),
        'class': CLASE_METABOLITO
    }


    df = pd.DataFrame([config])

    # Codificar variables categóricas
    categorical_cols = ['class', 'eluent_1', 'eluent_2', 'column_usp_code']
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
params = best_trial.params

# Reestructurar la configuración en secciones
formatted_config = {
    "configuration": {
        "eluent_1": params["eluent_1"],
        "eluent_2": params["eluent_2"],
        "eluent_1_ph": params["eluent_1_ph"],
        "eluent_2_ph": params["eluent_2_ph"],
        "column": {
            "column_usp_code": params["column_usp_code"],
            "column_length": params["column_length"],
            "particle_size": params["particle_size"],
            "column_temperature": params["column_temperature"],
            "column_flowrate": params["column_flowrate"],
            "dead_time": params["dead_time"]
        },
        "gradient": {
            "duration": params["duration"],
            "x1": params["x1"],
            "x2": params["x2"],
            "x3": params["x3"],
            "x4": params["x4"],
            "x5": params["x5"],
            "x6": params["x6"],
            "x7": params["x7"],
            "x8": params["x8"],
            "x9": params["x9"],
            "x10": params["x10"],
            "x0": params["x0"]
        }
    },
    "score": best_trial.value
}

print(json.dumps(formatted_config, indent=4))

