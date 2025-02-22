from core.data_processing import cargar_dataset, preprocesar_dataset, to_Excel
from core.feature_extraction import get_types_of_experiments, get_family_name, filter_rt_ltn_t0
from core.calculations import fscore_mejor_caso, fscore_peor_caso, fscore_caso_medio, best_config
from core.processing import process_experiments, calculate_results, build_results_list

import config
import argparse

import sys
import os


def main():
    sys.stderr = open(os.devnull, "w")

    # Crear un parser para recibir los argumentos desde la terminal
    parser = argparse.ArgumentParser(description="(Obligatorio) Introduce la clase a evaluar como primer parámetro.\n(No obligatorio) Especifica en caso lo quieres evaluar: peor, medio o mejor.\n(No obligatorio) Si deseas puedes especificar el modo de evaluación: 'alpha' o 'diff'")

    # Hay que quitar el nargs y el default de esta linea cuando se entre en producción
    parser.add_argument('family', help="Introduce la clase a evaluar", nargs='?', default='Organooxygen compounds (CHEMONTID:0000323)')
    parser.add_argument('eval', help="Evaluar en el 'mejor' caso, caso 'medio' o 'peor' caso?", nargs='?', default='peor')
    parser.add_argument('modo', choices=['alpha', 'diff'], help="El segundo argumento (opcional)", nargs='?', default=('alpha' if config.IS_ALPHA else 'diff'))

    args = parser.parse_args()

    if args.eval == 'mejor':
        fscore = fscore_mejor_caso
    elif args.eval == 'peor':
        fscore = fscore_peor_caso
    elif args.eval == 'medio':
        fscore = fscore_caso_medio

    if args.modo == 'alpha':
        is_alpha = True
    elif args.modo == 'diff':
        is_alpha = False
    else:
        is_alpha = config.IS_ALPHA

    dataset = cargar_dataset(config.DATA_PATH, config.TSV_NAME)
    dataset = preprocesar_dataset(dataset)

    family = args.family #"Organooxygen compounds (CHEMONTID:0000323)"
    types_of_experiments = get_types_of_experiments(dataset)
    family_name = get_family_name(family)

    result_datasets, configs = process_experiments(dataset, types_of_experiments, family_name, family)

    datasets = filter_rt_ltn_t0(result_datasets)


    #to_Excel(datasets, "../tmp/excel0_apha_2.xlsx")

    # Calcular resultados de alpha
    resultados = calculate_results(datasets, is_alpha=is_alpha)

    # Construir la lista de resultados finales
    lista_tuplas = build_results_list(configs, resultados, fscore)

    #posiciones_negativas = [i for i, tupla in enumerate(lista_tuplas) if float(tupla[1]) < 0]
    #print(f'{posiciones_negativas}\n{len(posiciones_negativas)}/{len(lista_tuplas)}\n\n')

    #print([tupla[1] for tupla in lista_tuplas])

    #print(f'\n\n\n{lista_tuplas}')

    #resultado = best_config(lista_tuplas)

    #print(resultado)
    for tupla in lista_tuplas:
        print(f'{family}, {tupla[0]}, {tupla[1]}\n')
    #return best_config
    

if __name__ == "__main__":
    main()
