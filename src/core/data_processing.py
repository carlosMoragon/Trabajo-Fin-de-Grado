import zipfile
import pandas as pd

def cargar_dataset(ruta_zip, nombre_tsv):
    with zipfile.ZipFile(ruta_zip, 'r') as archivo_zip:
        with archivo_zip.open(nombre_tsv) as archivo_tsv:
            dataset = pd.read_csv(archivo_tsv, sep='\t')
    return dataset

def preprocesar_dataset(dataset):
    dataset['name'] = dataset['name'].astype('str')
    dataset['comment'] = dataset['comment'].astype('str')
    return dataset
