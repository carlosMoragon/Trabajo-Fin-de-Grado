from models.models import Column, Config
from core.feature_extraction import filter_by_family, get_posible_families, filter_by_config
from core.calculations import alpha, diff

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
            id=row['column.id'],
            particle_size=row['column.particle.size'],
            temperature=row['column.temperature'],
            flowrate=row['column.flowrate'],
            t0=row['column.t0']
        )

        eluyente1 = next((key for key in dataset.columns if key.startswith('eluent.1.') and row[key] == 100), None)
        eluyente2 = next((key for key in dataset.columns if key.startswith('eluent.2.') and row[key] == 100), None)

        config = Config(eluyente1=eluyente1, eluyente2=eluyente2, columna=columna)
        config_objects.add(config)

    return list(config_objects)

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

def build_results_list(configs, resultados, fscore):
    lista_tuplas = []
    for i in range(min(len(configs), len(resultados))):
        # Aplicamos la función fscore a los resultados de cada configuración
        score = fscore(resultados[i])
        lista_tuplas.append((configs[i].__str__(), score.__str__()))  # Emparejamos config con su puntaje
    return lista_tuplas