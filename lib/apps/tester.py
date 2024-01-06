"""
Description
"""
__version__ = '20210618'

import sys
import os
import time


from datetime import datetime

import proc.process      as p
import utils.fileutils   as fu
import utils.netutils    as nu
import utils.strutils    as su

#from utils.emailutils    import EmailUtils
#from transport           import sshutil

from apps.pybase        import _PyBaseApp
#from statements.tester  import _SQLTester

current_date     = datetime.now().strftime('%Y%m%d')
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
dl               = "b-k-db"

class Tester(_PyBaseApp):

    def __init__(self):

        super(Tester, self).__init__()
        self.exitOnError = False

        # Environmental variables:
        self.env_vars = {}

        # Configuration variables:

        self.config = {
                        'dr_base-1'  : '',
                        'dr_ifile-1' : '',
                        'dr_ofile-1' : '',
                    }

        self.callqry = None
        self.em_cfg  = {}
        # Allowable commands for this application
        self.cmdStep = {
                        'A': self.test,
                        }
    # Use only for configuration values that need some manipulations/checks.
    def set_config_vars(self):

        if len(self.runSeq2) == 0: self.runSeq2 = 1

        self.dr_base  = self.config_vars[f'dr_base-{self.runSeq2}']
        self.dr_ifile = os.path.join(self.dr_base, self.config_vars[f'dr_ifile-{self.runSeq2}'])
        self.dr_ofile = os.path.join(self.dr_base, self.config_vars[f'dr_ofile-{self.runSeq2}'])

        return 0

    """'''''''''''''''''''''''''"""
    """ 1) -> TESTER """
    """'''''''''''''''''''''''''"""
    def test(self):

        ret = 1
        print(self.log_dir)
        return ret

def main(Args):

    a = Tester()
    rc = a.main(Args)
    return rc

if __name__ == '__main__':

    rc = main(sys.argv)
    sys.exit(rc)
