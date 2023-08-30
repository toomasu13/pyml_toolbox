# ConfHandler Class

The `ConfHandler` class is a utility for managing configuration data stored in a dictionary and saving it in a JSON file. It enables users to read, write, update, and delete configuration data using intuitive methods.

## Class Overview

The `ConfHandler` class provides methods and attributes to:

- Load and save configuration data from/to a JSON file.
- Set and update configuration data with dictionaries.
- Retrieve configuration data.
- List keys or subkeys in the configuration data.
- Add, update, or delete key-value pairs in the configuration data.

## Example Usage

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
print(value)  # Output: {'a': 1, 'b': 2}

# List all keys in the configuration data
keys = conf_handler.list_keys()
print(keys)  # Output: ['v1', 'v2']

# Add a new key-value pair to the configuration data
conf_handler.set_key('v3', 'new_value')

# Delete a key-value pair from the configuration data
conf_handler.del_key('v1')

# Reset the configuration data to an empty dictionary
conf_handler.reset_conf()
```

## Class Methods

- `load_conf()`: Load the configuration data from the file and store it.
- `save_conf()`: Save the configuration data to the file.
- `set_conf(conf)`: Set the configuration data with a new dictionary and save it.
- `update_conf(conf)`: Update the configuration data with a dictionary and save it.
- `get_conf()`: Retrieve the full configuration data.
- `list_keys(key=None)`: List keys or subkeys in the configuration data.
- `set_key(key, value)`: Set or add a key-value pair.
- `del_key(key)`: Delete a key-value pair.
- `update_key(key, value)`: Update or add a key-value pair.
- `get_key(key, ret=None)`: Get the value of a key with an optional default value.
- `reset_conf()`: Clear the configuration data and save an empty dictionary.

---

For detailed usage and additional methods, refer to the class documentation in the code.