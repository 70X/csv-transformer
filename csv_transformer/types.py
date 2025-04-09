from typing import Dict, List, Any, Union
from enum import Enum

class TransformerEnum(Enum):
    ID_SEQUENCE = 1
    SENSITIVE_DATA = 2
    CONVERT_DATE = 3
    
DataType = List[Dict[str, Any]]
TransformationMapType = Dict[str, TransformerEnum]
UserChoicesType = Dict[str, Union[List[str], TransformationMapType, str]]
