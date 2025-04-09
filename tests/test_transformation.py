import unittest
from unittest.mock import patch
from csv_transformer.types import TransformerEnum
from csv_transformer.transformation import transform_data

class TestTransformData(unittest.TestCase):

	def setUp(self):
		self.data = [
				{'user_id': 'EFEABEA5-981B-4E45-8F13-425C456BF7F6', 'manager_id': 'CDD3AA5D-F8BF-40BB-B220-36147E1B75F7', 'name': 'John Doe', 'email_address': 'john.doe@example.com', 'start_date': '2025-Mar-01'},
				{'user_id': 'CDD3AA5D-F8BF-40BB-B220-36147E1B75F7', 'manager_id': 'A37D98B9-98E7-43ED-9B27-A79EFDDAC033', 'name': 'Jane Smith', 'email_address': 'jane.smith@example.com', 'start_date': '2025-Mar-02'}
		]
  
		self.transformation_map = {
				'user_id': TransformerEnum.ID_SEQUENCE,
				'manager_id': TransformerEnum.ID_SEQUENCE,
				'name': TransformerEnum.SENSITIVE_DATA,
				'email_address': TransformerEnum.SENSITIVE_DATA,
				'start_date': TransformerEnum.CONVERT_DATE,
		}

	def test_transform_data(self):
		result = transform_data(self.data, self.transformation_map)

		self.assertEqual(result[0]['user_id'], '1')
		self.assertEqual(result[1]['manager_id'], '3')
		self.assertNotEqual(result[0]['name'], self.data[0]['name'])
		self.assertNotEqual(result[1]['email_address'], self.data[1]['email_address'])
		self.assertEqual(result[0]['start_date'], '2025-03-01') 

	def test_transform_data_same_user_number(self):
		result = transform_data(self.data, self.transformation_map)

		self.assertEqual(result[0]['manager_id'], '2')
		self.assertEqual(result[1]['user_id'], '2')
  
	def test_transform_data_with_default_transformer(self):
		transform_map_with_default = {}

		result = transform_data(self.data, transform_map_with_default, 2000)

		self.assertEqual(result[0]['start_date'], '2025-Mar-01')
		self.assertEqual(result[1]['start_date'], '2025-Mar-02')

	def test_transform_data_empty(self):
		result = transform_data([], self.transformation_map)

		self.assertEqual(result, [])

	
	def test_transform_data_incorrect_uuid(self):
		transform_map_with_default = {
			'name': TransformerEnum.ID_SEQUENCE,
		}

		with patch("builtins.print") as mock_print:
			result = transform_data(self.data, transform_map_with_default)
			mock_print.assert_any_call("Error transforming column '[1]' 'name' with value 'John Doe': The provided data 'John Doe' is not a valid UUID.")

		self.assertEqual(result[0]['name'], 'John Doe')

 
	def test_transform_data_incorrect_date(self):
		transform_map_with_default = {
			'name': TransformerEnum.CONVERT_DATE,
		}

		with patch("builtins.print") as mock_print:
			result = transform_data(self.data, transform_map_with_default)
			mock_print.assert_any_call("Error transforming column '[1]' 'name' with value 'John Doe': The provided data 'John Doe' is not a valid date.")

		self.assertEqual(result[0]['name'], 'John Doe')
   
if __name__ == '__main__':
    unittest.main()