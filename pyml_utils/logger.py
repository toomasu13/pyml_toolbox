import sys

import logging
import importlib


def init_logger(name, level=logging.INFO, handler='stream', file=None, c_format=None):
    """ Initializes logger inside a jupyter notebook. Return a logger with the specified name.
        
        For example, initiate a logger inside a class:
        self.logger = init_logger(self.__class__.__name__, level=log_level)
        
        Parameters
        ----------
        name: str
            The logger name
        level: int
            The numeric value of logging level. Default: DEBUG
            Logging level 
            CRITICAL 50
            ERROR 40
            WARNING 30
            INFO 20
            DEBUG 10
            NOTSET 0
        handler: str
            which handler to use 'stream', 'file' or 'both'. Default: 'stream'
        file: str
            the path to the log file. Default: 'event.log'
        c_format: str
            the log format string. Default: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    """
    importlib.reload(logging)
    if c_format is None:
        c_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if handler == 'stream' and file is not None:
        handler = 'both'
    logging.basicConfig(format=c_format, level=logging.ERROR, datefmt='%Y-%m-%d %H:%M') #, stream=sys.stdout
    formatter = logging.Formatter(c_format)
    
    logger = logging.getLogger(name)
    if handler == 'stream' or handler == 'both':
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    
    if handler == 'file' or handler == 'both':
        if file is None:
            file = 'event.log'
        fh = logging.FileHandler(file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    logger.setLevel(level)
    logger.propagate = False
    
    return logger
