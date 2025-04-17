# CSV Transformer

A small Python command-line application that allows you to transform an existing CSV dataset into a different format.

For more details about the requirements, please refer to the [CHALLENGE file](./CHALLENGE.md).

## Prerequisites

- `Docker` is required
- `make` is required to run the provided commands. \
  Alternatively, you can copy and paste the individual instructions from the `Makefile`.

## Get Started

1. Run tests

   ```sh
   make test
   ```

2. Start the app

   ```sh
   input=./data/input.csv make run
   ```

## Menu Overview

This program provides a menu-driven interface that allows users to process and transform data from a CSV file. The menu guides you through various options, including selecting columns and applying transformations.

Unless you choose to exit, the menu is shown after every action. You can overwrite previous choices or reset them at any time.

```sh
Menu:
1. Change the columns order
2. Transform data
3. Reset user choices
4. Output file name (default: ./data/output.csv)
5. Run (or r)
6. Exit (or q)
7. Print (or p)
```

### 1. Change the columns order

Displays the original headers for reference. Each header is associated with a number that you can use to specify the new column order.

**Note**: All column numbers must be included, and duplicates are allowed.

Example for [./data/input.csv](./data/input.csv)

```sh
New order: 3,4,1,2,5,6
```

### 2. Transform data

Displays the original headers as above, and allows you to select a transformation for a specific column.

```sh
You selected: user_id
Choose a transformation:
0. Reset to default
1. Convert UUIDs into simple integer sequence
2. Redact fields to replace data that is sensitive with similar looking random data
3. Conver timestamp to the appropriate date in the year-month-day format
Enter your choice:
```

### 3. Reset user choices

Resets all previously selected options.

### 4. Output file name

You can change the output file name from the default `./data/output.csv`.

**Note**: Since the app runs in a Docker container with a mounted volume at `./data`, make sure to use a relative path (e.g `./data/custom_output.csv`)

### 5. Run

Writes the output file based on your selected options. You can run this by typing `r` or `5`.

### 6. Exit

Exits the application. You can do this by typing `q` or `6`.

### 7. Print

Displays the current user choices. You can run this by typing `p` or `7`.

## Considerations

- If a transformation fails due to invalid data, a log message will be shown in the console and the original data will be written to the output file.

## How to scale

To handle large datasets (e.g. `1,000,000+ rows`) efficiently, I would keep the structure of `main.py` largely unchanged, while making targeted improvements to the data processing flow. Specifically:

- **Header Handling**: Read the CSV headers once at the beginning, as is currently done.
- **Chunked Processing**: During the run phase (`r` or `5`), process the input file in chunks (e.g. `1,000 rows` at a time) instead of loading the entire dataset into memory.
- **Modify CSVHeader Class**: Extend the class to support chunked reading and append-mode writing.
- **Streaming Transformations**: Apply the transformation logic within the chunk processing loop, operating only on the current chunk to minimize memory usage.
- **Incremental Writing**: Write each processed chunk directly to the output file in append mode, ensuring the application remains memory-efficient and responsive even with very large input files.

This approach allows the program to scale gracefully with available system resources and avoids memory bottlenecks, while maintaining the existing menu-driven interface and user experience.

In cases where I/O becomes a bottleneck or disk space is limited (e.g., with CSV files larger than 500 MB), it's possible to use Python’s built-in gzip module to read from or write to compressed .csv.gz files directly, without extracting them to disk and applying the chunk logic as well.
