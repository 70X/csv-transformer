import unittest
from unittest.mock import patch
from csv_transformer.transformers import IncrementalSequenceTransformer, SensitiveDataTransformer, TimestampConverterTransformer

class TestTransformers(unittest.TestCase):
	@patch("builtins.print")
	def setUp(self, mock_print):
			self.mock_print = mock_print

	def test_simple_integer_sequence(self):
		transformer = IncrementalSequenceTransformer()
		print(transformer.storage)
		transformed_data = transformer.transform("EFEABEA5-981B-4E45-8F13-425C456BF7F6")
  
		self.assertEqual(transformed_data, '1')

	def test_cover_sensitive_data(self):
		transformer = SensitiveDataTransformer()
		data = "example@me.com"
  
		transformed_data = transformer.transform(data)
  
		self.assertEqual(len(transformed_data), len(data))
		self.assertNotEqual(transformed_data, data)
		self.assertTrue('*' in transformed_data)

	def test_timestamp_converter_valid_format_with_month_name(self):
		transformer = TimestampConverterTransformer()
		data = "2025-Mar-01"
  	
		trasformed_data = transformer.transform(data)
  
		self.assertEqual(trasformed_data, "2025-03-01")

	def test_timestamp_converter_valid_format_datetime(self):
		transformer = TimestampConverterTransformer()
		data = "2025-03-23 16:54:43 CET"

		trasformed_data = transformer.transform(data)
  
		self.assertEqual(trasformed_data, "2025-03-23")

	def test_timestamp_converter_invalid_format(self):
		transformer = TimestampConverterTransformer()
		data = "2025-03-2316:54:43 CET"

		with self.assertRaises(ValueError) as context:
			transformer.transform(data)
  
		self.assertEqual(str(context.exception), "The provided data '2025-03-2316:54:43 CET' is not a valid date.")

	def test_transform_invalid_uuid(self):
		transformer = IncrementalSequenceTransformer()
		data = "invalid-uuid"
  
		with self.assertRaises(ValueError) as context:
			transformer.transform(data)

		self.assertEqual(str(context.exception), "The provided data 'invalid-uuid' is not a valid UUID.")

if __name__ == "__main__":
	unittest.main()