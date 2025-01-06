
import re
from pathlib import Path

from abc import ABC, abstractmethod

import json
import joblib

import pandas as pd

from .logger import init_logger


class PathHandler():
    """ A class to handle a file path.

        This class allows the user to set and get the components of a file path, such as the directory, the file name and the suffix.
        The user can also add additional directories to the path, check if the path exists, create or delete the path, and list the files in the path.

        Example
        Ph = PathHandler(file_dir='/tmp/test', file_name='script', file_suffix='sh')
        or
        Ph = PathHandler()
        Ph.path = '/tmp/test' # Stores file's directory
        Ph.file_name = 'script' # The name of the file
        Ph.suffix = 'sh' # The file's extension
        or
        Ph = PathHandler()
        Ph.file_path = '/tmp/test/script.sh' # The full path of the file
        are equivalent definitions of file path and return the same result
        Ph.file_path
        > /tmp/test/script.sh

        Attributes
        path : Path
            The directory of the file.
        file_name : str
            The name of the file without the suffix.
        suffix : str
            The extension of the file.
        name : str
            The name of the file with the suffix.
        file_path : Path
            The full path of the file as a Path object.

        Methods
        add_path(*args)
            Add additional directories to the file's directory.
        is_path()
            Return True if the file's directory exists.
        create_path()
            Create the file's directory if it does not exist.
        list_files(suffix=None, pattern=None, recursive=False, types=None)
            Return a list of files and directories in the path directory that match certain criteria.
        delete_file(path_file=None)
            Remove a file from the path directory.
        delete_dir(path_dir=None)
            Remove the directory. The directory must be empty.
        is_file()
            Return True if the path points to a file.
    """
    def __init__(self, file_dir=None, file_name=None, file_suffix=None, **kwargs):
        """ Initializes a PathHandler object with the given directory, file name and suffix.

            Parameters
            ----------
            file_dir : str or Path, optional
                The directory of the file. If None then the current working directory. If '@home' then the user's home directory. 
                If a string or a Path object that represents a full path of a file, then it will be parsed into its components. Default is None.
            file_name : str, optional
                The name of the file without the suffix. Default is None.
            file_suffix : str, optional
                The extension of the file. Default is None.
            **kwargs : dict, optional
                Additional keyword arguments for configuring the PathHandler object. See config() method for details.
            
        """
        self.logger = init_logger(self.__class__.__name__, level=kwargs.get('log_level', 20))
        
        if file_dir is not None and file_name is None and file_suffix is None:
            self.file_path = file_dir
        else: 
            self.path = file_dir
            self.file_name = file_name
            self.suffix = file_suffix
        self.config(**kwargs)
    
    def config(self, **kwargs):
        """ Configures additional parameters of PathHandler object.

            Parameters
            ----------
            multi_suffix : bool, default False
                When set to True, allows the file to have more than one suffix like 'file.tar.gz'. By default only one suffix is processed.
        """
        
        self._multi_suffix = False
        if kwargs.get('multi_suffix'):
            self._multi_suffix = kwargs.get('multi_suffix')
    
    @property
    def path(self):
        """ Returns or sets the directory of the file as a Path object.
        
        """
        return self._path_file
        
    @path.setter
    def path(self, file_dir=None):
        """ Returns or sets the directory of the file as a Path object.
        
        """
        
        if file_dir is None:
            self._path_file = Path.cwd()
        elif file_dir == '@home' or file_dir[0] = '~':
            self._path_file = Path.home()
        elif file_dir[0] != '/':
            self._path_file = Path.cwd().joinpath(file_dir)
        else:
            self._path_file = Path(file_dir)

    def add_path(self,  *args):
        """ Adds additional directories to the file's directory.

            Parameters
            ----------
            args : str or Path
                One or more strings or Path objects that represent directories to be added to the existing path.
        """
        args = tuple([ic for ic in args if isinstance(ic, str)])
        self._path_file = self._path_file.joinpath(*args)
    
    def is_path(self):
        """ Returns True if the file's directory exists.
        
        """
        return self.path.is_dir()
    
    def create_path(self):
        """ Creates the file's directory if it does not exist.
        
        """
        if not self.is_path():
            self.path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f'Directory created {self.path}')
    
    @property
    def suffix(self):
        """ Returns or sets the extension of the file as a string.
        
        """
        return self._file_suffix
        
    @suffix.setter
    def suffix(self, file_suffix=None):
        """ Returns or sets the extension of the file as a string.
        
        """
    
        if file_suffix is None:
            self._file_suffix = ''
        else:
            self._file_suffix = file_suffix
        
    @property
    def file_name(self):
        """ Returns or sets the name of the file without the suffix as a string.
        
        """
        
        return self._file_name
    
    @file_name.setter
    def file_name(self, file_name):
        """ Returns or sets the name of the file without the suffix as a string.
        
            Parameters
            ----------
            file_name: str
                The name of the file without the suffix 
        """
        
        self._file_name = file_name
    
    @property
    def name(self):
        """ Returns the name of the file with the suffix as a string.
            
            Returns
            -------
            file name: str
                The name of the file with the suffix.
        """
        
        return f'{self._file_name}.{self._file_suffix}'
    
    @property
    def file_path(self):
        """ Returns or sets the full path of the file as a Path object. 
            
            Returns
            -------
            path_file: Path
                The full path of the file
        """
