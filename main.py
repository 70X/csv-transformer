import sys
import csv_transformer.csv_handler as csv_module
from csv_transformer.csv_menu import CSVMenu
from csv_transformer.transformation import transform_data

def main():
	if len(sys.argv) < 2:
		print("Usage: python3 main.py <file_path>")
		sys.exit(1)

	file_path = sys.argv[1]
 
	handler = csv_module.CSVHandler()
	data = handler.read_csv(file_path)
	if not data:
		print("No data to process.")
		return

	headers = list(data[0].keys()) if data else []
	menu = CSVMenu(headers)
	while True:
		choice = menu.show_menu()
		if choice == "exit":
			return
		elif isinstance(choice, dict):
			data_transformed = transform_data(data, choice["transformation_map"])
			handler.write_csv(choice["output_file"], data_transformed, choice["header_order"])
 
if __name__ == "__main__":
	main()
