
from collections import defaultdict
from typing import Optional
from csv_transformer.types import TransformationMapType, TransformerEnum, DataType
from csv_transformer.transformers import DefaultTransformer, IncrementalSequenceTransformer, SensitiveDataTransformer, TimestampConverterTransformer

def create_transformer_map(transformation_map):
	transformer_map = {}
	seedIdSequence = IncrementalSequenceTransformer()
	for column, transformer_enum in transformation_map.items():
		match transformer_enum:
			case TransformerEnum.ID_SEQUENCE:
				transformer_map[column] = seedIdSequence
			case TransformerEnum.SENSITIVE_DATA:
				transformer_map[column] = SensitiveDataTransformer()
			case TransformerEnum.CONVERT_DATE:
				transformer_map[column] = TimestampConverterTransformer()
			case _:
				transformer_map[column] = DefaultTransformer()
	transformer_map = defaultdict(lambda: DefaultTransformer(), transformer_map)
	return transformer_map

def transform_data(data: DataType, transform_map: TransformationMapType, start_index: Optional[int] = 1) -> DataType:
	"""Transforms the input data based on the provided transformation map."""
	transformers = create_transformer_map(transform_map)
	transformed_data = []
	print("\nTransforming data...\n")
	for index, row in enumerate(data):
		transformed_row = {}
		position = start_index + index
		for column, value in row.items():
			transformer = transformers[column]
			try:
				transformed_row[column] = transformer.transform(value)
			except Exception as e:
				print(f"Error transforming column '[{position}]' '{column}' with value '{value}': {e}")
				transformed_row[column] = value

		transformed_data.append(transformed_row)
	print("\n\n")
	return transformed_data