#         return self.path.joinpath(self.name)
        if self.name is None:
            return self.path
        else:
            return self.path.joinpath(self.name)
    
    @file_path.setter
    def file_path(self, file_path):
        """ Returns or sets the full path of the file as a Path object.
            
            Parameters
            ----------
            file_path: str
                The full path of the file
        """
        
        path_file = Path(file_path)
        if path_file.suffixes and self._multi_suffix:
            self.path = path_file.parent
            self.file_name = Path(path_file.stem).stem.rstrip('.')
            self.suffix = ''.join([ic for ic in path_file.suffixes]).lstrip('.')
        elif path_file.suffix or file_path[-1] == '.':
            self.path = path_file.parent
            self.file_name = path_file.stem
            self.suffix = path_file.suffix.lstrip('.')
        else:
            self.path = path_file
    
    def list_files(self, suffix=None, pattern=None, recursive=False, types=None):
        """ Returns a list of files and directories in the path directory that match certain criteria.

            Parameters
            ----------
            suffix : str, optional
                The suffix pattern of the files to be listed. Default is None, which means all files.
            pattern : str, optional
                The regex pattern in the file name to be matched. Default is None, which means no pattern.
            recursive : bool, optional
                Whether to use recursive search in the subdirectories. Default is False.
            types : str, optional
                Whether to filter by directories 'd' or files 'f'. Default is None, which means both.

            Returns
            -------
            list
                A list of Path objects that represent the files and directories in the path directory that match the criteria. If no matches are found, returns an empty list.
        """
        if suffix:
            c_search = f'*.{suffix}'
        else:
            c_search = '*'
        
        if recursive:
            list_files = [ip for ip in self.path.rglob(c_search)]
        else:
            list_files = [ip for ip in self.path.glob(c_search)]
            
        if pattern: 
            list_files = [ip for ip in list_files if re.search(fr'{pattern}', ip.stem)]
        
        if types == 'd':
            list_files = [ip for ip in list_files if ip.is_dir()]
        elif types == 'f':
            list_files = [ip for ip in list_files if ip.is_file()]
            
        return list_files

    def delete_file(self, path_file=None):
        """ Removes a file from the path directory.

            Parameters
            ----------
            path_file : str or Path, optional
                The file to be removed. If not given, uses the file defined by the instance. Default is None.
        """
        if path_file is None:
            path_file = self.file_path
        else:
            if isinstance(path_file, str):
                path_file = Path(path_file)
        
        if path_file.is_file(): 
            path_file.unlink()
            self.logger.info(f'File deleted {path_file}')
        else:
            self.logger.info(f'File {path_file} not found for deleting')
            
    def delete_dir(self, path_dir=None):
        """ Removes the directory. The directory must be empty.

            Parameters
            ----------
            path_dir : str or Path, optional
                The directory to be removed. If not given, uses the directory defined by the instance. Default is None.
        """
        if path_dir is None:
            path_dir = self.path
        else:
            if isinstance(path_dir, str):
                path_dir = Path(path_dir)
        
        if path_dir.is_dir(): 
            path_dir.rmdir()
            self.logger.info(f'Directory deleted {path_dir}')
        else:
            self.logger.info(f'Directory {path_dir} not found for deleting')
            
    def is_file(self):
        """ Returns True if the path points to a file.
        
        """
        
        return self.file_path.is_file()

    def __str__(self):
        """ Returns string of the file path.
        
        """
        return str(self.file_path)
        

