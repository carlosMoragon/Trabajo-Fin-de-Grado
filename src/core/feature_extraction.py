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
