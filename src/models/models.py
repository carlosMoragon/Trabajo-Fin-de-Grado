class Column:
    def __init__(self, name, usp_code, length, id, particle_size, temperature, flowrate, t0):
        self.name = name
        self.usp_code = usp_code
        self.length = length
        self.id = id
        self.particle_size = particle_size
        self.temperature = temperature
        self.flowrate = flowrate
        self.t0 = t0

    def __eq__(self, value):
        if not isinstance(value, Column):
            return False
        return (
            self.name == value.name and
            self.usp_code == value.usp_code and
            self.length == value.length and
            self.id == value.id and
            self.particle_size == value.particle_size and
            self.temperature == value.temperature and
            self.flowrate == value.flowrate and
            self.t0 == value.t0
        )

    def __hash__(self):
        return hash((
            self.name,
            self.usp_code,
            self.length,
            self.id,
            self.particle_size,
            self.temperature,
            self.flowrate,
            self.t0
        ))

class Config:
    def __init__(self, eluyente1, eluyente2, columna: Column):
        self.eluyente1 = eluyente1
        self.eluyente2 = eluyente2
        self.columna = columna

    def __eq__(self, value):
        if not isinstance(value, Config):
            return False
        return (
            self.eluyente1 == value.eluyente1 and
            self.eluyente2 == value.eluyente2 and
            self.columna == value.columna
        )

    def __hash__(self):
        return hash((self.eluyente1, self.eluyente2, self.columna))
