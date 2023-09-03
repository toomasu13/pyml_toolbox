
# Engine Class

The `Engine` class is designed to manage stored logins and database engine configurations. It provides functionalities to store and retrieve login credentials, define database engine parameters, execute SQL queries, and read/write data frames to/from different database sources.

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Setting Login Credentials](#setting-login-credentials)
  - [Defining Database Drivers](#defining-database-drivers)
  - [Configuring Engine Parameters](#configuring-engine-parameters)
  - [Executing Queries and Data Operations](#executing-queries-and-data-operations)
  - [SQLite Examples](#examples)

## Introduction

The `Engine` class enables seamless interaction with databases by storing and managing login credentials, engine configurations, and executing SQL queries. It simplifies the process of connecting to databases, executing queries, and handling data operations. By storing the credentials using the Engine class, there is no need to expose them within Jupyter notebooks, thereby mitigating the risk of credentials being unintentionally exposed in a public Git repository or any other public location.

## Usage

### Initialization

Initialize an `Engine` object with optional parameters:

```python
E = Engine(dir_engine='/file/path', is_encode=True, log_level=20)
```

- `dir_engine` (optional): The directory of the JSON config file. Default is '.ml_toolbox' in the user's home directory.
- `is_encode` (optional): Whether logins will be encoded. Default is `True`.
- `log_level` (optional): The level of logging. Default is 20 (INFO).

### Setting Login Credentials

Add a new login credential for a database source:

```python
E.set_login(login='snowflake', user='name', password='pw')
```

### Defining Database Drivers

Set the URL template for a database driver:

```python
E.set_driver('snowflake', url='{driver}://{user}:{password}@{host}/{database}/{schema}?role={role}&warehouse={warehouse}')
```

### Configuring Engine Parameters

Add a new engine parameter for a database source:

```python
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
```

### Executing Queries and Data Operations

Execute a query in a database engine and retrieve the result as a DataFrame:

```python
query = '''
    SELECT
        *
    FROM client 
    LIMIT 10
'''
df = E.from_sql(query, 'snowflake')
```

Write records stored in a DataFrame to a SQL database table:

```python
df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3', 'User 4']})
E.to_sql(df, 'users', 'sqlite_mem')
```

### SQLite Examples 

```python
# Initialize Engine
E = Engine(dir_engine='/file/path')


# Set SQLite in-memory engine configuration
E.set_driver('sqlite', url='{driver}://{database}')
dict_sqlite_mem = {
    'driver': 'sqlite',
    'database': ''
}
E.set_engine('sqlite_mem', **dict_sqlite_mem)

# Write DataFrame to SQL table
df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3', 'User 4']})
E.to_sql(df, 'users', 'sqlite_mem')

# Execute SQL query on SQLite in-memory
query = '''
    SELECT * FROM users
'''
dfo = E.from_sql(query, 'sqlite_mem')

# Set SQLite file-based engine configuration
dict_sqlite_file = {
    'driver': 'sqlite',
    'database': '//home/user/data/sqlite/sqlite.db'
}
E.set_engine('sqlite_file', **dict_sqlite_file)
```
