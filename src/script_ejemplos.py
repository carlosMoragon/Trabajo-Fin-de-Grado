import subprocess

# Especifica el archivo de salida donde se guardarán los resultados
output_file = 'parcial_resultado.txt'

# Abrimos el archivo 'parametros.txt' para leer las líneas
with open('parametros_parcial.txt', 'r') as file:
    # Abrimos el archivo de salida para escribir los resultados
    with open(output_file, 'w') as output:
        # Iterar sobre cada línea del archivo de parámetros
        for line in file:
            # Limpiar la línea y separar los parámetros entre comillas
            params = line.strip().split('" "')
            
            # Limpiar cualquier comilla extra en los parámetros
            params = [param.replace('"', '') for param in params]
            
            # Asegurarse de que la línea tenga exactamente tres parámetros
            if len(params) == 2:#3:
                param1, param2 = params#, param3 = params
                # Ejecutar el script 'main.py' pasando los parámetros y redirigir la salida al archivo
                result = subprocess.run(['python', 'main.py', param1, param2],#, param2, param3],
                                        stdout=output, stderr=subprocess.STDOUT)
