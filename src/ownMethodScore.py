from core.data_processing import cargar_dataset, preprocesar_dataset
from core.feature_extraction import get_types_of_experiments, get_family_name, calcular_gradiente
from core.processing import build_results_list,normalizar_datos, calcular_resultados_confiables_gth, process_experiments_ownMethodScore

import config
import argparse

def main():

    # Crear un parser para recibir los argumentos desde la terminal
    parser = argparse.ArgumentParser(description="(Obligatorio) Introduce la clase a evaluar como primer parámetro.\n(No obligatorio) Especifica en caso lo quieres evaluar: peor, medio o mejor.\n(No obligatorio) Si deseas puedes especificar el modo de evaluación: 'alpha' o 'diff'")

    parser.add_argument('family', help="Introduce la clase a evaluar", nargs='?', default='Organooxygen compounds (CHEMONTID:0000323)')
    parser.add_argument('modo', choices=['alpha', 'diff'], help="El segundo argumento (opcional)", nargs='?', default=('alpha' if config.IS_ALPHA else 'diff'))

    args = parser.parse_args()

    # Determinar si es modo alpha o diff
    is_alpha = True if args.modo == 'alpha' else False

    dataset = cargar_dataset(config.DATA_PATH, config.TSV_NAME)
    dataset = preprocesar_dataset(dataset)

    dataset = calcular_gradiente(dataset)

    family = args.family
    types_of_experiments = get_types_of_experiments(dataset)
    family_name = get_family_name(family)

    result_datasets, configs, posible_families = process_experiments_ownMethodScore(dataset, types_of_experiments)
    print(f"length df: {len(result_datasets)}")
    print(f"length configs: {len(configs)}")
    print(f"length posible_families: {len(posible_families)}")

    for i, df in enumerate(result_datasets):
        

        #print(configs[i])
    #    print(posible_families[0])

if __name__ == "__main__":
    main()
