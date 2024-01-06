"""

@author: eocampo


Modification History
date-author-description

"""

__version__ = '20181113'

import os
import sys
import configparser

class _AppConf(object):
    """docstring for _AppConf."""

    def __init__(self):
        super(_AppConf, self).__init__()

    # --------------------------------------------------------------------------------
    # Function : _chk_config_var(cfg_def, conf_var)
    # Check that all the application required keys are in the config file.
    # cfg_def : read from config file.
    # conf_var: passed from the application, CONFIG_VAR

    def _chk_config_var(self, cfg_def, conf_var):
        cfg_file = set(cfg_def)
        cfg_app  = set(conf_var)
        var_dif  = cfg_app.difference(cfg_file)
        return var_dif

    # --------------------------------------------------------------------------------
    # Function : load_app_config(fn,conf_var,logger)
    # Reads an app config file.
    # Use always DEFAULT section in the config file.
    # fn       : default config file name use in case the env var 'CFG_NAME' is NOT set
    # conf_var : dict passed from the application, CONFIG_VAR.
    # logger   : handler to application logger.
    # Returns  : <class 'configparser.SectionProxy'>==<Section: DEFAULT>

    def load_app_config(self, fn, cfg_var, logger):

        cfg_default = None

        if len(cfg_var) == 0:
            logger.info('Application does not require config a file')
            return []

        if 'CFG_NAME' in os.environ.keys(): fn = os.environ['CFG_NAME']

        logger.info(f'Loading config file : {fn}')

        config = configparser.ConfigParser()
        config.optionxform = str            # Case Sensitive.

        try:
            config.read(fn)
            cfg_default = config['DEFAULT']

            var_dif = self._chk_config_var(cfg_default.keys(), cfg_var.keys())
            logger.debug(f'Config File Variables {list(cfg_default.keys())}')
            logger.debug(f'App Variables {list(cfg_var.keys())}')

            if len(var_dif) > 0:
                logger.error(f'Need to define : {var_dif} en {fn}')
                cfg_default = None

        except:
            logger.error(f'Except {sys.exc_info()}')

        finally:
            return cfg_default
