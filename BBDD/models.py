from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict
from datetime import datetime

'''/predict'''
class PredictCacheModel(BaseModel):
    family: str

'''
/recommendFamily/cache
    {
    "config":{
      "eluent1": "eluent.1.h2o 0",
      "eluent2": "eluent.2.acn 0",
      "ph1": 0.9008281904610115,
      "ph2": 6.027456183070403,
      "column": {
        "length": 1.4658129805029452,
        "temperature": 5.637376656633329,
        "particleSize": 5.962133916683182,
        "flowrate": 2.3021358869347655,
        "t0": 7.061401241503109,
        "uspCode": "column.usp.code_0"    
      },
      "gradient": {
        "x0": 9.301444243932576,
        "x1": 3.616076749251911,
        "x2": 2.027123023002322,
        "x3": 4.145608029883936,
        "x4": 7.386281948385884,
        "x5": 1.2315135367772556,
        "x6": 1.0246457001441578,
        "x7": 1.4894159098541704,
        "x8": 6.84685269835264,
        "x9": 7.457744773683766,
        "x10": 1.1730742509559433,
        "duration": 4.965218492984954, "intercept": 0
      }
    }
    }
'''
class Gradient(BaseModel):
    x0: float
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
    duration: float
    intercept: float

class Column(BaseModel):
    length: float
    temperature: float
    particleSize: float
    flowrate: float
    t0: float
    uspCode: str

class Config(BaseModel):
    eluent1: str
    eluent2: str
    ph1: float
    ph2: float
    column: Column
    gradient: Gradient

class RecommendFamilyCacheModel(BaseModel):
    configuration: Config

'''
/evaluate/cache
{
  "family": "Steroids and steroid derivatives (CHEMONTID:0000258)",
  "configuration": {
    "eluent1": "eluent.1.h2o 0",
    "eluent2": "eluent.2.meoh 0",
    "ph1": 3.5910844174331817,
    "ph2": 3.5948145851318323,
    "column": {
      "uspCode": "column.usp.code_L1",
      "length": 99.56231915503989,
      "particleSize": 2.076365982540317,
      "temperature": 30.17453028537216,
      "flowrate": 0.19981804041141074,
      "t0": 1.111194968943199
    },
    "gradient": {
      "x0": 0.13834797735586274,
      "x1": 0.0,
      "x2": 118.30750184789044,
      "x3": 0.0,
      "x4": 84.69413820946424,
      "x5": 0.0,
      "x6": 3.1195613795347117,
      "x7": 0.0,
      "x8": 0.013991028480915761,
      "x9": 0.0,
      "x10": 4.6853391820595954e-06,
      "duration": 19.793499106479825,
      "intercept": 97.48935389776577
    }
  }
}
'''

class EvaluateCacheModel(BaseModel):
    family: str
    config: Config = Field(..., alias="configuration")

'''
[
  {
    "rt": 0.8709,
    "gradiente": {
      "t_gradiente": [
        4.358848288462586,
        4.358848288462586
      ],
      "eluyente2": "ACN",
      "eluyente2_gradiente": [
        0.4,
        0.8
      ],
      "ph1": 6.845945396907188,
      "eluyente1": "Agua",
      "eluyente1_gradiente": [
        0.6,
        0.2
      ],
      "ph2": 3.516469643459712
    },
    "alternative_parents": "N/A",
    "smiles_std": "CC(C(=O)O)C1=CC2=C(C=C1)C(=O)O2",
    "column": {
      "usp_code": "BDS C18",
      "name": "Inertsil",
      "length": 5,
      "particle_size": 3.5,
      "temperature": 40,
      "flowrate": 1.0,
      "t0": 1.5
    },
    "formula": "C10H12O4",
    "comment": "Analytical standard",
    "inchi_std": "InChI=1S/C10H12O4/c1-6(11)8-3-5-9(12)7(8)4-10(13)2/h3-5H,6H2,1-2H3",
    "name_metabolito": "Metabolito 1",
    "classyfire": {
      "level5": "Phenolic acid",
      "level6": "Caffeic acid derivatives",
      "superclass": "Organic compounds",
      "subclass": "Aromatic compounds",
      "kingdom": "Chemicals",
      "class": "Phenolic acids"
    },
    "inchikey_std": "QVNYCNEBTTQYLB-UHFFFAOYSA-N"
  }
]
'''
# === Experiments ===
class Classyfire(BaseModel):
    kingdom: Optional[str]
    superclass: Optional[str]
    class_: Optional[str] = Field(None, alias="class")
    subclass: Optional[str]
    level5: Optional[str]
    level6: Optional[str]

class ExperimentModel(BaseModel):
    name_metabolito: Optional[str]
    formula: Optional[str]
    rt: Optional[float]
    smiles_std: Optional[str]
    inchi_std: Optional[str]
    inchikey_std: Optional[str]
    classyfire: Optional[Classyfire]
    comment: Optional[str]
    alternative_parents: Optional[str]
    column: Optional[Column]
    gradiente: Optional[Gradient]

'''Response Families'''
class FamilyModel(BaseModel):
    family: str
    CHEMONTID: str
    API_version: str

'''
POST /feedback
{
  "family": "Benzene and substituted derivatives (CHEMONTID:0002279)",
  "configuration": {
    "eluent1": "eluent.1.acn 0",
    "eluent2": "eluent.2.meoh 0",
    "ph1": 10.141918715870036,
    "ph2": 3.2625240433534155,
    "column": {
      "uspCode": "column.usp.code_L1",
      "length": 81.438324616267,
      "particleSize": 37.51673405868385,
      "temperature": 53.568048132071986,
      "flowrate": 0.07325098874295272,
      "t0": 0.687606741099049
    },
    "gradient": {
      "x1": -312.60589974387165,
      "x2": 785.5890125688627,
      "x3": 494.4090279181114,
      "x4": -150.0437339724866,
      "x5": 16.918306496505465,
      "x6": 1.136929653532251,
      "x7": -0.3011638133215218,
      "x8": -0.005021525997895986,
      "x9": -0.0003041422977282324,
      "x10": -0.0000013550332952165905,
      "duration": 55.9157547909326,
      "x0": 96.15289102331923
    }
  },
  "score": 0.445366770029068,
  "feedback": 4
}

'''
class FeedbackConfigurationColumn(BaseModel):
    uspCode: Optional[str]
    length: Optional[float]
    name: Optional[str]
    particleSize: Optional[float]
    temperature: Optional[float]
    flowrate: Optional[float]
    t0: Optional[float]

class FeedbackConfiguration(BaseModel):
    eluent1: Optional[str]
    eluent2: Optional[str]
    ph1: Optional[float]
    ph2: Optional[float]
    column: Optional[FeedbackConfigurationColumn]
    gradient: Optional[Gradient]

class FeedbackModel(BaseModel):
    family: str
    configuration: FeedbackConfiguration
    score: float
    feedback: float
    

# === Modelo base común para logs (Evaluate, Predict, RecommendFamily) ===
class RequestResponseModel(BaseModel):
    API_version: int = 1
    request: Dict[str, Any]
    respond: Dict[str, Any]
    cacheHits: Optional[int] = 0
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
