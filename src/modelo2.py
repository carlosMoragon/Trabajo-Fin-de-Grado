import pickle
import onnxruntime as ort
import numpy as np
import pandas as pd

# Cargar los archivos pickle
with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)
with open("imputer.pkl", "rb") as f:
    imputer = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("pca.pkl", "rb") as f:
    pca = pickle.load(f)

# Sesión ONNX
session = ort.InferenceSession("modelo_final.onnx")

# Preprocesamiento
# 1. Imputación
data_imputed = pd.DataFrame(imputer.transform(data), columns=data.columns)

# 2. Encoding (si aplica a algunas columnas)
if hasattr(encoder, "transform"):
    data_encoded = encoder.transform(data_imputed)
else:
    data_encoded = data_imputed  # Por si no hay columnas categóricas

# 3. Escalado
data_scaled = scaler.transform(data_encoded)

# 4. PCA (si es parte del pipeline)
data_pca = pca.transform(data_scaled)

# Convertir a formato ONNX
input_name = session.get_inputs()[0].name
input_data = data_pca.astype(np.float32)

# Hacer predicción
prediction = session.run(None, {input_name: input_data})[0]

print("Predicción:", prediction)
