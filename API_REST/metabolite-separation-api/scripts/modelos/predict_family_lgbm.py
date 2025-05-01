import optuna
import pandas as pd
import numpy as np
import joblib
import sys
import json
import optuna.logging
import logging

import warnings
warnings.filterwarnings('ignore')


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


# ---------- 1. Carga del modelo y preprocesadores ----------

# Cargar el modelo completo (incluyendo el pipeline)
#lgbm_model = joblib.load("scripts/modelos/modelo2/modelo_lgbm.pkl") 
lgbm_model = joblib.load("scripts/modelos/modelo_xgboost.pkl") 

# ---------- 2. Función de optimización ----------

def objective(trial):
    config = {
    "Eluent1": config_json['eluent1'],
    "Eluent2": config_json['eluent2'],
    "pH1": config_json['ph1'],
    "pH2": config_json['ph2'],
    "USP_Code": config_json['column']['uspCode'],
    "Length": config_json['column']['length'],
    "Particle_Size": config_json['column']['particleSize'],
    "Temperature": config_json['column']['temperature'],
    "Flow": config_json['column']['flowrate'],
    "T0": config_json['column']['t0'],
    "Duration": config_json['gradient']['duration'],
    "x1": config_json['gradient']['x1'],
    "x2": config_json['gradient']['x2'],
    "x3": config_json['gradient']['x3'],
    "x4": config_json['gradient']['x4'],
    "x5": config_json['gradient']['x5'],
    "x6": config_json['gradient']['x6'],
    "x7": config_json['gradient']['x7'],
    "x8": config_json['gradient']['x8'],
    "x9": config_json['gradient']['x9'],
    "x10": config_json['gradient']['x10'],
    "Intercept": config_json['gradient']['intercept'],
    'Class': trial.suggest_categorical('Class', [
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


    # Realizar predicción directamente usando el pipeline completo (que incluye transformaciones)
    pred = lgbm_model.predict(df_config)

    return pred[0]

# Ejecutar la optimización
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

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
