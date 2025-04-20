import optuna
import pandas as pd
import numpy as np
import onnxruntime as ort
import joblib
import sys
import json
import optuna.logging
import logging

# Deshabilitar el log detallado de Optuna
optuna.logging.set_verbosity(optuna.logging.ERROR)  # Solo mostrar mensajes de error de Optuna

# Configuración del logging de Python para evitar salidas innecesarias
logging.basicConfig(level=logging.ERROR)  # Esto solo mostrará errores, no info o warnings.

# Verificar que se pase el parámetro 'clase_metabolito' desde los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Error: El parámetro 'clase_metabolito' no ha sido proporcionado.")
    sys.exit(1)

N = 100
CLASE_METABOLITO = sys.argv[1]  # Obtener el parámetro 'clase_metabolito' de los argumentos

# ---------- 1. Carga de modelo y preprocesadores ----------
session = ort.InferenceSession("../../src/modelo2/modelo_final.onnx")  # archivo del modelo exportado
encoder = joblib.load("../../src/modelo2/encoder.pkl")           # OrdinalEncoder
imputer = joblib.load("../../src/modelo2/imputer.pkl")           # SimpleImputer
scaler = joblib.load("../../src/modelo2/scaler.pkl")             # StandardScaler
pca = joblib.load("../../src/modelo2/pca.pkl")                   # Cargar el modelo PCA

# ---------- 2. Función de optimización ----------
def objective(trial):
    config = {
        'Eluyente1': trial.suggest_categorical('Eluyente1', ['eluent.1.h2o 0', 'eluent.1.acn 0']),
        'Eluyente2': trial.suggest_categorical('Eluyente2', ['eluent.2.acn 0', 'eluent.2.meoh 0', 'eluent.2.h2o 0']),
        'pH1': trial.suggest_float('pH1', 0.0, 11.0),
        'pH2': trial.suggest_float('pH2', 0.0, 9.0),
        'USP Code': trial.suggest_categorical('USP Code', [
            'column.usp.code_L1','column.usp.code_L68', 'column.usp.code_L11',
            'column.usp.code_0','column.usp.code_L43','column.usp.code_L122',
            'column.usp.code_L114','column.usp.code_L7', 'column.usp.code_L3',
            'column.usp.code_L10'
        ]),
        'Longitud': trial.suggest_float('Longitud', 50.0, 250.0),
        'Tamaño de Partícula': trial.suggest_float('Tamaño de Partícula', 1.6, 100.0),
        'Temperatura': trial.suggest_float('Temperatura', 25.0, 65.0),
        'Flujo': trial.suggest_float('Flujo', 0.01, 1.0),
        'T0': trial.suggest_float('T0', 0.125, 6.67),
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
        'Intercepto': trial.suggest_float('Intercepto', 0.32, 101.21),

        'Clase': CLASE_METABOLITO
    }

    df_config = pd.DataFrame([config])

    cat_cols = ['Clase', 'Eluyente1', 'Eluyente2', 'USP Code']
    df_config[cat_cols] = encoder.transform(df_config[cat_cols])

    df_config = df_config[imputer.feature_names_in_]

    # Imputación
    df_imputed = imputer.transform(df_config)

    # Escalado de los datos antes de PCA (corrigiendo el orden de las transformaciones)
    df_scaled = scaler.transform(df_imputed)

    # Aplicar PCA para reducir la dimensionalidad
    df_pca = pca.transform(df_scaled)  # Aplicar la transformación PCA

    # Asegurarnos que el tipo de datos sea float32 como el modelo espera
    x_input = df_pca.astype(np.float32)

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    pred = session.run([output_name], {input_name: x_input})[0]

    return pred[0][0]

# Correr optimización
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=N)

# Solo obtener el mejor trial después de la optimización
best_trial = study.best_trial

best_params = best_trial.params
best_value = best_trial.value

# Resultado final como JSON
result = {
    "best_params": best_params,
    "best_value": best_value
}

# Pasar resultados como JSON
print(json.dumps(result))
