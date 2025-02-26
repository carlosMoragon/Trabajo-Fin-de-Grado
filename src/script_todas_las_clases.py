import subprocess
import sys
import csv
import re

def extraer_datos(linea):
    match = re.match(r"(.*?), Config\(eluyente1=(.*?), eluyente2=(.*?), columna=Column\(name=(.*?), usp_code=(.*?), length=(.*?), particle_size=(.*?), temperature=(.*?), flowrate=(.*?), t0=(.*?)\)\), (.*?)$", linea)#id=(.*?), particle_size=(.*?), temperature=(.*?), flowrate=(.*?), t0=(.*?)\)\), (.*?)$", linea)
    if match:
        return list(match.groups())
    return None

def leer_clases_desde_archivo(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
    
    # Separamos el contenido usando las comas como delimitadores
    clases = contenido.split('", "')
    
    # Limpiar las comillas al inicio y final de la cadena
    clases[0] = clases[0].replace('"', '')  # Eliminar la primera comilla
    clases[-1] = clases[-1].replace('"', '')  # Eliminar la última comilla
    
    return clases

def ejecutar_clases(archivo_clases, param2, archivo_salida):#param1, param2, archivo_salida):
    try:
        clases = leer_clases_desde_archivo(archivo_clases)
        print(f"Clases leídas: {clases}")  # Mensaje de depuración para verificar que se leen todas las clases
        
        # Abrir el archivo de salida en modo escritura
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Clase", "Eluyente1", "Eluyente2", "Columna", "USP Code", "Length", "Particle Size", "Temperature", "Flowrate", "T0", "Score"])

            # Iterar sobre todas las clases leídas
            for clase in clases:
                print(f"Ejecutando para la clase: {clase}")  # Agregar mensaje de depuración para cada clase
                result = subprocess.run(
                    ['python', 'main.py', clase, param2],#param1, param2],
                    capture_output=True,
                    text=True
                )
                
                # Imprimir la salida y los errores del comando para depuración
                if result.stdout:
                    print(f"Salida de {clase}: {result.stdout}")
                if result.stderr:
                    print(f"Error al ejecutar {clase}: {result.stderr}")
                
                # Procesar la salida del comando
                for line in result.stdout.strip().split('\n'):
                    datos = extraer_datos(line)
                    if datos:
                        #writer.writerow([clase] + datos)  # Guardar también el nombre de la clase para cada fila
                        writer.writerow(datos)

                
                # Mensaje de depuración para indicar que se ha completado la clase
                print(f"Terminada ejecución para la clase: {clase}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3: #4:
        print("Uso: python script.py <param1> <param2> <archivo_salida>")
        sys.exit(1)
    
    archivo_clases = "clases.txt"
    #param1 = sys.argv[1]
    param2 = sys.argv[1]
    archivo_salida = sys.argv[2]
    
    ejecutar_clases(archivo_clases, param2, archivo_salida)#param1, param2, archivo_salida)
