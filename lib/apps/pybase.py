"""
 pybase is the base class for all CORP applications.
 This program :
    1)ventas - use data , clean data, insert data, generate reports
    2)
"""

__version__ = '20190825'

import sys
import os

from datetime import datetime
from common import app_base, app_log, app_conf, app_env

RET_WARN     = 101
current_date = datetime.now().strftime('%Y-%m-%d')

class _PyBaseApp(object):
    # exitOnError = False
    def __init__(self):
        self.appName = self.__class__.__name__.lower()

        # Class section.
        self._appbase   = app_base._AppBase()
        self._applogger = app_log._AppLogger()
        self._appenv    = app_env._AppENV()
        self._appconf   = app_conf._AppConf()
        # Class section.

        # Shell
        # Path section.
        self.base_dir   = self._appbase._set_base_path()
        self.data_dir   = os.path.join(self.base_dir, 'data'          )
        self.config_dir = os.path.join(self.base_dir, 'config'        )
        self.script_dir = os.path.join(self.base_dir, 'scripts'       )
        #self.log_dir    = os.path.join(self.base_dir, 'log'           )
        self.log_dir    = os.path.join(os.path.join(self.base_dir, 'log'), current_date)
        self.lib_dir    = os.path.join(self.base_dir, 'lib'           )
        self.output_dir = os.path.join(self.data_dir, 'output'        )
        self.input_dir  = os.path.join(self.data_dir, 'input'         )
        self.stmnt_dir  = os.path.join(self.lib_dir , 'statements'    )
        self.source_dir = os.path.join(self.lib_dir , 'sources'       )
        #self.hs_log_dir = os.path.join(self.base_dir, 'log_historial' )

        self.stmnt_fn = os.path.join(self.stmnt_dir , f'{self.appName}.py' )
        self.cfg_file = os.path.join(self.config_dir, f'{self.appName}.cfg')

        self.log_name = f'{self.appName}.log'
        self.set_log_folder()##
        self.log      = self._applogger.get_logger(self.log_dir, self.log_name)

        # Can be overwritten by ENV Vars.
        self.env_vars    = {}
        self.config_vars = {}
        self.config      = {}
        self.cmdStep     = {}
        self.runSeq      = None # set default
        self.runSeq2     = None # set default

    # Abstract define in child class.
    # Use to set configuration variables, that might need spme verification.
    # e.g. int, float, emails, etc
    def set_log_folder(self):  
        if os.path.isdir(self.log_dir) is False: os.makedirs(self.log_dir)
        return 0

    def set_statement_file(self):
        if os.path.exists(self.stmnt_fn):
            self.log.info(f" statements file exist, name:{self.stmnt_fn}")
        else:
            self.log.warning(f" statements file no exist, name:{self.stmnt_fn}")

    def set_config_vars(self): return 0

    # Abstract define in child class.
    def set_global_exe(self): return 0

    # Show all configuration variables in log file.
    def print_config_vars(self):
        for k, v in self.config_vars.items():
            self.log.debug(f'self.config_vars = {k} --  {v}')

    # Set Incoming arguments
    def _set_args(self, argv):

        if len(argv) == 2:
            self.log.critical(f" running <{argv[1]}> fx [runSeq] - Number of arguments ({len(argv)})")

        elif len(argv) == 3: #new order
            self.log.critical(f" running <{argv[1]}>, {argv[2]}> fx [runSeq] [runSeq2] - Number of arguments ({len(argv)})")
            self.runSeq2 = argv[2]

        self.runSeq = argv[1]

        return 0

    # # Execute Steps
    def _execSteps(self, run_step):
        self.log.info(f'runStep = {run_step}')
        for s in run_step:
            if not s in self.cmdStep:
                self.log.error(f'Invalid step {s}')
                return 1

            rv = 1
            try:
                rv = self.cmdStep[s]()
                if rv != 0 and self.exitOnError:
                    self.log.error(f'{s}:{self.cmdStep[s].__name__}()\trc\t={rv}')
                    return rv

                self.log.info(f'{s}:{self.cmdStep[s].__name__}()\trc\t= {rv}')

            except AttributeError:
                self.log.error(f'{s}:{self.cmdStep[s].__name__}')
                self.log.error(f'Except {sys.exc_info()}')
                if (self.exitOnError): return rv

            except SyntaxError:
                self.log.error(f'{s}:{self.cmdStep[s].__name__}()\trc\t={rv}')
                self.log.error(f'Except {sys.exc_info()}')
                if (self.exitOnError): return rv

        return rv

    # # Execute Steps Troubleshoooting

    # argv is a list of runnable commands, defined per class basic
    def main(self, argv):
        rc = 1  # Failed

        # should NEVER get this programmatic error !!!!
        if self.cmdStep is None or len(self.cmdStep) == 0:
            self.log.critical(f'Program Error:self.cmdStep is {self.cmdStep}')
            return 1

        rc = self._set_args(argv)
        if rc != 0:
            return rc

        rc = self._appenv.get_env_vars(self.env_vars, self.log)
        if rc != 0:
            self.log.error('Need to set all env vars')
            return rc

        self.config_vars = self._appconf.load_app_config(self.cfg_file, self.config, self.log)
        if self.config_vars is None:
            self.log.error("Error Loading Config File:\n")
            return rc

        self.print_config_vars()

        rc = self.set_config_vars()
        if rc != 0:
            self.log.error("Error Setting Config Vars\n")
            return rc

        rc = self.set_statement_file()##
        

        if self.runSeq is not None and len(self.runSeq) > 0:
            rc = self._execSteps(self.runSeq)
            if rc == 0:
                self.log.info(f'Completed running exec_steps rc = {rc}')
            else:
                self.log.error(f'execSteps rc = {rc}')

        sys.exit(rc)

    def __del___(self): self.log.debug('Base class cleaning')

if __name__ == '__main__':

    from apps.set_env import setEnvVars

    os.environ['LOG_CONS' ] =  'TRUE'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    a = _PyBaseApp()
    rc = a.main(('a','b'))
