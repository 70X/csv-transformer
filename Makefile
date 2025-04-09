.PHONY: test run

build:
	@echo "Building the project..."
	docker build -t csv-transform:latest .
	@echo "Build completed."

test: build
	@echo "Running tests..."
	docker run --rm csv-transform:latest python3 -m unittest discover -s tests
	@echo "Tests completed."

run: build
	@echo "Running the application input=./data/input.csv output=./data/output.csv make run"
	docker run --rm -it -v $(PWD)/data:/usr/src/app/data csv-transform:latest python3 main.py $(input)
	@echo "Application run completed."