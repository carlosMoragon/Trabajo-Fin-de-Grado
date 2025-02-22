import itertools

# Leer el archivo de clases
with open('clases.txt', 'r') as file:
    clases = file.read().strip().split(", ")

# Opciones de EVAL y METODO
evals = ["peor", "medio", "mejor"]
metodos = ["alpha", "diff"]

# Generar todas las combinaciones posibles
combinaciones = itertools.product(clases, evals, metodos)

# Escribir las combinaciones en un archivo de salida
with open('todos_parametros.txt', 'w') as output_file:
    for clase, eval, metodo in combinaciones:
        output_file.write(f'{clase} "{eval}" "{metodo}"\n')

print("Combinaciones generadas y guardadas en todos_parametros.txt")

