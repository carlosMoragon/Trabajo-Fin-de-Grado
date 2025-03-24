from models.models import Column, Config
from core.feature_extraction import filter_by_family, get_posible_families, filter_by_config
from core.calculations import alpha, diff

def normalizar_datos(lista_tuplas):
    if not lista_tuplas:
        return []

    n_max = max(score for _, score in lista_tuplas)

    if n_max == 0:
        return [(config, 0) for config, _ in lista_tuplas]

    lista_normalizada = [(config, score / n_max) for config, score in lista_tuplas]

    return lista_normalizada
    

def create_config_objects(dataset):
    def get_uspcode(row):
        usp_columns = [
            'column.usp.code_0', 'column.usp.code_L1', 'column.usp.code_L10',
            'column.usp.code_L109', 'column.usp.code_L11', 'column.usp.code_L114',
            'column.usp.code_L122', 'column.usp.code_L3', 'column.usp.code_L43',
            'column.usp.code_L68', 'column.usp.code_L7'
        ]
        return next((col for col in usp_columns if row[col] == 1), None)

    config_objects = set()

    for _, row in dataset.iterrows():
        columna = Column(
            name=row['column.name'],
            usp_code=get_uspcode(row),
            length=row['column.length'],
            #id=row['column.id'],
            particle_size=row['column.particle.size'],
            temperature=row['column.temperature'],
            flowrate=row['column.flowrate'],
            t0=row['column.t0']
        )

        #ph1 = row.get('eluent.1.pH 0', 0)
        #ph2 = row.get('eluent.2.pH 0', 0)
        
        ph1 = row.get(next((key for key in dataset.columns if key.startswith('eluent.1.pH ') and row[key] != 0), None), 0)
        ph2 = row.get(next((key for key in dataset.columns if key.startswith('eluent.2.pH ') and row[key] != 0), None), 0)

        ph1 = float(ph1)
        ph2 = float(ph2)
        
        eluyente_1_gradiente = row.get('eluyente_1_gradiente', 0)
        eluyente_2_gradiente = row.get('eluyente_2_gradiente', 0)
        t_gradiente = row.get('t_gradiente', 0)

        #gradiente = row.get('gradiente', 0)

        eluyente1 = next((key for key in dataset.columns if key.startswith('eluent.1.') and row[key] != 0), None)
        eluyente2 = next((key for key in dataset.columns if key.startswith('eluent.2.') and row[key] != 0), None)

        config = Config(eluyente1=eluyente1, eluyente2=eluyente2, ph1=ph1, ph2=ph2, eluyente_1_gradiente=eluyente_1_gradiente, eluyente_2_gradiente=eluyente_2_gradiente, t_gradiente=t_gradiente, columna=columna)#gradiente, columna=columna)
        config_objects.add(config)

    return list(config_objects)

def process_experiments_ownMethodScore(data, experiments):
    result_datasets = []
    configs = []  # Lista de configuraciones
    posible_families = []
    families_exp = []
    for exp in experiments:
        experiment_data = data[data['experiment'] == exp]
        families = get_posible_families(experiment_data)
            
        # Creamos un objeto configuración y lo añadimos a una lista
        exp_configs = create_config_objects(experiment_data)
        configs.extend(exp_configs)
            
        datasets_by_config = [filter_by_config(experiment_data, config) for config in exp_configs]
        result_datasets.extend(datasets_by_config)
        families_exp.append(families)
        posible_families.append(families_exp)
        families_exp.clear()
        
    return result_datasets, configs, posible_families

# Dada los tipos de experimentos separa
def process_experiments(data, experiments, family_name, family):
    result_datasets = []
    configs = []  # Lista de configuraciones
    for exp in experiments:
        experiment_data = data[data['experiment'] == exp]
        families = get_posible_families(experiment_data)
        data_family = filter_by_family(experiment_data, families, family_name, family)
            
        # Creamos un objeto configuración y lo añadimos a una lista
        exp_configs = create_config_objects(data_family)
        configs.extend(exp_configs)
            
        datasets_by_config = [filter_by_config(data_family, config) for config in exp_configs]
        result_datasets.extend(datasets_by_config)
        
    return result_datasets, configs

def calculate_alpha_results(dataset):
    resultados_dataset = []
    primer_elemento = dataset.iloc[0]
    #t0_value = t0(primer_elemento['column.length'], primer_elemento['column.flowrate'])
        
    for i in range(1, len(dataset)):
        elemento_n_menos_1 = dataset.iloc[i - 1]
        elemento_n = dataset.iloc[i]
        resultado = alpha(elemento_n_menos_1['rt'], elemento_n['rt'], elemento_n_menos_1['column.t0'], elemento_n['column.t0'])#t0_value)
        resultados_dataset.append(resultado)
    return resultados_dataset

def calculate_diff_results(dataset):
    dataset = dataset.sort_values(by='rt').reset_index(drop=True)
    resultados_dataset = []
    ultimo_elemento = dataset.iloc[len(dataset)-1]
    total = ultimo_elemento['rt']
        
    for i in range(1, len(dataset)):
        elemento_n_menos_1 = dataset.iloc[i - 1]
        elemento_n = dataset.iloc[i]
        resultado = diff(elemento_n_menos_1['rt'], elemento_n['rt'], total)
        resultados_dataset.append(resultado)
    return resultados_dataset

