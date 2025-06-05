from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


# --- Submodelos ---
class ColumnConfig(BaseModel):
    column_usp_code: str
    column_length: float
    particle_size: float
    column_temperature: float
    column_flowrate: float
    dead_time: float

class GradientConfig(BaseModel):
    duration: float
    x1: float
    x2: float
    x3: float
    x4: float
    x5: float
    x6: float
    x7: float
    x8: float
    x9: float
    x10: float
    x0: float

class Configuration(BaseModel):
    eluent_1: Literal['h2o', 'acn']
    eluent_2: Literal['acn', 'meoh', 'h2o']
    eluent_1_ph: float
    eluent_2_ph: float
    column: ColumnConfig
    gradient: GradientConfig


# --- Entradas ---
class EvaluateInput(BaseModel):
    configuration: Configuration
    class_: str = Field(..., alias="class")

class PredictInput(BaseModel):
    class_: str = Field(..., alias="class")

class FamilyRecommendInput(BaseModel):
    configuration: Configuration


# --- Salidas ---
class EvaluateOutput(BaseModel):
    score: float

class PredictOutput(BaseModel):
    configuration: Dict[str, Any]
    score: float

class RecommendFamilyOutput(BaseModel):
    class_: str = Field(..., alias="class")
    score: float