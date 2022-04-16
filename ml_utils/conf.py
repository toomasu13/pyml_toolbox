#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 13:49:23 2021

@author: toomaskirt
"""

import json
from pathlib import Path

from .logger import init_logger



class ConfHandler:
    """
        A class used to handle conf files

        Parameters
        ----------
        dir_conf : str, list of strings, default cwd
            a directory of the conf file 
        file_conf : str, default 'conf'
            the name of the conf file
        log_level : int, Default Info
            the log level

        Methods
        -------
        set_conf(conf)
            Changes conf and saves
        set_key(key, value)
            Changes a key value in a conf
        get_conf()
            Get conf
        get_key(key)
            Get key value from conf
    """
    
    def __init__(self, dir_conf=None, file_conf=None, log_level=20):
        
        self.logger = init_logger('ConfFile', level=log_level)
        self.conf = {}
        self.file_ext = 'json'
        self.set_path(dir_conf)
        self.set_file_path(file_conf)
        self.load_conf()
    
    def set_path(self, dir_conf):
        
        if isinstance(dir_conf, list):
            self.path_data = Path.home().joinpath(*dir_conf,)
        elif isinstance(dir_conf, str):
            self.path_data = Path.home().joinpath(dir_conf)
        else:
            self.path_data = Path.cwd()
            
        if not self.path_data.is_dir():
            self.path_data.mkdir(parents=True, exist_ok=True)
            
        self.logger.debug(f'Conf path {self.path_data}')
    
    def set_file_path(self, file_name):
        
        if file_name is None:
            file_name = 'conf'
            
        file_name = f'{file_name}.{self.file_ext}'
        
        self.path_file = self.path_data.joinpath(file_name)
        self.logger.debug(f'Conf file path {self.path_file}')
    
    def load_conf(self):
        
        if self.path_file.is_file(): 
            with open(str(self.path_file), 'rb') as file:  
                self.conf = json.load(file)
                self.logger.debug(f'File read {self.path_file}')
        else:
            self.logger.info(f'File {self.path_file} not found. Empty conf')
                
    def save_conf(self):
        
        with open(str(self.path_file), 'w') as file:  
            json.dump(self.conf, file)
            self.logger.debug(f'File saved {self.path_file}')
    
    def set_conf(self, conf):
        
        if isinstance(conf, dict):
            self.conf.update(conf)
            self.save_conf()
        else:
            self.logger.info('Input was not a dictionary type')
    
    def set_key(self, key, value):
        
        if self.conf.get(key) is None:
            self.conf[key] = value
        else:
            if isinstance(self.conf[key], dict) and isinstance(value, dict):
                self.conf[key].update(value)
            else:
                self.conf[key] = value
        self.save_conf()
    
    def get_conf(self):
        
        return self.conf
    
    def get_key(self, key, ret=None):
        
        return self.conf.get(key, ret)