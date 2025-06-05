import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import re
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score




def calcular_gradiente(data):
    data = get_gradiente(data)
    for i in range(0, 18):
        data = data.drop(columns=[f"eluent.1 {i}", f"eluent.2 {i}", f"t {i}"])
    
    return data

def get_gradiente(df):
    # Encuentra las columnas que comienzan con "eluent.1", "eluent.2" y "t"
    eluent_1_columns = [col for col in df.columns if col.startswith("eluent.1 ")]
    eluent_2_columns = [col for col in df.columns if col.startswith("eluent.2 ")]
    t_columns = [col for col in df.columns if col.startswith("t")]
    
    # Asigna las listas de valores a las nuevas columnas
    df["eluyente_1_gradiente"] = df[eluent_1_columns].values.tolist()
    df["eluyente_2_gradiente"] = df[eluent_2_columns].values.tolist()
    df["t_gradiente"] = df[t_columns].values.tolist()

    return df
    

"""
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def get_gradiente(data):
    x = []
    y = []
    t = []
    
    for j in range(0, len(data['eluent.1 0'])):
        elemento_x = []
        elemento_y = []
        elemento_t = []
        for i in range(0, 18):
            elemento_x.append(data[f"eluent.1 {i}"][j])
            elemento_y.append(data[f"eluent.2 {i}"][j])
            elemento_t.append(data[f"t {i}"][j])
            
        x.append(elemento_x)
        y.append(elemento_y)
        t.append(elemento_t)
    
    X = np.array(x)  # Variables independientes
    T = np.array(t)  # Otra variable independiente
    Y = np.array(y)  # Variable dependiente
    
    # Definir el grado del polinomio
    degree = 2  

    # Lista para almacenar las ecuaciones polinómicas
    polynomial_equations = []

    # Iterar sobre cada registro
    for i in range(len(X)):
        # Seleccionar las variables del registro i
        X_single = np.array([X[i]]).reshape(1, -1)  # Forma 2D para X
        T_single = np.array([T[i]]).reshape(1, -1)  # Forma 2D para T
        Y_single = np.array(Y[i]).reshape(-1, 1)  # Asegurar formato correcto

        # Combinar las variables independientes del registro i
        X_combined_single = np.hstack([X_single, T_single])  # Unir X y T en una sola matriz

        # Crear transformación polinómica y generar características polinómicas para el registro i
        poly = PolynomialFeatures(degree)
        X_poly_single = poly.fit_transform(X_combined_single)  # Generar características polinómicas

        # Ajustar un modelo de regresión lineal polinómica
        model = LinearRegression()
        model.fit(X_poly_single, Y_single)

        # Obtener coeficientes calculados y el intercepto
        coef = model.coef_[0]  # Extraer coeficientes de la regresión
        intercept = model.intercept_[0]  # Extraer el intercepto

        # Obtener los nombres de las características generadas
        feature_names = poly.get_feature_names_out()

        # Construir la ecuación polinómica con coeficientes calculados
        equation = f"{intercept:.4f} "
        for name, c in zip(feature_names[1:], coef[1:]):  # Ignorar el término independiente
            equation += f"+ ({c:.4f})*{name} "

        # Guardar la ecuación
        polynomial_equations.append(equation)
    
    return polynomial_equations



def get_gradiente(data):
    x = []
    y = []
    t = []
    for j in range(0, len(data['eluent.1 0'])):
        elemento_x = []
        elemento_y = []
        elemento_t = []
        for i in range(0, 18):
            elemento_x.append(data[f"eluent.1 {i}"][j])
            elemento_y.append(data[f"eluent.2 {i}"][j])
            elemento_t.append(data[f"t {i}"][j])
            
        x.append(elemento_x)
        y.append(elemento_y)
        t.append(elemento_t)
    
    X = np.array(x)  # Variables independientes
    T = np.array(t)  # Otra variable independiente
    Y = np.array(y)  # Variable dependiente
    
    # Definir el grado del polinomio
    degree = 2  

    # Lista para almacenar los polinomios
    polynomial_equations = []

    # Iterar sobre cada registro
    for i in range(len(X)):
        # Seleccionar las variables del registro i
        X_single = np.array([X[i]]).reshape(1, -1)  # Forma 2D para X
        T_single = np.array([T[i]]).reshape(1, -1)  # Forma 2D para T
        Y_single = Y[i]

        # Combinar las variables independientes del registro i
        X_combined_single = np.hstack([X_single, T_single])  # Unir X y T en una sola matriz

        # Crear transformación polinómica y generar características polinómicas para el registro i
        poly = PolynomialFeatures(degree)
        X_poly_single = poly.fit_transform(X_combined_single)  # Generar características polinómicas

        # Obtener los coeficientes del modelo (simulados aquí)
        coef = np.random.random(X_poly_single.shape[1])  # Simulamos los coeficientes para este ejemplo
        intercept = np.random.random()  # Simulamos un intercepto

        # Obtener los nombres de las características generadas sin pasar input_features
        feature_names = poly.get_feature_names_out()

        # Construir la ecuación polinómica
        equation = f"{intercept:.4f} "
        for name, c in zip(feature_names[1:], coef[1:]):  # Ignorar coeficiente del término independiente
            equation += f"+ ({c:.4f})*{name} "

        # Añadir la ecuación polinómica a la lista de resultados
        polynomial_equations.append(equation)
    
    return polynomial_equations
"""


