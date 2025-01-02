from models.models import Column, Config

def create_config_objects(dataset):
    def get_uspcode(row):
        usp_columns = [
            'column.usp.code_0', 'column.usp.code_L1', 'column.usp.code_L10',
            'column.usp.code_L109', 'column.usp.code_L11', 'column.usp.code_L114',
            'column.usp.code_L122', 'column.usp.code_L3', 'column.usp.code_L43',
            'column.usp.code_L68', 'column.usp.code_L7'
        ]
        return next((col for col in usp_columns if row[col] == 1), None)

    config_objects = set()

    for _, row in dataset.iterrows():
        columna = Column(
            name=row['column.name'],
            usp_code=get_uspcode(row),
            length=row['column.length'],
            id=row['column.id'],
            particle_size=row['column.particle.size'],
            temperature=row['column.temperature'],
            flowrate=row['column.flowrate'],
            t0=row['column.t0']
        )

        eluyente1 = next((key for key in dataset.columns if key.startswith('eluent.1.') and row[key] == 100), None)
        eluyente2 = next((key for key in dataset.columns if key.startswith('eluent.2.') and row[key] == 100), None)

        config = Config(eluyente1=eluyente1, eluyente2=eluyente2, columna=columna)
        config_objects.add(config)

    return list(config_objects)
