import re

def get_types_of_experiments(data):
    data['experiment'] = data['id'].apply(lambda x: x.split('_')[0])
    return data['experiment'].unique()

def get_family_name(family):
    match = re.search(r'\((.*?)\)', family)
    if match:
        return family.split('(')[0].strip()
    return family

def get_posible_families(experiment_data):
    alternative_parents = [set(item.split(",")) for item in experiment_data["alternative_parents"]]
    class_attr = experiment_data["classyfire.class"]
    return [parent_set.union({cls}) for parent_set, cls in zip(alternative_parents, class_attr)]

def filter_by_family(experiment_data, families, family_name, family):
    return experiment_data[[family_name in conjunto or family in conjunto for conjunto in families]]

# Filtra el dataset según su configuración 
def filter_by_config(data_family, config):
    usp_columns = [
        'column.usp.code_0', 'column.usp.code_L1', 'column.usp.code_L10',
        'column.usp.code_L109', 'column.usp.code_L11', 'column.usp.code_L114',
        'column.usp.code_L122', 'column.usp.code_L3', 'column.usp.code_L43',
        'column.usp.code_L68', 'column.usp.code_L7'
    ]
    # Crear una lista de condiciones para las columnas usp_code
    usp_conditions = [
        (data_family[usp_col] == 1) if usp_col == config.columna.usp_code else (data_family[usp_col] == 0)
        for usp_col in usp_columns
    ]

    # Combinar todas las condiciones usando '&'
    combined_usp_condition = usp_conditions[0]
    for condition in usp_conditions[1:]:
        combined_usp_condition &= condition

    # Crear la condición general
    combined_condition = (
        (data_family['column.name'] == config.columna.name) &
        (data_family['column.length'] == config.columna.length) &
        (data_family['column.id'] == config.columna.id) &
        (data_family['column.particle.size'] == config.columna.particle_size) &
        (data_family['column.temperature'] == config.columna.temperature) &
        (data_family['column.flowrate'] == config.columna.flowrate) &
        (data_family['column.t0'] == config.columna.t0) &
        combined_usp_condition  # Condiciones combinadas de usp_code
    )

    # Filtrar los datos que cumplen la condición
    return data_family[combined_condition]

def filter_rt_ltn_t0(datasets):
    return [df[df['rt'] > df['column.t0']] for df in datasets]
