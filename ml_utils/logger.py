import sys

import logging
import importlib


def init_logger(name, level=logging.DEBUG, handler='stream', file=None, file_level=None, c_format=None):
    """ 
        Initializes logger. Return a logger with the specified name.
        
        Parameters
        ----------
        name: str
            The logger name
        level: int
            The numeric value of logging level. Default DEBUG
            Logging level 
            CRITICAL 50
            ERROR 40
            WARNING 30
            INFO 20
            DEBUG 10
            NOTSET 0
        handler: str
            which handler to use 'stream', 'file' or 'both'. Default 'stream'
        file: str
            the log file name
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
        sh.setLevel(level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    
    if handler == 'file' or handler == 'both':
        if file_level is None:
            file_level = level
        if file is None:
            file = 'log.log'
        fh = logging.FileHandler(file)
        sh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    #logger.setLevel(level)
    logger.propagate = False
    
    return logger