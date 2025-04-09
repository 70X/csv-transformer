import unittest
from unittest.mock import patch
from csv_transformer.csv_menu import CSVMenu
from csv_transformer.types import TransformerEnum

class TestCSVMenu(unittest.TestCase):
	def setUp(self):
		self.headers = ["id", "name", "email", "date"]
		self.menu = CSVMenu(self.headers)

	def test_reset_user_choices(self):
		expected_choices = {
			"header_order": self.headers,
			"transformation_map": {},
			"output_file": "./data/output.csv",
		}
  
		self.assertEqual(self.menu.reset_user_choices(), expected_choices)

	def test_change_columns_order_valid(self):
		self.menu.headers = ["id", "name", "email"]
		input_order = "2, 3, 1"
		expected_order = ["name", "email", "id"]

		with patch("builtins.input", side_effect=[input_order]):
			self.menu.change_columns_order()
		
		self.assertIsInstance(self.menu.user_choices, dict)
		self.assertEqual(self.menu.user_choices["header_order"], expected_order)

	def test_change_columns_order_invalid(self):
		self.menu.headers = ["id", "name", "email"]
		input_order = "2, 3"

		with patch("builtins.input", side_effect=[input_order]):
			with patch("builtins.print") as mock_print:
				self.menu.change_columns_order()
    
				mock_print.assert_any_call("Invalid order. Please ensure all numbers are included.")

	def test_transform_map_data_valid(self):
		column = "email"
		column_choice = "3"
		transformation_choice = "2"

		with patch("builtins.input", side_effect=[column_choice, transformation_choice]):
			self.menu.transform_data()

		self.assertIn(column, self.menu.user_choices["transformation_map"])
  
	def test_transform_map_instance_sensitive_transformer(self):
		column = "email"
		column_choice = "3"
		transformation_choice = "2"

		with patch("builtins.input", side_effect=[column_choice, transformation_choice]):
			self.menu.transform_data()

		self.assertEqual(self.menu.user_choices["transformation_map"][column], TransformerEnum.SENSITIVE_DATA)

	def test_transform_map_instance_date_transformer(self):
		column = "date"
		column_choice = "4"
		transformation_choice = "3"

		with patch("builtins.input", side_effect=[column_choice, transformation_choice]):
			self.menu.transform_data()

		self.assertEqual(self.menu.user_choices["transformation_map"][column], TransformerEnum.CONVERT_DATE)
  
	def test_transform_map_instance_sequence_transformer(self):
		column = "id"
		column_choice = "1"
		transformation_choice = "1"

		with patch("builtins.input", side_effect=[column_choice, transformation_choice]):
			self.menu.transform_data()

		self.assertEqual(self.menu.user_choices["transformation_map"][column], TransformerEnum.ID_SEQUENCE)
  
	def test_transform_data_invalid_column(self):
		column = "invalid_column"

		with patch("builtins.input", side_effect=[column]):
			with patch("builtins.print") as mock_print:
				self.menu.transform_data()
				mock_print.assert_any_call("Invalid input. Please enter a valid number.")

	def test_transform_data_invalid_transformation(self):
		column = "email"
		transformation_choice = "5"

		with patch("builtins.input", side_effect=[column, transformation_choice]):
			with patch("builtins.print") as mock_print:
				self.menu.transform_data()
				mock_print.assert_any_call("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
	unittest.main()