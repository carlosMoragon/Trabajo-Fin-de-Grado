from core.data_processing import cargar_dataset, preprocesar_dataset, to_Excel
from core.feature_extraction import get_types_of_experiments, get_family_name, filter_rt_ltn_t0
from core.calculations import fscore_mejor_caso, fscore_peor_caso, fscore_caso_medio, best_config
from core.processing import process_experiments, calculate_results, build_results_list, calcular_resultados_confiables

import config
import argparse

import sys
import os

def main():
    #sys.stderr = open(os.devnull, "w")

    # Crear un parser para recibir los argumentos desde la terminal
    parser = argparse.ArgumentParser(description="(Obligatorio) Introduce la clase a evaluar como primer parámetro.\n(No obligatorio) Especifica en caso lo quieres evaluar: peor, medio o mejor.\n(No obligatorio) Si deseas puedes especificar el modo de evaluación: 'alpha' o 'diff'")

    parser.add_argument('family', help="Introduce la clase a evaluar", nargs='?', default='Organooxygen compounds (CHEMONTID:0000323)')
    parser.add_argument('eval', help="Evaluar en el 'mejor' caso, caso 'medio' o 'peor' caso?", nargs='?', default='peor')
    parser.add_argument('modo', choices=['alpha', 'diff'], help="El segundo argumento (opcional)", nargs='?', default=('alpha' if config.IS_ALPHA else 'diff'))

    args = parser.parse_args()

    # Determinar el método fscore adecuado
    if args.eval == 'mejor':
        fscore = fscore_mejor_caso
    elif args.eval == 'peor':
        fscore = fscore_peor_caso
    elif args.eval == 'medio':
        fscore = fscore_caso_medio

    # Determinar si es modo alpha o diff
    is_alpha = True if args.modo == 'alpha' else False

    dataset = cargar_dataset(config.DATA_PATH, config.TSV_NAME)
    dataset = preprocesar_dataset(dataset)

    family = args.family
    types_of_experiments = get_types_of_experiments(dataset)
    family_name = get_family_name(family)

    result_datasets, configs = process_experiments(dataset, types_of_experiments, family_name, family)

    # Encontrar el máximo número de datos entre todas las configuraciones
    max_datos = max([len(d) for d in result_datasets])

    # Calcular los resultados ponderados por confianza
    resultados_confiables = calcular_resultados_confiables(result_datasets, is_alpha, max_datos)

    # Construir la lista de resultados finales con los scores ponderados
    lista_tuplas = build_results_list(configs, resultados_confiables, fscore)

    for tupla in lista_tuplas:
        print(f'{family}, {tupla[0]}, {tupla[1]}')#, Score Promedio: {tupla[1]}, Confianza: {tupla[2]}, Score Final: {tupla[3]}\n')


if __name__ == "__main__":
    main()
