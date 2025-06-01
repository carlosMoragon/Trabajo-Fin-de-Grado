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

N = config.ITERATIONS 
# Verificar que se pase el parámetro 'config_json'
if len(sys.argv) != 2:
    print("Error: El parámetro 'config_json' no ha sido proporcionado.")
    sys.exit(1)

try:
    config_json = json.loads(sys.argv[1])
    #print(config_json)
except json.JSONDecodeError as e:
    print(f"Error al decodificar el JSON: {e}")
    sys.exit(1)

# ---------- 1. Cargar modelo y preprocesadores ----------
#contenido = joblib.load("./modelo_xgboost.pkl")
contenido = joblib.load("./modelo.pkl")

if isinstance(contenido, dict):
    model = contenido.get("model")
    encoder = contenido.get("encoder")
    imputer = contenido.get("imputer")
    column_order = contenido.get("column_order")
else:
    print("Error: El archivo del modelo no contiene los objetos necesarios.")
    sys.exit(1)

# ---------- 2. Función de optimización con preprocesamiento completo ----------
def objective(trial):
   
    config = {
        "eluent_1": config_json['configuration']['eluent_1'],
        "eluent_2": config_json['configuration']['eluent_2'],
        "eluent_1_ph": config_json['configuration']['eluent_1_ph'],
        "eluent_2_ph": config_json['configuration']['eluent_2_ph'],
        "column_usp_code": config_json['configuration']['column']['column_usp_code'],
        "column_length": config_json['configuration']['column']['column_length'],
        "particle_size": config_json['configuration']['column']['particle_size'],
        "column_temperature": config_json['configuration']['column']['column_temperature'],
        "column_flowrate": config_json['configuration']['column']['column_flowrate'],
        "dead_time": config_json['configuration']['column']['dead_time'],
        "duration": config_json['configuration']['gradient']['duration'],
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
        "x0": config_json['configuration']['gradient']['x0'],
        "class": trial.suggest_categorical("class", [
            'Azoles', 
            'Benzene and substituted derivatives', 
            'Carboxylic acids and derivatives', 
            'Cinnamic acids and derivatives', 
            'Coumarans', 
            'Coumarins and derivatives', 
            'Diazines', 
            'Fatty Acyls', 
            'Hydroxy acids and derivatives', 
            'Imidazopyrimidines', 
            'Indoles and derivatives', 
            'Keto acids and derivatives', 
            'Lactones', 
            'Organic dithiophosphoric acids and derivatives', 
            'Organic thiophosphoric acids and derivatives', 
            'Organonitrogen compounds', 
            'Organooxygen compounds', 
            'Phenol ethers', 
            'Phenols', 
            'Phenylpropanoic acids', 
            'Prenol lipids', 
            'Pteridines and derivatives', 
            'Purine nucleosides', 
            'Purine nucleotides', 
            'Pyridines and derivatives', 
            'Pyrimidine nucleosides', 
            'Pyrimidine nucleotides', 
            'Quinolines and derivatives', 
            'Steroids and steroid derivatives', 
            'Triazines'
        ])
    }


    df_input = pd.DataFrame([config])

    # Asegurar orden de columnas y codificación
    cat_cols = ["class", "eluent_1", "eluent_2", "column_usp_code"]
    df_input[cat_cols] = encoder.transform(df_input[cat_cols])

    # Reordenar columnas
    df_input = df_input[column_order]

    # Imputar datos faltantes
    df_input_imputed = imputer.transform(df_input)

    # Predicción y transformación inversa
    y_pred_transformed = model.predict(df_input_imputed)
    y_pred_original = y_pred_transformed ** 4  # Inversa de la raíz cuarta

    return y_pred_original[0]

# ---------- 3. Ejecutar la optimización ----------
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=N)

# ---------- 4. Resultado final ----------
best_trial = study.best_trial
result = {
    "class": best_trial.params["class"],
    "score": best_trial.value
}

print(json.dumps(result))
