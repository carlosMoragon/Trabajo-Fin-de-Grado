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

# Verificar que se pase el parámetro 'config_json' desde los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Error: El parámetro 'config_json' no ha sido proporcionado.")
    sys.exit(1)

# Cargar el JSON de los parámetros directamente desde el argumento pasado en la línea de comandos
try:
    config_json = json.loads(sys.argv[1])  # Convertir el string JSON a un diccionario
except json.JSONDecodeError as e:
    print(f"Error al decodificar el JSON: {e}")
    sys.exit(1)

N = 100

# ---------- 1. Carga de modelo y preprocesadores ----------
# Tienen la ruta relativa a routes del servicio REST
session = ort.InferenceSession("../../src/modelos/modelo1/modelo_final.onnx")  # archivo del modelo exportado
encoder = joblib.load("../../src/modelos/modelo1/encoder.pkl")           # OrdinalEncoder
imputer = joblib.load("../../src/modelos/modelo1/imputer.pkl")           # SimpleImputer
scaler = joblib.load("../../src/modelos/modelo1/scaler.pkl")             # StandardScaler
pca = joblib.load("../../src/modelos/modelo1/pca.pkl")                   # Cargar el modelo PCA

# ---------- 2. Función de optimización ----------
def objective(trial):
    config = {
        # Tomamos los valores del JSON, excepto 'Clase' que es optimizado
        'Eluyente1': config_json['Eluyente1'],
        'Eluyente2': config_json['Eluyente2'],
        'pH1': config_json['pH1'],
        'pH2': config_json['pH2'],
        'USP Code': config_json['USP Code'],
        'Longitud': config_json['Longitud'],
        'Tamaño de Partícula': config_json['Tamaño de Partícula'],
        'Temperatura': config_json['Temperatura'],
        'Flujo': config_json['Flujo'],
        'T0': config_json['T0'],
        'duration': config_json['duration'],

        'x1': config_json['x1'],
        'x2': config_json['x2'],
        'x3': config_json['x3'],
        'x4': config_json['x4'],
        'x5': config_json['x5'],
        'x6': config_json['x6'],
        'x7': config_json['x7'],
        'x8': config_json['x8'],
        'x9': config_json['x9'],
        'x10': config_json['x10'],
        'Intercepto': config_json['Intercepto'],

        # Aquí es donde Optuna optimiza la variable 'Clase'
        'Clase': trial.suggest_categorical('Clase', [
            'Azoles (CHEMONTID:0000436)', 
            'Benzene and substituted derivatives (CHEMONTID:0002279)', 
            'Carboxylic acids and derivatives (CHEMONTID:0000265)', 
            'Cinnamic acids and derivatives (CHEMONTID:0000476)', 
            'Coumarans (CHEMONTID:0004189)', 
            'Coumarins and derivatives (CHEMONTID:0000145)', 
            'Diazines (CHEMONTID:0001346)', 
            'Fatty Acyls (CHEMONTID:0003909)', 
            'Hydroxy acids and derivatives (CHEMONTID:0000472)', 
            'Imidazopyrimidines (CHEMONTID:0001797)', 
            'Indoles and derivatives (CHEMONTID:0000211)', 
            'Keto acids and derivatives (CHEMONTID:0000389)', 
            'Lactones (CHEMONTID:0000050)', 
            'Organic dithiophosphoric acids and derivatives (CHEMONTID:0003385)', 
            'Organic thiophosphoric acids and derivatives (CHEMONTID:0001303)', 
            'Organonitrogen compounds (CHEMONTID:0000278)', 
            'Organooxygen compounds (CHEMONTID:0000323)', 
            'Phenol ethers (CHEMONTID:0002341)', 
            'Phenols (CHEMONTID:0000134)', 
            'Phenylpropanoic acids (CHEMONTID:0002551)', 
            'Prenol lipids (CHEMONTID:0000259)', 
            'Pteridines and derivatives (CHEMONTID:0000109)', 
            'Purine nucleosides (CHEMONTID:0000479)', 
            'Purine nucleotides (CHEMONTID:0001506)', 
            'Pyridines and derivatives (CHEMONTID:0000089)', 
            'Pyrimidine nucleosides (CHEMONTID:0000480)', 
            'Pyrimidine nucleotides (CHEMONTID:0001509)', 
            'Quinolines and derivatives (CHEMONTID:0001253)', 
            'Steroids and steroid derivatives (CHEMONTID:0000258)', 
            'Triazines (CHEMONTID:0000098)'
        ])
    }

    # Convertir el diccionario 'config' a DataFrame
    df_config = pd.DataFrame([config])

    # Realizar transformaciones solo en las columnas que lo requieren
    cat_cols = ['Clase', 'Eluyente1', 'Eluyente2', 'USP Code']
    df_config[cat_cols] = encoder.transform(df_config[cat_cols])  # Solo las variables categóricas

    # Realizar imputación de valores
    df_config = df_config[imputer.feature_names_in_]
    df_imputed = imputer.transform(df_config)

    # Escalado
    df_scaled = scaler.transform(df_imputed)

    # Aplicar PCA
    df_pca = pca.transform(df_scaled)

    # Tipo de datos esperado por el modelo
    x_input = df_pca.astype(np.float32)

    # Ejecutar la predicción en el modelo
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    pred = session.run([output_name], {input_name: x_input})[0]

    return pred[0][0]

# Ejecutar la optimización
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=N)

# Obtener el mejor trial
best_trial = study.best_trial
best_params = best_trial.params
best_value = best_trial.value

# Mostrar el resultado como JSON
result = {
    "best_params": best_params,
    "best_value": best_value
}

print(json.dumps(result))
