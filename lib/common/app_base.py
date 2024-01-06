"""
@author: jalcarraz

Modification History
date-author-description
Use for standalone application.

# """
__version__ = '20190825'


import os
import sys
import inspect
import threading
import platform

class _AppBase(object):

    def __init__(self):
        
        self.base_dir   = None
        self.data_dir   = None
        self.config_dir = None
        self.script_dir = None
        self.log_dir    = None
        self.lib_dir    = None
        self.output_dir = None
        self.input_dir  = None
        self.stmnt_dir  = None
        self.source_dir = None

        #self._set_dir_project()

    def _set_base_path(self):

        main_id = None
        ret     = 0

        for t in threading.enumerate():
            if t.name == 'MainThread':
                main_id = t.ident
                break
        if not main_id:
            raise RuntimeError("Main thread exited before execution")

        current_main_frame = sys._current_frames()[main_id]
        base_frame = inspect.getouterframes(current_main_frame)[-1]

        if platform.system() == 'Windows':
            filename = base_frame.filename
        else:
            filename = base_frame[0].f_code.co_filename

        ret = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(filename))))

        return ret

    def _set_dir_project(self):


        self.base_dir = self._set_base_path()

        # try:
        #     if len(self.base_dir) == 0 : return sys.exc_info()
        # except Exception as e:
        #     print(f"exc base app {e}")
        #     raise RuntimeError(f"error except {e}")

        self.data_dir   = os.path.join(self.base_dir, 'data'       )
        self.config_dir = os.path.join(self.base_dir, 'config'     )
        self.script_dir = os.path.join(self.base_dir, 'script'     )
        self.log_dir    = os.path.join(self.base_dir, 'log'        )
        self.lib_dir    = os.path.join(self.base_dir, 'lib'        )
        self.output_dir = os.path.join(self.data_dir, 'output'     )
        self.input_dir  = os.path.join(self.data_dir, 'input'      )
        self.stmnt_dir  = os.path.join(self.lib_dir , 'statements' )
        self.source_dir = os.path.join(self.lib_dir , 'sources'    )

        #print(self.data_dir)
