# import sys
import json
from pathlib import Path
import joblib
# import pickle
import re
from functools import wraps

import pandas as pd

import matplotlib.pyplot as plt

from .conf import ConfHandler
from .logger import init_logger
# from .s3handler import S3Handler
# from .awshandler import AwsHandler



class Files():
    """
        A class to conduct file operations. 
        Reads and saves files. 
    """
    def __init__(self, c_name='', dir_data=None, file_ext=None, file_log=None):
        """ 
            Parameters
            ----------
            c_name: str
                The name of the class 
            dir_data: str
                Directory for the data files. If None then cwd()/Data/<c_project>
            file_ext: str
                The default file extension
        """
        
        conf_toolbox = ConfHandler(dir_conf='.ml_toolbox', file_conf='ml_toolbox').get_conf()
        log_level = conf_toolbox.get('log_level', 20)
        self.is_s3 = conf_toolbox.get('is_s3', True)
        
        self.logger = init_logger('Files', level=log_level, file=file_log)
        
        self.s3 = None
        if self.is_s3:
            self.s3 = S3Handler(file_log=file_log)
        
        self.file_ext = file_ext
        self.file_name = None
        
        if dir_data is None:
            dir_data = Path.cwd()
            
        if not Path(dir_data).is_dir():
            Path(dir_data).mkdir(parents=True, exist_ok=True)
            
        self.path_data = Path(dir_data)
        self.logger.debug('Working directory of {} is set {} '.format(c_name, str(self.path_data)))
        
    def create_file_name(self, file_name, file_ext=None):
        """
            Creates a path to the file. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_ext: str
                The file extension
            Returns
            -------
            path_file: Path
                a path to the file
        """
        if file_ext is None:
            file_ext = self.file_ext
        file_name = f'{file_name}.{file_ext}'
        
        return self.path_data.joinpath(file_name)
        
    def df_from_parquet(self, file_name):
        """
            Load a parquet object, returning a DataFrame. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            Returns
            -------
            df: DataFrame
                dataframe of the data
        """
        file_name = f'{file_name}.parquet.gzip'
        path_file = self.path_data.joinpath(file_name)
        
        df = None
        if path_file.is_file(): 
            df = pd.read_parquet(path_file)
            self.logger.info('File read {}'.format(path_file))
        else:
            self.logger.error('File {} not found'.format(path_file))
        return df
    
    def df_to_parquet(self, df, file_name): 
        """
            Write a DataFrame to the binary parquet format. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            df: DataFrame
                dataframe of the data
        """
        file_name = f'{file_name}.parquet.gzip'
        path_file = self.path_data.joinpath(file_name)
        
        df.to_parquet(path_file, compression='gzip', index=False)
        self.logger.info('File saved {}'.format(path_file))
        
    def obj_from_bin(self, obj, file_name): 
        """
            Load a xgboost model.
            
            Parameters
            ----------
            obj: a xgboost model
                The xgboost model stored in the file.
            file_name: str
                The file name from which to load the object 
            Returns
            -------
            obj: a xgboost model
                The xgboost model stored in the file.
        """
        
        file_name = f'{file_name}.bin'
        path_file = self.path_data.joinpath(file_name)
        
        if path_file.is_file(): 
            obj.load_model(str(path_file))
            self.logger.info('File read {}'.format(path_file))
        else:
            self.logger.error('File {} not found'.format(path_file))
            
        return obj
      
    def obj_to_bin(self, obj, file_name):
        """
            Write a xgboost model into a file.
            
            Parameters
            ---------- 
            obj: a xgboost model
                The xgboost model to store to the file.
            file_name: str
                The file name from which to load the object
        """
        
        file_name = f'{file_name}.bin'
        path_file = self.path_data.joinpath(file_name)
        
        obj.get_booster().save_model(str(path_file))
        self.logger.info('File saved {}'.format(path_file))
            
    def obj_from_pkl(self, file_name): 
        """
            Load a pkl file. Reconstruct a Python object from a file persisted with joblib.dump.
            
            Parameters
            ----------
            file_name: str
                The file name from which to load the object 
            Returns
            -------
            obj: any Python object
                The object stored in the file.
        """
        
        file_name = f'{file_name}.pkl'
        path_file = self.path_data.joinpath(file_name)
        
        obj = None
        if path_file.is_file(): 
            with open(str(path_file), 'rb') as file:  
                obj = joblib.load(file)
                self.logger.info('File read {}'.format(path_file))
        else:
            self.logger.error('File {} not found'.format(path_file))
            
        return obj
      
    def obj_to_pkl(self, obj, file_name):
        """
            Write a Ptyon object into a file. 
            
            Parameters
            ----------
            obj: any Python object
                The object to store to disk.
            file_name: str
                The file name in which it is to be stored. 
        """
        
        file_name = f'{file_name}.pkl'
        path_file = self.path_data.joinpath(file_name)
        
        with open(str(path_file), 'wb') as file:  
            joblib.dump(obj, file)
            self.logger.info('File saved {}'.format(path_file))
            
    def dict_from_json(self, file_name):
        """
            Load a json file into a Python dictonary. 
            
            Parameters
            ----------
            file_name: str
                The file name from which to load the json 
            Returns
            -------
            obj: a Python dictonary
                The dictonary stored in the file.
        """
        
        file_name = f'{file_name}.json'
        path_file = self.path_data.joinpath(file_name)
        
        obj = None
        if path_file.is_file(): 
            with open(str(path_file), 'rb') as file:  
                obj = json.load(file)
                self.logger.info('File read {}'.format(path_file))
        else:
            self.logger.error('File {} not found'.format(path_file))
            
        return obj
      
    def dict_to_json(self, obj, file_name):
        """
            Write a Ptyon dictonaty into a json file. 
            
            Parameters
            ----------
            obj: dict
                The dictonary to store to disk.
            file_name: str
                The file name in which it is to be stored. 
        """
        
        file_name = f'{file_name}.json'
        path_file = self.path_data.joinpath(file_name)
        
        with open(str(path_file), 'w') as file:  
            json.dump(obj, file)
            self.logger.info('File saved {}'.format(path_file))
            
    def save_fig(self, file_name, dpi=300):
        """
            Save the current figure in a png format. 
            
            Parameters
            ----------
            file_name: str
                The file name in which it is to be stored.
            dpi: int
                The resolution in dots per inch. 
        """
        
        file_name = f'{file_name}.png'
        path_file = self.path_data.joinpath(file_name)
        
        plt.tight_layout()
        plt.savefig(str(path_file), dpi=dpi) 
    
    def delete_file(self, file_name, file_ext=None):
        """
            Removes a file. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_ext: str
                The file extension
        """
        path_file = self.create_file_name(file_name, file_ext)
        if path_file.is_file(): 
            path_file.unlink()
            self.logger.info('File deleted {}'.format(path_file))
        else:
            self.logger.info('File {} not found'.format(path_file))
       
    def file_to_s3(self, file_name, file_object, file_ext=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_object: str
                The object name of the file in S3
            file_ext: str
                The file extension
        """
        if self.is_s3:
            path_file = self.create_file_name(file_name, file_ext)
            if path_file.is_file(): 
                self.s3.upload_file(str(path_file), file_object)
                self.logger.info(f'File {path_file} uploaded {file_object}')
            else:
                self.logger.info(f'File {path_file} not found')
        else:
            self.logger.info(f'S3 disabled')
                               
    def file_from_s3(self, file_object, file_name, file_ext=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_object: str
                The object name of the file in S3
            file_name: str
                The name of the file 
            file_ext: str
                The file extension
        """
        if self.is_s3:
            path_file = self.create_file_name(file_name, file_ext)
            self.s3.download_file(str(path_file), file_object)
            self.logger.info(f'File {file_object} downloaded {path_file}')
        else:
            self.logger.info(f'S3 disabled')
        

class PathHandler():
    def __init__(self, file_dir=None, file_name=None, file_suffix=None):
        """ 
            Handles file path and name. 
            Parameters
            ----------
            file_dir: str
                Directory for the files. If None then the active directory cwd(), if @home then the users home directory
            file_name: str
                The name of the file 
            file_suffix: str
                The default file extension
        """
        
        if file_dir is not None and file_name is None and file_suffix is None:
            self.file_path = file_dir
        else: 
            self.path = file_dir
            self.file_name = file_name
            self.suffix = file_suffix
    
    @property
    def path(self):
        
        return self.path_file
        
    @path.setter
    def path(self, file_dir=None):
        
        if file_dir is None:
            self.path_file = Path.cwd()
        elif file_dir == '@home':
            self.path_file = Path.home()
        else:
            self.path_file = Path(file_dir)

    def add_path(self,  *args):
        
        args = tuple([ic for ic in args if isinstance(ic, str)])
        self.path_file = self.path_file.joinpath(*args)
    
    def is_path(self):
        
        return self.path.is_dir()
    
    def create_path(self):
        
        if not self.is_path():
            self.path.mkdir(parents=True, exist_ok=True)
    
    @property
    def suffix(self):
        
        return self.file_suffix
        
    @suffix.setter
    def suffix(self, file_suffix=None):
    
        if file_suffix is None:
            self.file_suffix = ''
        else:
            self.file_suffix = file_suffix
        
    @property
    def file_name(self):
        
        return self._file_name
    
    @file_name.setter
    def file_name(self, file_name):
        
        self._file_name = file_name
    
    @property
    def name(self):
        
        return f'{self._file_name}.{self.file_suffix}'
    
    @property
    def file_path(self):
        """
            Creates a path to the file. 
            
            Parameters
            ----------
            file_name: str
                
            file_suffix: str
                The file extension
            Returns
            -------
            path_file: Path
                a path to the file
        """
        return self.path.joinpath(self.name)
    
    @file_path.setter
    def file_path(self, file_path):
        
        path_file = Path(file_path)
        self.path = path_file.parent
        self.file_name = Path(path_file.stem).stem.rstrip('.')
        self.suffix = ''.join([ic for ic in path_file.suffixes]).lstrip('.')
    
    def is_file(self):
        
        return self.file_path.is_file()

    def __str__(self):
        
        return str(self.file_path)
        

class FHandler():
    """
        A class to conduct file operations. 
        Reads and saves files. 
    """
    def __init__(self, file_dir=None, file_name=None, file_suffix=None, out_dir=None, out_name=None, c_s3=None, c_aws=None, file_log=None):
        """ 
            Parameters
            ----------
            c_name: str
                The name of the class 
            dir_data: str
                Directory for the data files. If None then cwd()/Data/<c_project>
            file_suffix: str
                The default file extension
        """
        
        conf_toolbox = ConfHandler(dir_conf='.ml_toolbox', file_conf='ml_toolbox').get_conf()
        log_level = conf_toolbox.get('log_level', 20)
#         self.is_s3 = conf_toolbox.get('is_s3', True)
#         self.is_aws = conf_toolbox.get('is_aws', True)
        
        self.logger = init_logger('Files', level=log_level, file=file_log)
        
        self.s3 = None
        self.is_s3 = False
        if self.is_s3:
            self.init_s3(c_conf=c_s3, file_log=file_log)
            self.is_s3 = True
        
        self.aws = None
        self.is_aws = False
        if self.is_aws:
            self.init_aws(c_conf=c_aws, file_log=file_log)
            self.is_aws = True
        
        self.set_file(file_dir=file_dir, file_name=file_name, file_suffix=file_suffix)
        self.set_out_file(out_dir=out_dir, out_name=out_name, out_suffix=file_suffix)
        
    def set_file(self, file_dir=None, file_name=None, file_suffix=None):
        
        self.local_path = PathHandler(file_dir=file_dir, file_name=file_name, file_suffix=file_suffix)
        if not self.local_path.is_path():
            path_file = self.local_path.get_path()
            path_file.mkdir(parents=True, exist_ok=True)
            self.logger.info(f'Directory created {path_file}')
            
    def set_out_file(self, out_dir=None, out_name=None, out_suffix=None):
    
        self.out_path = None
        if out_dir is not None:
            if out_name is None: 
                out_name = self.local_path.get_file_name()
            if out_suffix is None:
                out_suffix = self.local_path.get_suffix()
            self.out_path = PathHandler(file_dir=out_dir, file_name=out_name, file_suffix=out_suffix)
    
    def search_files(self, pattern=None):
        
        if pattern is None: 
            return self.local_path.get_path().glob(f'*.{self.file_suffix}')
        else:
            return [ip for ip in self.local_path.get_path().glob(f'*.{self.file_suffix}') if re.search(fr'{pattern}', ip.stem)]

    def delete_file(self, path_file=None):
        """
            Removes a file. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_ext: str
                The file extension
        """
        if path_file is None:
            path_file = self.local_path.file_path
        
        if path_file.is_file(): 
            path_file.unlink()
            self.logger.info('File deleted {}'.format(path_file))
        else:
            self.logger.info('File {} not found'.format(path_file))
    
    def reading_file(self, path_file):
        
        return path_file.read_bytes()

    def saving_file(self, obj, path_file):
        
        path_file.write_bytes(obj)

    def read_file(self, file_name=None):
        
        if file_name is not None:
            self.local_path.set_file_name(file_name)
        path_file = self.local_path.file_path
        obj = None
        if path_file.is_file(): 
            obj = self.reading_file(path_file)
            self.logger.info(f'File read {path_file}')
        else:
            self.logger.error(f'File {path_file} not found')
        return obj
    
    def save_file(self, obj, file_name=None):
        
        if file_name is not None:
            self.local_path.set_file_name(file_name)
        
        path_file = self.local_path.file_path
        self.saving_file(obj, path_file)
        self.logger.info(f'File savad {path_file}')
    
    def init_s3(self, c_conf=None, file_log=None):
        
        self.s3 = S3Handler(c_conf=c_conf, file_log=file_log)
        
    def to_s3(self, file_object=None, file_name=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_object: str
                The object name of the file in S3
            file_ext: str
                The file extension
        """
        if self.is_s3:
            if file_name is not None:
                self.local_path.set_file_name(file_name)
                self.out_path.set_file_name(file_name)
            path_file = self.local_path.file_path
            
            if file_object is not None:
                self.out_path.set_file_name(file_object)
            path_object = self.out_path.file_path
            
            if path_file.is_file(): 
                self.s3.upload_file(str(path_file), str(path_object))
                self.logger.info(f'File {path_file} uploaded {path_object}')
            else:
                self.logger.info(f'File {path_file} not found')
        else:
            self.logger.info(f'S3 disabled')
                               
    def from_s3(self, file_object=None, file_name=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_object: str
                The object name of the file in S3
            path_file: str
                The name of the file 
        """
        if self.is_s3:
            if file_name is not None:
                self.local_path.set_file_name(file_name)
                self.out_path.set_file_name(file_name)
            path_file = self.local_path.file_path
            
            if file_object is not None:
                self.out_path.set_file_name(file_object)
            path_object = self.out_path.file_path
            
            self.s3.download_file(str(path_object), str(path_file))
            self.logger.info(f'File {path_object} downloaded {path_file}')
        else:
            self.logger.info(f'S3 disabled')
        
    def init_aws(self, c_conf=None, file_log=None):
        
        self.aws = AwsHandler(c_name=c_conf, file_log=file_log)
        
    def to_aws(self, file_object=None, file_name=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_name: str
                The name of the file 
            file_object: str
                The object name of the file in the aws instance
        """
        if self.is_aws:
            if file_name is not None:
                self.local_path.set_file_name(file_name)
                self.out_path.set_file_name(file_name)
            path_file = self.local_path.file_path
            
            if file_object is not None:
                self.out_path.set_file_name(file_object)
            path_object = self.out_path.file_path
        
            if path_file.is_file(): 
                self.aws.to_aws(str(path_file), str(path_object))
                self.logger.info(f'File {path_file} uploaded {path_object}')
            else:
                self.logger.info(f'File {path_file} not found')
        else:
            self.logger.info('Aws disabled')
                               
    def from_aws(self, file_object=None, file_name=None):
        """
            Uploades a file to s3. 
            
            Parameters
            ----------
            file_object: str
                The object name of the file in the aws instance
            file_name: str
                The name of the file 
        """

        if self.is_aws:
            if file_name is not None:
                self.local_path.set_file_name(file_name)
                self.out_path.set_file_name(file_name)
            path_file = self.local_path.file_path
            
            if file_object is not None:
                self.out_path.set_file_name(file_object)
            path_object = self.out_path.file_path
            
            self.aws.to_aws(str(path_object), str(path_file))
            if path_file.is_file():
                self.logger.info(f'File {path_object} downloaded {path_file}')
            else:
                self.logger.info(f'File {path_object} downloaded was not successful ')
        else:
            self.logger.info('S3 disabled')
            
    @classmethod
    def download_wrapper(cls, func):
        
        @wraps(func)
        def local_wrapper(self, *args, **kwargs):
            
            file_name = kwargs.get('file_name')
            file_object = kwargs.get('file_object')
            self.logger.info(f'Wrapper file {file_name} obj {file_object}')
            if self.is_s3:
                self.from_s3(file_object=file_object, file_name=file_name)
            elif self.is_aws:
                self.from_aws(file_object=file_object, file_name=file_name)
            obj = func(self, *args, **kwargs)
            
        return local_wrapper
            
    @classmethod
    def upload_wrapper(cls, func):
        
        @wraps(func)
        def local_wrapper(self, *args, **kwargs):
            
            func(self, *args, **kwargs)
            
            file_name = kwargs.get('file_name')
            file_object = kwargs.get('file_object')
            self.logger.info(f'Wrapper file {file_name} obj {file_object}')
            if self.is_s3:
                self.to_s3(file_object=file_object, file_name=file_name)
            elif self.is_aws:
                self.to_aws(file_object=file_object, file_name=file_name)
            
        return local_wrapper
    
    # @classmethod.download_wrapper
    def read_file(cls, file_name=None, **kwargs):
        
        return cls.read_file(file_name=file_name)

