Certainly! Here's a Markdown format README that describes the provided classes and includes examples of how to use them:

# File Handling Classes

This repository contains Python classes for handling various file operations, including reading and writing JSON, CSV, and Parquet files. These classes provide a convenient and structured way to work with different file formats.

## Classes

### `FileHandler` (Abstract Class)

An abstract class that defines the basic structure for reading and saving objects into files.

```python
class FileHandler(ABC):
    # ... (class description, constructor, and abstract methods)
    # ...
```

#### Methods

- `set_path(path_file)`
- `read_object()`
- `write_object(obj)`
- `read(path_file=None, **kwargs)`
- `write(obj, path_file=None, **kwargs)`

### `JsonFile`

A class for performing JSON file operations.

```python
class JsonFile(FileHandler):
    # ... (class description and methods)
    # ...
```

#### Methods

- `read_object(**kwargs)`
- `write_object(obj, **kwargs)`

### `CsvFile`

A class for reading and writing CSV files using Pandas DataFrame.

```python
class CsvFile(FileHandler):
    # ... (class description and methods)
    # ...
```

#### Methods

- `read_object(**kwargs)`
- `write_object(obj, **kwargs)`

### `ParquetFile`

A class for reading and writing Parquet files using Pandas DataFrame.

```python
class ParquetFile(FileHandler):
    # ... (class description and methods)
    # ...
```

#### Methods

- `read_object(**kwargs)`
- `write_object(obj, **kwargs)`

## Usage Examples

### Using the `JsonFile` class

```python
from file_handlers import JsonFile

# Initialize a JsonFile object
json_file = JsonFile('data.json')

# Write a dictionary to the JSON file
data = {'name': 'John', 'age': 30}
json_file.write(data)

# Read the JSON file and retrieve the dictionary
read_data = json_file.read()

print(read_data)  # Output: {'name': 'John', 'age': 30}
```

### Using the `CsvFile` class

```python
from file_handlers import CsvFile
import pandas as pd

# Initialize a CsvFile object
csv_file = CsvFile('data.csv')

# Create a Pandas DataFrame
data = {'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 32, 28]}
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
csv_file.write(df)

# Read the CSV file and retrieve the DataFrame
read_df = csv_file.read()

print(read_df)
```

### Using the `ParquetFile` class

```python
from file_handlers import ParquetFile
import pandas as pd

# Initialize a ParquetFile object
parquet_file = ParquetFile('data.parquet')

# Create a Pandas DataFrame
data = {'name': ['Emily', 'David', 'Eva'],
        'age': [22, 29, 24]}
df = pd.DataFrame(data)

# Write the DataFrame to a Parquet file
parquet_file.write(df)

# Read the Parquet file and retrieve the DataFrame
read_df = parquet_file.read()

print(read_df)
```

## License

This project is licensed under the [MIT License](LICENSE).
