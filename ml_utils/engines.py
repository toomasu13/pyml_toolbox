#from pathlib import Path
import base64 as b64
import re
#import json
from sqlalchemy import create_engine
import pandas as pd

from .conf import ConfHandler
from .logger import init_logger

class Engine():
    """
    A class to handle stored logins and database engine configs
    
    Usage:
    L = Engine(dir_engine='location of json file')
    
    user, password = L.get_login('sf')
    
    engine_core = get_engine('core')
    
    query = '''
        SELECT
            *
        FROM client 
        limit 10
        '''
    df = E.from_sql(query, 'core')

    """
    
    def __init__(self, is_encode=True, dir_engine=None):
        """
        Parameters
        ----------
        is_encode: bool
            Whether logins will be encoded
        dir_engine: str - optional
            Directory for the json config file. Default '.ml_toolbox'
        """
        
        log_level = ConfHandler(dir_conf='.ml_toolbox', file_conf='ml_toolbox').get_key('log_level', 20)
        self.logger = init_logger('Engine', level=log_level)
        if not dir_engine:
            dir_engine = '.ml_toolbox'
        self.conf = ConfHandler(dir_conf=dir_engine, file_conf='engine', log_level=log_level) 
        self.is_encode = is_encode
        
        if not self.conf.get_conf():
            self.conf.set_conf({'login': {}, 'engine': {}, 'url': {}})
            
        self.default_url = '{driver}://{user}:{password}@{host}/{database}'
        self.sessions = {}
        
    def set_login(self, login, user, password):
        """
        Add a new login
        """
        if self.is_encode:
            user = b64.b64encode(user.encode("utf-8")).decode("utf-8")
            password = b64.b64encode(password.encode("utf-8")).decode("utf-8")
            
        self.conf.set_key('login', {login: {'user': user, 'password': password, 'is_encode': self.is_encode}})
        
    def list_logins(self):
        """
        Returns list of available logins
        
        """
        
        return [ic for ic in self.conf.get_key('login').keys()]
    
    def get_login_json(self, login):
        """
        Returns login - user name and password for a source as a json
        
        Parameters
        ----------
        login: str
            The name of login
        """
        user = None
        password = None
        dict_login = {}
        if self.conf.get_key('login').get(login) is not None:
            user = self.conf.get_key('login').get(login).get('user')
            password = self.conf.get_key('login').get(login).get('password')
            is_encode = self.conf.get_key('login').get(login).get('is_encode', False)

            if is_encode:
                try:
                    user = b64.b64decode(user.encode("utf-8")).decode("utf-8")
                    password = b64.b64decode(password.encode("utf-8")).decode("utf-8")
                except:
                    self.logger.info(f'Decode failed')
            dict_login = {'user': user, 'password': password}
        else:
            self.logger.info(f'Driver {login} logins not found')
            
        return dict_login
        
    def get_login(self, login):
        """
        Returns login - user name and password for a source
        
        Parameters
        ----------
        login: str
            The name of login
        """
        dict_login = self.get_login_json(login)
        user = None
        password = None
        if dict_login:
            user = dict_login.get('user')
            password = dict_login.get('password')
            
        return user, password
    
    def set_url(self, driver, url=None):
        """
            Set url string for a database driver
        """
        if url is None: 
            url = self.default_url
        self.conf.set_key('url', {driver: url})   
    
    def get_url(self, driver):
        """
            Get url string for a database driver. If not present, returns default string
            https://docs.sqlalchemy.org/en/14/core/engines.html
            dialect+driver://username:password@host:port/database
        """
        
        url = self.conf.get_key('url').get(driver)
        if url is None: 
            url = self.default_url
            self.logger.info(f'Url missing. Default url for {driver}')
        return url
    
    def list_url(self):
        
        return self.conf.get_key('url')
    
    def set_engine(self, source, **kwargs):
        """
            Add a new login
        """
        
        if not kwargs:
            kwargs = {}
            
        self.conf.set_key('engine', {source: {**kwargs}})
        
    def list_engines(self):
        """
            Returns list of available engine names
        """
        

        return [ic for ic in self.conf.get_key('engine').keys()]
    
    def get_engine_json(self, source):
        """
            Returns fields of the engine as a json
        """
        dict_engine = {}
        if self.conf.get_key('engine').get(source) is not None:
            login = self.conf.get_key('engine').get(source).get('login')
            dict_engine.update(self.conf.get_key('engine').get(source).copy())
            if login:
                dict_engine.update(self.get_login_json(login))
        else:
            self.logger.info(f'Engine {source} not found')
        return dict_engine
        
    def get_engine(self, source):
        """
            Returns database engine

            Parameters
            ----------
            source: str
                database name
        """
        
        if not self.is_active(source):
            dict_engine =  self.get_engine_json(source)
            driver = dict_engine.get('driver')
            if driver:
                url = self.get_url(driver)
                dict_url = {ic: '' for ic in re.findall(r"{(\w+)}", url)}
                dict_url.update(dict_engine)
                self.sessions[source] = create_engine(url.format(**dict_url))
            else:
                self.logger.info(f'Engine {source} driver {driver} not found')
                
        return self.sessions.get(source)

    def is_active(self, source):
        """
            Cheks whether the session is acitve
        """
        is_active = False
        
        if self.sessions.get(source) is not None:
            try:
                if self.sessions.get(source).execute('select 1').fetchone()[0] == 1:
                    is_active = True
            except:
                self.logger.debug(f'Session {source} not active')
               
        return is_active
    
    def from_sql(self, query, source):
        """
            Runs a query in a database engine

            Parameters
            ----------
            query: str
                database query, e.g. 'select 1'
            source: str
                name of the database, e.g.'core'
        """        
        return pd.read_sql_query(query, self.get_engine(source))
    
    def to_sql(self, df, table_name, source, if_exists='replace', index=False, chunksize=16000, method='multi'):
        """
        Write records stored in a DataFrame to a SQL database.
        
        Parameters
        ----------
        df: DataFrame
            Pandas Dataframe
        table_name: str
            Name of SQL table.
        source: str
            name of the database, e.g.'snowflake'
        if_exists: {‘fail’, ‘replace’, ‘append’}, default 'replace'
            How to behave if the table already exists. 
        chunksize : int, default 16000
            Rows will be written in batches of this size at a time.
        method : {None, ‘multi’, callable}, default 'multi'
            Controls the SQL insertion clause used
        index: bool, default False
            Write DataFrame index as a column. Snowflake does not support index writing. 
        """
        chunksize = 16000
        
        try:
            if df.shape[0] > chunksize:
                df.to_sql(table_name, con=self.get_engine(source), if_exists=if_exists, chunksize=chunksize, method=method, index=index)
            else:
                df.to_sql(table_name, con=self.get_engine(source), if_exists=if_exists, method=method, index=index)
        except:
            self.logger.info(f"Error when creating table {table_name}")