def calculate_results(result_datasets, is_alpha):
    resultados = []
    for dataset in result_datasets:
        if dataset.empty:
            continue
        if(is_alpha):
            resultados.append(calculate_alpha_results(dataset))
        else:
            resultados.append(calculate_diff_results(dataset))
        
    return resultados



def calcular_resultados_confiables(result_datasets, is_alpha, max_datos):
    """
    Calcula los resultados de las configuraciones y los pondera con la confianza
    calculada en función del tamaño de los datos.

    :param result_datasets: Lista de datasets por configuración
    :param is_alpha: True para calcular alpha, False para calcular diff
    :param max_datos: Número máximo de datos entre todas las configuraciones
    :return: Lista de resultados ponderados por la confianza
    """
    resultados_finales = []

    for dataset in result_datasets:
        if dataset.empty:
            continue

        # Obtener la cantidad de datos de esta configuración
        n_datos = len(dataset)
        
        # Calcular la confianza
        confianza = calcular_confianza(n_datos, max_datos)

        # Calcular los resultados (alpha o diff)
        if is_alpha:
            resultados = calculate_alpha_results(dataset)
        else:
            resultados = calculate_diff_results(dataset)

            # Contar cuántos valores son negativos antes de corregirlos
        negativos = sum(1 for r in resultados if r < 0)
        #print(f"Cantidad de valores negativos antes de corregir: {negativos}")
            # Asegurar que los valores negativos de alpha/diff no arruinen el cálculo
            #resultados = [max(0, r) for r in resultados]  # Eliminar valores negativos
            
            # Calcular el score promedio
        score_promedio = sum(resultados) / len(resultados) if resultados else 0

            # Ponderar el score con la confianza y evitar negativos
        score_final = max(0, score_promedio * confianza)

            #print(f"nº dataset: {n_datos}, max_datos: {max_datos}, confianza: {confianza}, score_promedio score: {score_final}")

            # Guardar el resultado final
        resultados_finales.append((score_promedio, confianza, score_final))

    return resultados_finales

def calcular_resultados_confiables_gth(result_datasets, is_alpha):
    """
    Calcula los resultados de las configuraciones y los pondera con la confianza
    calculada en función del tamaño de los datos.

    :param result_datasets: Lista de datasets por configuración
    :param is_alpha: True para calcular alpha, False para calcular diff
    :param max_datos: Número máximo de datos entre todas las configuraciones
    :return: Lista de resultados ponderados por la confianza
    """
    resultados_finales = []
    max_datos = max([len(d) for d in result_datasets])

    for dataset in result_datasets:
        if dataset.empty:
            continue

        # Obtener la cantidad de datos de esta configuración
        n_datos = len(dataset)

            # Calcular la confianza
        confianza = calcular_confianza(n_datos, max_datos)

            # Calcular los resultados (alpha o diff)
        if is_alpha:
            resultados = calculate_alpha_results(dataset)
        else:
            resultados = calculate_diff_results(dataset)

            #print(f"Cantidad de valores negativos antes de corregir: {negativos}")
            # Asegurar que los valores negativos de alpha/diff no arruinen el cálculo
            #resultados = [max(0, r) for r in resultados]  # Eliminar valores negativos
            
            # Calcular el score promedio
        score_promedio = sum(resultados) / len(resultados) if resultados else 0

            # Ponderar el score con la confianza y evitar negativos
        score_final = max(0, score_promedio * confianza)

            #print(f"nº dataset: {n_datos}, max_datos: {max_datos}, confianza: {confianza}, score_promedio score: {score_final}")

            # Guardar el resultado final
        resultados_finales.append((score_promedio, confianza, score_final))

    return resultados_finales

def calcular_confianza(n_datos, max_datos):
    """
    Calcula la confianza de una configuración basada en la cantidad de datos
    que tiene en comparación con la configuración con más datos.
    
    :param n_datos: Número de datos en la configuración
    :param max_datos: Número máximo de datos entre todas las configuraciones
    :return: Un valor de confianza entre 0 y 1
    """
    return n_datos / max_datos


def build_results_list(configs, resultados):
    """
    Construye la lista de resultados finales, con el score ponderado por confianza.
    
    :param configs: Lista de configuraciones
    :param resultados: Resultados calculados para cada configuración
    :param fscore: Función de puntuación (por ejemplo, fscore_mejor_caso)
    :return: Lista de tuplas (configuración, score final)
    """
    lista_tuplas = []
    
    for i, config in enumerate(configs):
        score_promedio, confianza, score_final = resultados[i]
        lista_tuplas.append((config, score_final))#score_promedio, confianza, score_final))

    # Ordenar por el score final, de mayor a menor
    lista_tuplas = sorted(lista_tuplas, key=lambda x: x[1], reverse=True)#x[3], reverse=True)
    
    return lista_tuplas

'''
def build_results_list(configs, resultados, fscore):
    lista_tuplas = []
    for i in range(min(len(configs), len(resultados))):
        # Aplicamos la función fscore a los resultados de cada configuración
        score = fscore(resultados[i])
        lista_tuplas.append((configs[i].__str__(), score.__str__()))  # Emparejamos config con su puntaje
    return lista_tuplas
'''