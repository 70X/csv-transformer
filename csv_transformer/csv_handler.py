import csv
from typing import List
from csv_transformer.types import DataType

class CSVHandler:
	def read_csv(self, file_path: str) -> DataType:
		try:
			with open(file_path, mode='r', newline='', encoding='utf-8') as file:
				reader = csv.DictReader(file)
				return [row for row in reader]
		except FileNotFoundError:
			print(f"Error: File '{file_path}' not found.")
			return []
		except Exception as e:
			print(f"An error occurred while reading the file: {e}")
			return []

	def write_csv(self, file_path: str, data: DataType, fieldnames: List[str]) -> None:
		print(f"Writing to file {file_path}...")
		try:
			with open(file_path, mode='w', newline='', encoding='utf-8') as file:
				writer = csv.DictWriter(file, fieldnames=fieldnames)
				writer.writeheader()
				writer.writerows(data)
				print("File written successfully.")
		except Exception as e:
			print(f"An error occurred while writing to the file: {e}")