class FileHandler(ABC):
    """ An abstract class for file operations.
    
        This class defines the basic structure for reading and saving objects into files.
    """
    def __init__(self, path_file=None, log_level=20):
        """ Initializes a FileHandler object.
        
            Parameters
            ----------
            path_file : str or Path, optional
                The file path. Default is None.
            log_level : int, optional
                Level of logging. Default is 20 (INFO).
        """
        
        self.logger = init_logger(self.__class__.__name__, level=log_level)
        self.set_path(path_file)
            
    def set_path(self, path_file):
        """ Sets the file path.
        
            Parameters
            ----------
            path_file : str or Path
                The file path.
        """
        
        if isinstance(path_file, Path):
            self.path_file = path_file
        elif isinstance(path_file, str):
            self.path_file = Path(path_file)
        else:
            self.logger.debug(f'File path {path_file} should be str or Path')
            self.path_file = None

    @abstractmethod
    def read_object(self):
        """ Abstract method to read an object from a file.
        
        """
        pass
        
    @abstractmethod
    def write_object(self):
        """ Abstract method to write an object to a file.
        
        """
        pass
     
    def read(self, path_file=None, **kwargs):
        """ ead an object from a file.
        
            Parameters
            ----------
            path_file : str or Path, optional
                The file path. Default is None.
            **kwargs : dict
                Additional keyword arguments for reading.

            Returns
            -------
            obj : object or None
                The read object or None if reading fails.
        """
        
        if path_file:
            self.set_path(path_file)
        obj = None
        if self.path_file is None: 
            self.logger.info(f'File path not defined.')
        elif self.path_file.is_file(): 
            obj = self.read_object()
            self.logger.debug(f'File read {self.path_file}')
        else:
            self.logger.info(f'File {self.path_file} not found.')
        return obj

    def write(self, obj, path_file=None, **kwargs):
        """ Write an object to a file.
        
            Parameters
            ----------
            obj : object
                The object to be written.
            path_file : str or Path, optional
                The file path. Default is None.
            **kwargs : dict
                Additional keyword arguments for writing.
        """
        
        if path_file:
            self.set_path(path_file)
        
        if self.path_file is None: 
            self.logger.info(f'File path not defined.')
        else:
            result = self.write_object(obj, **kwargs)
            if result:
                self.logger.debug(f'Object {type(obj).__name__} saved to file {self.path_file}')
            else:
                self.logger.debug(f'Object {type(obj).__name__} not saved')

                
class JsonFile(FileHandler):
    """A class for performing JSON file operations.
    
        This class enables reading and writing JSON files.
    """      
    def np_encoder(self, obj):
        """ Custom NumPy encoder function to handle NumPy data types.
        
        """
        if isinstance(obj, np.generic):
            return obj.item()
        
    def read_object(self, **kwargs):
        """ Reads a dictionary from a JSON file.
        
            Returns
            -------
            obj : dict
                The dictionary read from the JSON file.
        """
        
        with open(str(self.path_file), 'rb') as file:  
            obj = json.load(file)
        return obj

    def write_object(self, obj, **kwargs):
        """ Write a dictionary to a JSON file.
        
            Parameters
            ----------
            obj : dict
                The dictionary object to be written.
        """
        
        is_success = False
        if isinstance(obj, dict):
            with open(str(self.path_file), 'w') as file:  
                json.dump(obj, file, default=self.np_encoder)
            is_success = True
        else:
            self.logger.info(f'Expecting dictionary object')
        return is_success
        

class CsvFile(FileHandler):
    """ A class for reading and writing CSV files using Pandas DataFrame.
    
        This class provides functionalities to read and write CSV files as Pandas DataFrames.
    """
        
    def read_object(self, **kwargs):
        """ Reads a CSV file into a Pandas DataFrame.
        
            Returns
            -------
            obj : pandas.DataFrame
                The DataFrame read from the CSV file.
        """
        
        obj = pd.read_csv(self.path_file, **kwargs)
        return obj

    def write_object(self, obj, **kwargs):
        """ Write a Pandas DataFrame to a CSV file.
        
            Parameters
            ----------
            obj : pandas.DataFrame
                The DataFrame to be written.
        """
        
        is_success = False
        if isinstance(obj, pd.DataFrame):
            obj.to_csv(self.path_file, **kwargs)
            is_success = True
        else:
            self.logger.info(f'Expecting Pandas DataFrame ')
        return is_success
    
    
class ParquetFile(FileHandler):
    """ A class for reading and writing Parquet files using Pandas DataFrame.
    
        This class provides functionalities to read and write Parquet files as Pandas DataFrames.
    """
        
    def read_object(self, **kwargs):
        """ Reads a Parquet file into a Pandas DataFrame.
        
            Returns
            -------
            obj : pandas.DataFrame
                The DataFrame read from the Parquet file.
        """
        
        obj = pd.read_parquet(self.path_file, **kwargs)
        return obj

    def write_object(self, obj, **kwargs):
        """ Write a Pandas DataFrame to a Parquet file.
        
            Parameters
            ----------
            obj : pandas.DataFrame
                The DataFrame to be written.
        """
        
        is_success = False
        if isinstance(obj, pd.DataFrame):
            obj.to_parquet(self.path_file, **kwargs)
            is_success = True
        else:
            self.logger.info(f'Expecting Pandas DataFrame ')
        return is_success
    
        
        


        
