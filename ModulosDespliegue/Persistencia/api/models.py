from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# === Gradient & Column ===

class Gradient(BaseModel):
    x0: float = Field(..., alias="x0")
    x1: float = Field(..., alias="x1")
    x2: float = Field(..., alias="x2")
    x3: float = Field(..., alias="x3")
    x4: float = Field(..., alias="x4")
    x5: float = Field(..., alias="x5")
    x6: float = Field(..., alias="x6")
    x7: float = Field(..., alias="x7")
    x8: float = Field(..., alias="x8")
    x9: float = Field(..., alias="x9")
    x10: float = Field(..., alias="x10")
    duration: float = Field(..., alias="duration")

class Column(BaseModel):
    column_usp_code: str = Field(..., alias="column_usp_code")
    column_name: Optional[str] = Field(None,  alias="column_name")
    column_length: float = Field(..., alias="column_length")
    particle_size: float = Field(..., alias="particle_size")
    column_temperature: float = Field(..., alias="column_temperature")
    column_flowrate: float = Field(..., alias="column_flowrate")
    dead_time: float = Field(..., alias="dead_time")

class Config(BaseModel):
    eluent_1: str = Field(..., alias="eluent_1")
    eluent_2: str = Field(..., alias="eluent_2")
    eluent_1_ph: float = Field(..., alias="eluent_1_ph")
    eluent_2_ph: float = Field(..., alias="eluent_2_ph")
    column: Column
    gradient: Gradient

# === Cache Models ===

class PredictCacheModel(BaseModel):
    class_: str = Field(..., alias="class")

class RecommendFamilyCacheModel(BaseModel):
    configuration: Config

class EvaluateCacheModel(BaseModel):
    class_: str = Field(..., alias="class")
    configuration: Config

# === Experiment Models ===

class Classyfire(BaseModel):
    kingdom: Optional[str]
    superclass: Optional[str]
    class_: Optional[str] = Field(None, alias="class")
    subclass: Optional[str]
    level5: Optional[str]
    level6: Optional[str]

'''class ExperimentModel(BaseModel):
    metabolite_name: Optional[str]
    formula: Optional[str]
    rt: Optional[float]
    smiles_std: Optional[str]
    inchi_std: Optional[str]
    inchikey_std: Optional[str]
    classyfire: Optional[Classyfire]
    comment: Optional[str]
    alternative_parents: Optional[str]
    column: Optional[Column]
    gradient: Optional[Gradient]
'''
class ExperimentModel(BaseModel):
    metabolite_name: Optional[str] = None
    formula: Optional[str] = None
    rt: Optional[float] = None
    smiles_std: Optional[str] = None
    inchi_std: Optional[str] = None
    inchikey_std: Optional[str] = None
    classyfire: Optional[Classyfire] = None
    comment: Optional[str] = None
    alternative_parents: Optional[str] = None
    column: Optional[Column] = None
    gradient: Optional[Gradient] = None 


# === Family ===

class FamilyModel(BaseModel):
    class_: str = Field(..., alias="class")
    CHEMONTID: str
    API_version: str

# === Feedback ===

class FeedbackModel(BaseModel):
    class_: str = Field(..., alias="class")
    configuration: Config
    score: float
    feedback: int

# === Mongo Cache: evaluate, predict, recommendFamily ===

class RequestResponseModel(BaseModel):
    API_version: int = 1
    request: Dict[str, Any]
    respond: Dict[str, Any]
    cacheHits: Optional[int] = 0
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
