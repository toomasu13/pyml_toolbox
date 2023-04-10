from setuptools import setup, find_packages


setup(name='pyml_toolbox',
      version='0.1',
      description='A machine learning toolbox and utilities',
      url='https://github.com/toomasu13/pyml_toolbox.git',
      author='Toomas Kirt',
      author_email='Toomas.Kirt@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),
      install_requires=[
        'pandas>=1.4.1',
        'sqlalchemy',
        'numpy>=1.21.1',
        'matplotlib>=3.1.1',
        'joblib',
        'jupyter'],
      zip_safe=False)