def get_types_of_experiments(data):
    data['experiment'] = data['id'].apply(lambda x: x.split('_')[0])
    return data['experiment'].unique()

def get_family_name(family):
    match = re.search(r'\((.*?)\)', family)
    if match:
        return family.split('(')[0].strip()
    return family

def get_posible_families(experiment_data):
    alternative_parents = [set(item.split(",")) for item in experiment_data["alternative_parents"]]
    class_attr = experiment_data["classyfire.class"]
    return [parent_set.union({cls}) for parent_set, cls in zip(alternative_parents, class_attr)]

def filter_by_family(experiment_data, families, family_name, family):
    return experiment_data[[family_name in conjunto or family in conjunto for conjunto in families]]

# Filtra el dataset según su configuración 
def filter_by_config(data_family, config):
    usp_columns = [
        'column.usp.code_0', 'column.usp.code_L1', 'column.usp.code_L10',
        'column.usp.code_L109', 'column.usp.code_L11', 'column.usp.code_L114',
        'column.usp.code_L122', 'column.usp.code_L3', 'column.usp.code_L43',
        'column.usp.code_L68', 'column.usp.code_L7'
    ]
    # Crear una lista de condiciones para las columnas usp_code
    usp_conditions = [
        (data_family[usp_col] == 1) if usp_col == config.columna.usp_code else (data_family[usp_col] == 0)
        for usp_col in usp_columns
    ]

    # Combinar todas las condiciones usando '&'
    combined_usp_condition = usp_conditions[0]
    for condition in usp_conditions[1:]:
        combined_usp_condition &= condition

    # Crear la condición general
    combined_condition = (
        (data_family['column.name'] == config.columna.name) &
        (data_family['column.length'] == config.columna.length) &
        #(data_family['column.id'] == config.columna.id) &
        (data_family['column.particle.size'] == config.columna.particle_size) &
        (data_family['column.temperature'] == config.columna.temperature) &
        (data_family['column.flowrate'] == config.columna.flowrate) &
        (data_family['column.t0'] == config.columna.t0) &
        combined_usp_condition  # Condiciones combinadas de usp_code
    )

    # Filtrar los datos que cumplen la condición
    return data_family[combined_condition]

def filter_rt_ltn_t0(datasets):
    return [df[df['rt'] > df['column.t0']] for df in datasets]
