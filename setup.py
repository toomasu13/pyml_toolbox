from setuptools import setup, find_packages


setup(
    name='pyml_toolbox',
    version='0.1.0',
    description='A machine learning toolbox and utility functions',
    url='https://github.com/toomasu13/pyml_toolbox',
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
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',       
        'Programming Language :: Python :: 3.10',
    ],
    )
