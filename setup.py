from setuptools import setup, find_packages


setup(
    name='pyml_toolbox',
    version='0.1',
    description='A machine learning toolbox and utilities',
    url='https://github.com/toomasu13/pyml_toolbox.git',
    author='Toomas Kirt',
    author_email='Toomas.Kirt@gmail.com',
    license='GNU GPLv3',
    packages=find_packages(include=['pyml_utils', 'pyml_toolbox']),
    install_requires=[
        'pandas',
        'pyarrow',  
        'sqlalchemy',
        'snowflake-connector-python',
        'snowflake-sqlalchemy',
        'joblib',
        ],
    zip_safe=False,
    )
