"""
@author: eocampo

Modification History
date-author-description

"""
__version__ = '20181113'

import os
import sys

class _AppENV(object):
    """docstring for _AppENV."""

    def __init__(self):
        super(_AppENV, self).__init__()

        self.varsENV = None
        self.log     = None

    def get_env_vars(self, e_vars, logger):
        ret = 0
        err = []

        self.varsENV = e_vars
        self.log     = logger

        if len(self.varsENV) == 0:

            self.log.info('No env vars to load')
            return 0

        for ev, v in self.varsENV.items():
            self.log.debug(f'{v} = os.environ[{ev}]')

        for ev, v in self.varsENV.items():

            try:
                print(f'---------- ev = {ev} v = {v}')
                x = os.environ[ev]
                exec(f"v='x'")
                self.log.debug(f"{v}='{x}'")

            except:
                ret = 2
                err.append(ev)
                self.log.debug(f'Except {sys.exc_info()}')

        if len(err) > 0:
            self.log.error(f'Need to define envars {err}')

        return ret
