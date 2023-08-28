
import json
from pathlib import Path

from .logger import init_logger
from .files import JsonFile


class ConfHandler:
    """ A class to handle configuration stored in a dictionary and save it in a JSON file.
        This class allows the user to read, write, update, delete and get configuration data from a file.
        The configuration data is stored as a dictionary in the class attribute and the file.
        The file is saved automatically after every change in the configuration data.
        
        Example
        Ch = ConfHandler(file_conf='conf1.json', log_level=20)
        Ch.set_conf({'v1': 1, 'v2': {'a': 1, 'b': 3}})
        Ch.update_key('v2', {'c': 3, 'b': 2})
        Ch.get_key('v2')
        > {'a': 1, 'b': 2, 'c': 3}

        Parameters
        ----------
        file_conf : str, optional
            The file path of the configuration file. Default is 'conf.json' in the current directory.
        log_level : int, optional
            The log level. Default is 20 (INFO).

        Methods
        -------
        load_conf()
            Loads the configuration data from the file and stores it in the _conf attribute.
        save_conf()
            Saves the configuration data from the _conf attribute to the file.
        set_conf(conf)
            Replaces the configuration data with the given dictionary and saves it to the file.
        update_conf(conf)
            Updates the configuration data with the given dictionary and saves it to the file.
        get_conf()
            Returns the full configuration data as a dictionary.
        list_keys(key=None)
            Returns a list of keys or subkeys in the configuration data. If no keys are found, returns an empty list.
        set_key(key, value)
            Sets or adds a key-value pair in the configuration data and saves it to the file.
        del_keykey
            Deletes a key-value pair from the configuration data and saves it to the file.
        update_key(key, value)
            Updates or adds a key-value pair in the configuration data and saves it to the file.
        get_key(key, ret=None)
            Returns the value of a key in the configuration data. If the key is not found, returns a default value or None.
        reset_conf()
            Clears the configuration data and saves an empty dictionary to the file.
    """
    
    def __init__(self, file_conf=None, log_level=20):
        """ Initializes the ConfHandler object with the given file path and log level.

            Parameters
            ----------
            file_conf : str, optional
                The file path of the configuration file. Default is 'conf.json' in the current directory.
            log_level : int, optional
                The log level. Default is 20 (INFO).
        """
        
        self.logger = init_logger(self.__class__.__name__, level=log_level)
        
        self._conf = {}
        if file_conf is None:
            file_conf = 'conf.json'
        self._file = JsonFile(path_file=file_conf, log_level=log_level)
        self.load_conf()
    
    def load_conf(self):
        """ Loads the configuration data from the file and stores it in the _conf attribute.
        
        """
        
        self._conf = self._file.read()

    def save_conf(self):
        """ Saves the configuration data from the _conf attribute to the file.
        
        """
        
        self._file.write(self._conf)
    
    def set_conf(self, conf):
        """ Replaces the configuration data with the given dictionary and saves it to the file.
        
            Parameters
            ----------
            conf : dict
                The new configuration data as a dictionary.
        """
        
        if isinstance(conf, dict):
            self._conf = conf
            self.save_conf()
        else:
            self.logger.info('Input was not a dictionary type')
    
    def update_conf(self, conf):
        """ Updates the configuration data with the given dictionary and saves it to the file.
            
            Parameters
            ----------
            conf : dict
                The dictionary of key-value pairs to update or add to the configuration data.
        """
        
        if isinstance(conf, dict):
            self._conf.update(conf)
            self.save_conf()
        else:
            self.logger.info('Input was not a dictionary type')
    
    def get_conf(self):
        """ Returns the full configuration data as a dictionary.
        
            Returns
            -------
            dict
                The configuration data.      
        """
        
        return self._conf
    
    def list_keys(self, key=None):
        """ Returns a list of keys or subkeys in the configuration data. If no keys are found, returns an empty list.
        
            Parameters
            ----------
            The key to get the subkeys from. If not given, returns the top-level keys. Default is None.
            
            Returns
            -------
            list
                The list of keys or subkeys. If the key is not found or the value is not a dictionary, returns an empty list.
        """
        if key is None:
            out = self._conf
        else:
            out = self._conf.get(key, {})
        out = out if isinstance(out, dict) else {}
        return list(out)
    
    def set_key(self, key, value):
        """ Sets or adds a key-value pair in the configuration data and saves it to the file.
        
            Parameters
            ----------
            key : str or int
                The key to set or add.
            value : any
                The value to assign to the key.
        """
        
        self._conf[key] = value
        self.save_conf()
    
    def del_key(self, key):
        """ Deletes a key-value pair from the configuration data and saves it to the file.
        
            Parameters
            ----------
            key : str or int
                The key to delete.
        """
        if key in self._conf:
            del self._conf[key]
            self.logger.info(f'Key {key} deleted')
            self.save_conf()
    
    def update_key(self, key, value):
        """ Updates or adds a key-value pair in the configuration data and saves it to the file.
        
            Parameters
            ----------
            key : str or int
                The key to update or add.
            value : any
                The value to assign to the key.
        """
        
        if self._conf.get(key) is None:
            self._conf[key] = value
        else:
            if isinstance(self._conf[key], dict) and isinstance(value, dict):
                self._conf[key].update(value)
            else:
                self._conf[key] = value
        self.save_conf()
    
    def get_key(self, key, ret=None):
        """ Returns the value of a key in the configuration data. If the key is not found, returns a default value or None.
        
            Parameters
            Returns
            any
            The value of the key in the configuration data. If the key is not found, returns ret or None.
        
            Parameters
            ----------
            key : str or int
                The key to get the value from.
            ret : any, optional
                The default value to return if the key is not found. Default is None.
            Returns
            -------
            any
                The value of the key in the configuration data. If the key is not found, returns ret or None.
        """
        
        return self._conf.get(key, ret)
    
    def reset_conf(self):
        """ Clears the configuration data and saves an empty dictionary to the file.
        
        """
        
        self._conf = {}
        self.save_conf()

