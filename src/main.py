from core.data_processing import cargar_dataset, preprocesar_dataset
from core.feature_extraction import get_types_of_experiments, get_family_name, filter_by_family, get_posible_families
from core.calculations import fscore_mejor_caso
from core.processing import create_config_objects

import config
import argparse

def main():

    # Crear un parser para recibir los argumentos desde la terminal
    parser = argparse.ArgumentParser(description="(Obligatorio) Introduce la clase a evaluar como primer parámetro.\n(No obligatorio) Si deseas puedes especificar el modo de evaluación: 'alpha' o 'diff'")

    # Hay que quitar el nargs y el default de esta linea cuando se entre en producción
    parser.add_argument('family', help="Introduce la clase a evaluar", nargs='?', default='Organooxygen compounds (CHEMONTID:0000323)')
    parser.add_argument('modo', choices=['alpha', 'diff'], help="El segundo argumento (opcional)", nargs='?', default=('alpha' if config.IS_ALPHA else 'diff'))

    args = parser.parse_args()

    if args.modo == 'alpha':
        is_alpha = True
    elif args.modo == 'diff':
        is_alpha = False
    else:
        is_alpha = config.IS_ALPHA

    # ruta_zip = '../data/RepoRT_classified_CCinformation.zip'
    # nombre_tsv = 'RepoRT_classified_CCinformation.tsv'

    dataset = cargar_dataset(config.DATA_PATH, config.TSV_NAME)
    dataset = preprocesar_dataset(dataset)

    family = args.family #"Organooxygen compounds (CHEMONTID:0000323)"
    types_of_experiments = get_types_of_experiments(dataset)
    family_name = get_family_name(family)

    result_datasets = []
    configs = []
    for exp in types_of_experiments:
        experiment_data = dataset[dataset['experiment'] == exp]
        families = get_posible_families(experiment_data)
        data_family = filter_by_family(experiment_data, families, family_name, family)
        config_objects = create_config_objects(data_family)
        configs.extend(config_objects)
            
        datasets_by_config = [filter_by_config(data_family, config) for config in exp_configs]
        result_datasets.extend(datasets_by_config)

        print(f"Experiment {exp}: {config_objects}")


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

def main():    

    # Cargamos el dataset y lo preprocesamos
    dataset = cargar_dataset(config.DATA_PATH, config.TSV_NAME)
    dataset = preprocesar_dataset(dataset)

    # Obtener los tipos de experimentos y el nombre de la familia
    types_of_experiments = get_types_of_experiments(dataset)
    family_name = get_family_name(family)

    # A PARTIR DE AQUI ME PIERDO *1

    # Procesar experimentos y obtener datasets y configuraciones
    result_datasets, configs = process_experiments(data, types_of_experiments, family_name, family)

    #save_excel(result_datasets, "../data/result_datasets.xlsx")

    # Ordenar datasets por RT
    for dataset in result_datasets:
        dataset.sort_values(by="rt", inplace=True)

    # Calcular resultados de alpha
    resultados = calculate_results(result_datasets, is_alpha=True)

    # Construir la lista de resultados finales
    lista_tuplas = build_results_list(configs, resultados, fscore)

    return lista_tuplas

if __name__ == "__main__":
    main()
