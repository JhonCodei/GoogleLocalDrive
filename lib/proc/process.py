"""

@author: eocampo
This module manages OS operations.  All OS specfic should br handled here.

Modification History
date-author-description

"""
__version__ = '20181113'

import sys
import subprocess

SUCCESS = 0
ERROR   = -1
EXCEP   = -3

# Executes synchronous processes, so THE invoking method will wait for a response.

def run_sync(cmd, logger):
    rc = (ERROR, 'Error')

    try:
        logger.debug(f"cmd {cmd}")
        # -------------- Platform Specific Cmd :Start
        if (sys.platform == 'win32'):
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        # -------------- Platform Specific Cmd :End

        r_msg  = p.communicate()[0]
        r_code = p.wait()

        rc = (r_code, r_msg)

        logger.debug(f"rv={r_code} p.rc={p.returncode}\np.msg ======= {r_msg} ======== ")
        if r_code != SUCCESS:
            logger.error(f"rv={r_code} rc={p.returncode}\nmsg ========= {r_msg} ========= ")

    except:
        logger.error(f'Error {sys.exc_info()}')
        rc = (EXCEP, r_msg)

    finally:
        return rc
