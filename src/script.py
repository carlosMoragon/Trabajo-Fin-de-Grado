import subprocess
import sys
import csv
import pandas as pd
import re

# Función para extraer los datos del texto
def extraer_datos(linea):
    # Esta expresión regular debe coincidir con el formato que genera el main.py
    # Aquí asumo que los datos de la salida están en el formato adecuado
    # Cambia la expresión regular si el formato de la salida varía
    #match = re.match(r"(.*?), Config\(eluyente1=(.*?), eluyente2=(.*?), ph1=(.*?), ph2=(.*?), gradiente=(.*?), columna=Column\(name=(.*?), usp_code=(.*?), length=(.*?), particle_size=(.*?), temperature=(.*?), flowrate=(.*?), t0=(.*?)\)\), (.*?)$", linea)
    match = re.match(r"(.*?), Config\(eluyente1=(.*?), eluyente2=(.*?), ph1=(.*?), ph2=(.*?), eluyente_1_gradiente=\[(.*?)\], eluyente_2_gradiente=\[(.*?)\], t_gradiente=\[(.*?)\], columna=Column\(name=(.*?), usp_code=(.*?), length=(.*?), particle_size=(.*?), temperature=(.*?), flowrate=(.*?), t0=(.*?)\)\), (.*?), (.?)$", linea)
    if match:
        return list(match.groups())
    return None

# Leer el archivo de clases
def leer_clases_desde_archivo(archivo):
    # Utilizamos pandas para leer el archivo csv
    df = pd.read_csv(archivo, header=None)  # Leemos el CSV sin encabezado
    clases = df.iloc[0].dropna().tolist()  # Convertimos la fila en una lista (sin valores nulos)
    return clases

# Función para ejecutar las clases
def ejecutar_clases(archivo_clases, param2, archivo_salida):
    try:
        clases = leer_clases_desde_archivo(archivo_clases)
        print(f"Clases leídas: {clases}")  # Imprime las clases leídas para depuración

        # Abrimos el archivo de salida para escribir los resultados
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as output:
            writer = csv.writer(output)
            # Escribimos el encabezado del CSV de salida
            #writer.writerow(["Clase", "Eluyente1", "Eluyente2", "ph1", "ph2", "Gradiente", "Columna", "USP Code", "Length", "Particle Size", "Temperature", "Flowrate", "T0", "Score"])
            writer.writerow(["Clase", "Eluyente1", "Eluyente2", "pH1", "pH2", "Eluyente1 Gradiente", "Eluyente2 Gradiente", "T Gradiente", "Columna Nombre", "USP Code", "Longitud", "Tamaño de Partícula", "Temperatura", "Flujo", "T0", "Score", "n_datos"])


            # Iteramos sobre las clases leídas
            for clase in clases:
                print(f"Ejecutando para la clase: {clase}")  # Mensaje de depuración para cada clase

                # Ejecutamos el script main.py para cada clase
                result = subprocess.run(
                    ['python', 'main.py', clase, param2],
                    capture_output=True,
                    text=True
                )

                # Mostramos la salida y los errores para depuración
                if result.stdout:
                    print(f"Salida de {clase}: {result.stdout}")
                if result.stderr:
                    print(f"Error al ejecutar {clase}: {result.stderr}")

                # Procesamos la salida línea por línea
                for line in result.stdout.strip().split('\n'):
                    print(f"Línea procesada: {line}")  # Depuración de la línea
                    datos = extraer_datos(line)
                    if datos:
                        writer.writerow([clase] + datos)  # Escribimos los datos en el archivo de salida

                print(f"Terminada ejecución para la clase: {clase}")  # Mensaje de depuración

    except Exception as e:
        print(f"Error al ejecutar el proceso: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <param2> <archivo_salida>")
        sys.exit(1)

    archivo_clases = "clases_de_interes.csv"  # El archivo CSV que contiene las clases
    param2 = sys.argv[1]  # Parámetro que se pasará a main.py
    archivo_salida = sys.argv[2]  # Archivo donde se guardarán los resultados

    # Ejecutamos la función que maneja el proceso
    ejecutar_clases(archivo_clases, param2, archivo_salida)
