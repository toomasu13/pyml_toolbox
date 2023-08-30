
# PyML_Toolbox

PyML_Toolbox (Python Machine Learning Toolbox) is a Python package designed to assist data scientists and Jupyter notebook users in securely handling credentials, database connections, and file operations. This toolbox offers a collection of classes and functions that simplify various tasks related to data processing and management.

## Installation

You can install the PyML Toolbox package using pip:

```bash
pip install pyml_toolbox
```

## Classes and Functions

### Engine Class

The `Engine` class enables seamless management of stored logins, database engine configurations, and query executions.

Example Usage:

```python
from pyml_toolbox import Engine

# Initialize an Engine object with optional parameters
E = Engine(dir_engine='/file/path', is_encode=True, log_level=20)

# Add a new login credential for a database source
E.set_login(login='snowflake', user='name', password='pw')

# Set the URL template for a database driver
E.set_driver('snowflake', url='{driver}://{user}:{password}@{host}/{database}/{schema}?role={role}&warehouse={warehouse}')

# Add a new engine parameter for a database source
dict_snowflake = {
    'driver': 'snowflake',
    'login': 'snowflake',
    'host': 'snowflake.host',
    'database': 'db',
    'schema': 'sc',
    'warehouse': 'wh',
    'role': 'user_role'
}
E.set_engine('snowflake', **dict_snowflake)

# Execute a query in a database engine and retrieve the result as a DataFrame
query = '''
    SELECT 1
'''
df = E.from_sql(query, 'snowflake')
```

### ConfHandler Class

The `ConfHandler` class is designed for handling configuration data stored in a dictionary and saving it in a JSON file.

Example Usage:

```python
from pyml_toolbox import ConfHandler

# Initialize a ConfHandler object with a configuration file
conf_handler = ConfHandler(file_conf='conf1.json', log_level=20)

# Set initial configuration data
conf_handler.set_conf({'v1': 1, 'v2': {'a': 1, 'b': 3}})

# Update a key in the configuration data
conf_handler.update_key('v2', {'b': 2})

# Get the value of a key in the configuration data
value = conf_handler.get_key('v2')
```

### PathHandler Class

The `PathHandler` class simplifies file path handling, including setting and getting components of a file path, adding additional directories, checking path existence, and more.

Example Usage:

```python
from pyml_toolbox import PathHandler

# Initialize a PathHandler object with file components
path_handler = PathHandler(file_dir='/tmp/test', file_name='script', file_suffix='sh')

# Add additional directories to the path
path_handler.add_path('subdir1')

# Check if the file's directory exists and create it if not
if not path_handler.is_path():
    path_handler.create_path()
```

### JsonFile Class

The `JsonFile` class provides functions for performing JSON file operations.

Example Usage:

```python
from pyml_toolbox import JsonFile

# Initialize a JsonFile object
json_file = JsonFile('data.json')

# Write a dictionary to the JSON file
data = {'name': 'John', 'age': 30}
json_file.write(data)

# Read the JSON file and retrieve the dictionary
read_data = json_file.read()
```

### CsvFile Class

The `CsvFile` class simplifies reading and writing CSV files using Pandas DataFrame.

Example Usage:

```python
from pyml_toolbox import CsvFile
import pandas as pd

# Initialize a CsvFile object
csv_file = CsvFile('data.csv')

# Write DataFrame to CSV file
df = pd.DataFrame({'name': ['John', 'Jane'], 'age': [30, 25]})
csv_file.write(df)

# Read CSV file into a Pandas DataFrame
read_df = csv_file.read()
```

### ParquetFile Class

The `ParquetFile` class facilitates reading and writing Parquet files using Pandas DataFrame.

Example Usage:

```python
from pyml_toolbox import ParquetFile
import pandas as pd

# Initialize a ParquetFile object
parquet_file = ParquetFile('data.parquet')

# Write DataFrame to Parquet file
df = pd.DataFrame({'name': ['John', 'Jane'], 'age': [30, 25]})
parquet_file.write(df)

# Read Parquet file into a Pandas DataFrame
read_df = parquet_file.read()
```

### init_logger Function

The `init_logger` function initializes a logger within a Jupyter notebook and returns a logger with the specified name.

Example Usage:

```python
from pyml_toolbox import init_logger

# For example, initiate a logger inside a class
self.logger = init_logger(self.__class__.__name__, level=log_level)
```

## License

PyML_Toolbox is licensed under the GNU General Public License v3 (GPLv3).

## TODOs

- Add a simple model registry which stores time, data, hyperparameters, and other relevant features of the model training process.