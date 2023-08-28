import base64 as b64
import re

from sqlalchemy import create_engine
import pandas as pd

from .logger import init_logger
from .conf import ConfHandler
from .files import PathHandler


class Engine():
    """ A class to handle stored logins and database engine configs.

        This class allows the user to store and retrieve login credentials and engine parameters for different database sources.
        The user can also use this class to execute SQL queries and read or write data frames from and to the database sources.
        
        Parameters
        ----------
        dir_engine : str or Path, optional
            The directory of the JSON config file. Default is '.ml_toolbox' in the user's home directory.
        is_encode : bool, optional
            Whether logins will be encoded. Default is True.
        log_level : int, optional
            The level of logging. Default is 20 (INFO).
                
        Methods
        -------
        set_login(login, user, password)
            Add a new login credential for a database source.
        list_logins()
            Return a list of available login names.
        get_login_json(login)
            Return a dictionary of user name and password for a login name.
        get_login(login)
            Return a tuple of user name and password for a login name.
        set_driver(driver, url=None)
            Set the URL template for a database driver.
        get_driver(driver)
            Get the URL template for a database driver. If not present, returns the default template.
        list_drivers()
            Return a dictionary of available drivers and their URL templates.
        set_engine(source, [**kwargs)
            Add a new engine parameter for a database source.
        list_engines()
            Return a list of available engine names.
        get_engine_json(source)
            Return a dictionary of engine parameters for a source name.
        get_engine(source)
            Return a database engine object for a source name. If not active, creates a new session.
        is_active(source)
            Return True if the session for a source name is active.
        from_sql(query, source)
            Execute a SQL query on a database source and return a data frame with the results.
        to_sql(df, table_name, source, if_exists='replace', index=False, chunksize=16000, method='multi')
            Write a data frame to a SQL table on a database source.

        Example
        E = Engine(dir_engine='/file/path')
        E.set_login(login='snowflake', user='name', password='pw')

        user, password = E.get_login('snowflake')

        E.set_driver('snowflake', url= '{driver}://{user}:{password}@{host}/{database}/{schema}?role={role}&warehouse={warehouse}')
        dict_snowflake = {'driver': 'snowflake',
                  'login': 'snowflake',
                  'host': 'snowflake.host',
                  'database': 'db',
                  'schema': 'sc',
                  'warehouse': 'wh',
                  'role': 'user_role',
                    } 
        E.set_engine('snowflake', **dict_snowflake)

        query = '''
            SELECT
                *
            FROM client 
            limit 10
            '''
        df = E.from_sql(query, 'snowflake')
        
        # SQLite in memory
        E.set_driver('sqlite', url='{driver}://{database}')
        dict_sqlite_mem = {'driver': 'sqlite',
                          'database': '',
                            } 
        E.set_engine('sqlite_mem', **dict_sqlite_mem)
        
        df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3', 'User 4']})
        E.to_sql(df, 'users', 'sqlite_mem')
        
        query = '''
                SELECT * FROM users
            '''
        dfo = E.from_sql(query, 'sqlite_mem')
        
        dict_sqlite_file = {'driver': 'sqlite',
                            'database': '//home/user/data/sqlite/sqlite.db',
                           } 
        E.set_engine('sqlite_file', **dict_sqlite_file)
    """
    
    def __init__(self, dir_engine=None, is_encode=True, log_level=20):
        """ Initializes an Engine object with the given directory, encoding flag and log level.
        
            Parameters
            ----------
            dir_engine : str or Path, optional
                The directory of the JSON config file. Default is '.ml_toolbox' in the user's home directory.
            is_encode : bool, optional
                Whether logins will be encoded. Default is True.
            log_level : int, optional
                The level of logging. Default is 20 (INFO).
        """
        
        self.logger = init_logger(self.__class__.__name__, level=log_level)
        
        if not dir_engine:
            path_engine = PathHandler(file_dir='@home', file_name='engine', file_suffix='json')
            path_engine.add_path('.ml_toolbox')
        else:
            path_engine = PathHandler(file_dir=dir_engine, file_name='engine', file_suffix='json') 
        if not path_engine.is_path():
            path_engine.create_path()
        self.conf = ConfHandler(file_conf=path_engine.file_path, log_level=log_level) 
        
        self.is_encode = is_encode
        
        if not self.conf.get_conf():
            self.conf.set_conf({'login': {}, 'engine': {}, 'driver': {}})
            
        self._default_url = '{driver}://{user}:{password}@{host}/{database}'
        self.sessions = {}
        
    def set_login(self, login, user, password):
        """ Add a new login credential for a database source.

            Parameters
            ----------
            login : str
                The name of the login credential.
            user : str
                The user name of the login credential.
            password : str
                The password of the login credential.
        """
        if self.is_encode:
            user = b64.b64encode(user.encode("utf-8")).decode("utf-8")
            password = b64.b64encode(password.encode("utf-8")).decode("utf-8")
            
        self.conf.update_key('login', {login: {'user': user, 'password': password, 'is_encode': self.is_encode}})
        
    def list_logins(self):
        """ Return a list of available login names.
        
            Returns
            -------
            dict
                A list of available login names.
        """
        
        return [ic for ic in self.conf.get_key('login').keys()]
    
    def get_login_json(self, login):
        """ Return a dictionary of user name and password for a login name.
        
            Parameters
            ----------
            login : str
                The name of the login credential.
                
            Returns
            -------
            dict
                A dictionary with keys 'user' and 'password' that store the user name and password for the login name. If the login name is not found, returns an empty dictionary.
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
            self.logger.info(f'Logins {login} not found')
            
        return dict_login
        
    def get_login(self, login):
        """ Return a tuple of user name and password for a login name.

            Parameters
            ----------
            login : str
                The name of the login credential.

            Returns
            -------
            tuple
                A tuple of user name and password for the login name. If the login name is not found, returns (None, None).
        """
        dict_login = self.get_login_json(login)
        user = None
        password = None
        if dict_login:
            user = dict_login.get('user')
            password = dict_login.get('password')
            
        return user, password
    
    def set_driver(self, driver, url=None):
        """ Set the URL template for a database driver.

            Parameters
            ----------
            driver : str
                The name of the database driver.
            url : str, optional
                The URL template for the database driver. If not given, uses the default template. Default is None.
        """
        if url is None: 
            url = self._default_url
        self.conf.update_key('driver', {driver: url})   
    
    def get_driver(self, driver):
        """ Get the URL template for a database driver. If not present, returns the default template.

            Parameters
            ----------
            driver : str
                The name of the database driver.

            Returns
            -------
            str
                The URL template for the database driver. The template has placeholders for user name, password, host and database that can be filled with format() method. 
                For example: 'snowflake://{user}:{password}@{host}/{database}'.
        """
        
        url = self.conf.get_key('driver').get(driver)
        if url is None: 
            url = self._default_url
            self.logger.info(f'Driver Url missing. Default url for {driver}')
        return url
    
    def list_drivers(self):
        """ Return a dictionary of available database drivers and their URL templates.

            Returns
            -------
            dict
                A list containing names of available database drivers.
        """
        
        return self.conf.get_key('driver')
    
    def set_engine(self, source, **kwargs):
        """ Add a new engine parameter for a database source.

            Parameters
            ----------
            source : str
                The name of the database source.
            **kwargs : dict, optional
                Additional keyword arguments for configuring the engine parameter. For example: {'login': 'snowflake', 'driver': 'snowflake', 'host': 'myhost', 'database':...
        """
        
        if not kwargs:
            kwargs = {}
            
        self.conf.update_key('engine', {source: {**kwargs}})
        if self.sessions.get(source):
            del self.sessions[source]  # Remove active session
        
    def list_engines(self):
        """ Returns a list of available engine names.
        
            Returns
            -------
            list
                A list containing names of available engine configurations.
        """
        
        return [ic for ic in self.conf.get_key('engine').keys()]
    
    def get_engine_json(self, source):
        """ Retrieve engine configuration details as a dictionary in JSON format.

            Parameters
            ----------
            source : str
                The name of the source database.

            Returns
            -------
            dict
                A dictionary containing engine configuration details, including login and driver information.
        """
        dict_engine = {}
        if self.conf.get_key('engine').get(source) is not None:
            dict_engine.update(self.conf.get_key('engine').get(source).copy())
            login = self.conf.get_key('engine').get(source).get('login')
            if login:
                dict_engine.update(self.get_login_json(login))
            driver = self.conf.get_key('engine').get(source).get('driver')
            if driver:
                dict_engine.update({driver: self.get_driver(driver)})
        else:
            self.logger.info(f'Engine {source} not found')
        return dict_engine
        
    def get_engine(self, source):
        """ Retrieve the database engine for the specified source.

            Parameters
            ----------
            source : str
                The name of the source database.

            Returns
            -------
            sqlalchemy.engine.base.Engine
                The SQLAlchemy engine associated with the specified source.
        """
        
        if not self.is_active(source):
            dict_engine =  self.get_engine_json(source)
            driver = dict_engine.get('driver')
            if driver:
                url = self.get_driver(driver)
                dict_url = {ic: '' for ic in re.findall(r"{(\w+)}", url)}
                dict_url.update(dict_engine)
                self.sessions[source] = create_engine(url.format(**dict_url))
            else:
                self.logger.info(f'Engine {source} driver {driver} not found')
                
        return self.sessions.get(source)

    def is_active(self, source):
        """ Check whether the session for the specified source is active.

            Parameters
            ----------
            source : str
                The name of the source database.

            Returns
            -------
            bool
                True if the session is active, False otherwise.
        """
        is_active = False
        
        if self.sessions.get(source) is not None:
            try:
                test_out = self.sessions.get(source).execute('select 1').fetchone()[0]
                if test_out == 1:
                    is_active = True
            except:
                self.logger.info(f'Session {source} not active')
               
        return is_active
    
    def from_sql(self, query, source):
        """ Execute a query in a database engine and retrieve the result as a DataFrame.

            Parameters
            ----------
            query : str
                The database query, e.g., 'SELECT * FROM my_table'.
            source : str
                The name of the source database, e.g., 'snowflake'.

            Returns
            -------
            pandas.DataFrame
                A DataFrame containing the query result.
        """  
        df = None
        try:
            df = pd.read_sql_query(query, self.get_engine(source))
        except Exception as exc:
            self.logger.error(f"{type(exc).__name__} - message: {exc} - when running the query {query[:30]}...")
        return df
    
    def to_sql(self, df, table_name, source, if_exists='replace', index=False, chunksize=16000, method='multi'):
        """ Write records stored in a DataFrame to a SQL database table.

            Parameters
            ----------
            df : pandas.DataFrame
                The DataFrame containing the records to be written.
            table_name : str
                The name of the SQL table.
            source : str
                The name of the source database, e.g., 'snowflake'.
            if_exists : {'fail', 'replace', 'append'}, default 'replace'
                How to behave if the table already exists.
            chunksize : int, default 16000
                Number of rows to be written in each batch.
            method : {'None', 'multi', callable'}, default 'multi'
                Controls the SQL insertion clause used.
            index : bool, default False
                Whether to write DataFrame index as a column. Note: Snowflake does not support index writing.
        """
        
        try:
            if df.shape[0] > chunksize:
                df.to_sql(table_name, con=self.get_engine(source), if_exists=if_exists, chunksize=chunksize, method=method, index=index)
            else:
                df.to_sql(table_name, con=self.get_engine(source), if_exists=if_exists, method=method, index=index)
        except Exception as exc:
            self.logger.error(f" {type(exc).__name__} - message: {exc} - when creating table {table_name}")
