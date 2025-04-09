from abc import ABC, abstractmethod
import random
import uuid
from dateutil import parser
from typing import Any, Dict, Optional
import pytz
          
class Transformer(ABC):
	@abstractmethod
	def transform(self, data: Any) -> str:
		return data

class DefaultTransformer(Transformer):
	def transform(self, data: Any) -> str:
		return data
	  
class IncrementalSequenceTransformer(Transformer):
	def __init__(self, storage: Optional[Dict[str, int]] = None):
		if storage is None:
			storage = {}
		self.storage = storage	
		
	def transform(self, data: Any) -> str:	
		try:
			uuid.UUID(data)
		except ValueError:
			raise ValueError(f"The provided data '{data}' is not a valid UUID.")
		if data not in self.storage:
			self.storage[data] = len(self.storage.keys()) + 1
		return str(self.storage[data])
  
class SensitiveDataTransformer(Transformer):
	def transform(self, data: Any) -> str:
		data_list = list(data)
		for _ in range(len(data) // 3):
			random_index = random.randint(0, len(data_list) - 1)
			data_list[random_index] = '*'
		return ''.join(data_list)
				
class TimestampConverterTransformer(Transformer):
	def transform(self, data: Any) -> str:
		try:
			tzinfos = {
				'CET': pytz.timezone('Europe/Paris')
			}
			parsed_date = parser.parse(data, tzinfos=tzinfos)
			return parsed_date.strftime("%Y-%m-%d")
		except Exception as e:
			raise ValueError(f"The provided data '{data}' is not a valid date.")
          