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
contenido = joblib.load("./modelo_xgboost.pkl")

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
        "Class": trial.suggest_categorical("Class", [
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

    df_input = pd.DataFrame([config])

    # Asegurar orden de columnas y codificación
    cat_cols = ["Class", "Eluent1", "Eluent2", "USP_Code"]
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
    "Family": best_trial.params,
    "Score": best_trial.value
}

print(json.dumps(result))
