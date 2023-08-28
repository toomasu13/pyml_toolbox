# PathHandler Class

The `PathHandler` class is a utility for handling file paths. It allows users to set and get various components of a file path, manage directories, and perform file-related operations.

## Class Overview

The `PathHandler` class provides methods and attributes to:

- Set and retrieve the file's directory, name, and suffix.
- Add additional directories to the file's directory.
- Check if the file's directory exists and create it if not.
- List files and directories in the path directory based on specific criteria.
- Delete files and directories from the path.
- Check if the path points to a file.

## Example Usage

```python
from path_handler import PathHandler

# Initialize a PathHandler object with file components
path_handler = PathHandler(file_dir='/tmp/test', file_name='script', file_suffix='sh')

# Add additional directories to the path
path_handler.add_path('subdir1', 'subdir2')

# Check if the file's directory exists and create it if not
if not path_handler.is_path():
    path_handler.create_path()

# List files in the path directory with a specific suffix and pattern
files = path_handler.list_files(suffix='sh', pattern='script', recursive=True, types='f')
print(files)

# Delete a specific file
file_to_delete = '/tmp/test/subdir1/subdir2/script.sh'
path_handler.delete_file(file_to_delete)

# Check if the path points to a file
if path_handler.is_file():
    print(f'The path points to a file: {path_handler}')
else:
    print(f'The path does not point to a file: {path_handler}')

# Print the full file path
print(f'Full file path: {path_handler.file_path}')
```

## Class Attributes

- `path`: The directory of the file.
- `file_name`: The name of the file without the suffix.
- `suffix`: The extension of the file.
- `name`: The name of the file with the suffix.
- `file_path`: The full path of the file as a `Path` object.

## Class Methods

- `add_path(*args)`: Add additional directories to the file's directory.
- `is_path()`: Check if the file's directory exists.
- `create_path()`: Create the file's directory if it does not exist.
- `list_files(suffix=None, pattern=None, recursive=False, types=None)`: List files and directories in the path directory based on criteria.
- `delete_file(path_file=None)`: Delete a file from the path directory.
- `delete_dir(path_dir=None)`: Delete a directory (must be empty).
- `is_file()`: Check if the path points to a file.

## License

This project is licensed under the [MIT License](LICENSE).

---

For detailed usage and additional methods, refer to the class documentation in the code.