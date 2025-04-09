from typing import Union
from csv_transformer.types import TransformerEnum, UserChoicesType, TransformationMapType

class CSVMenu:
	def __init__(self, headers: list[str]):
		self.headers = headers
		self.user_choices = self.reset_user_choices()

	def reset_user_choices(self) -> UserChoicesType:
		return {
			"header_order": self.headers[:],
			"transformation_map": {},
			"output_file": "./data/output.csv",
		}
  
	def pretty_print_user_choices(self):
		print("Current user choices:")
		for key, value in self.user_choices.items():
			if isinstance(value, dict):
				print(f"{key}: {{")
				for sub_key, sub_value in value.items():
					print(f"\t{sub_key}: {sub_value}")
				print("}")
			else:
					print(f"{key}: {value}")

	def show_menu(self) -> Union[UserChoicesType, str, None]:
		print("\nMenu:")
		print("1. Change the columns order")
		print("2. Transform data")
		print("3. Reset user choices")
		print("4. Output file name (default: ./data/output.csv)")
		print("5. Run (or r)")
		print("6. Exit (or q)")
		print("7. Print (or p)")
		choice = input("Choose an option: ").strip()
		match choice:
			case "1":
				self.change_columns_order()
			case "2":
				self.transform_data()
			case "3":
				self.user_choices = self.reset_user_choices()
			case "4":
				output_file = input("Enter the output file name (with .csv extension): ").strip()
				self.user_choices["output_file"] = output_file
			case "5" | "r":
				return self.user_choices
			case "6" | "q":
				print("Exiting...")
				return "exit"
			case "7" | "p":
				self.pretty_print_user_choices()
			case _:
				print("Invalid option. Please try again.")
     
	def display_headers(self):
		print("\n Original headers:")
		for i, header in enumerate(self.headers, start=1):
			print(f"{i}. {header}")
		print("\n")
  
	def change_columns_order(self):
		self.display_headers()
		print("Enter the numbers in the desired order, separated by commas:")
		print("Example: 1, 3, 2")
		new_order_indices = input("New order: ").strip().split(",")
		try:
			new_order_indices = [int(index.strip()) - 1 for index in new_order_indices]
			if set(new_order_indices) == set(range(len(self.headers))):
				self.user_choices["header_order"] = [self.headers[i] for i in new_order_indices]
				print("New order set: ", self.user_choices["header_order"])
			else:
				print("Invalid order. Please ensure all numbers are included.")
		except ValueError:
			print("Invalid input. Please enter numbers only.")
		except IndexError:
			print("Index out of range. Please ensure the numbers are within the correct range.")
		except Exception as e:
			print(f"An unexpected error occurred: {e}")

	def transform_data(self):
		self.display_headers()
		column = input("Choose a column to transform: ").strip()
		try:
			column_index = int(column) - 1
			if column_index < 0 or column_index >= len(self.headers):
				print("Invalid column index. Please try again.")
				return
			column_name = self.headers[column_index]
			print("You selected:", column_name)
		except ValueError:
			print("Invalid input. Please enter a valid number.")
			return

		print("Choose a transformation:")
		print("0. Reset to default")
		print("1. Convert UUIDs into simple integer sequence")
		print("2. Redact fields to replace data that is sensitive with similar looking random data")
		print("3. Conver timestamp to the appropriate date in the year-month-day format")
		transformation = input("Enter your choice: ").strip()

		if transformation not in ["0", "1", "2", "3"]:
			print("Invalid transformation. Please try again.")
			return

		if transformation == "0":
			self.user_choices["transformation_map"].pop(column_name, None)
			return
 
		transformation_map: TransformationMapType = {
			"1": TransformerEnum.ID_SEQUENCE,
			"2": TransformerEnum.SENSITIVE_DATA,
			"3": TransformerEnum.CONVERT_DATE,
		}
		self.user_choices["transformation_map"][column_name] = transformation_map[transformation]

