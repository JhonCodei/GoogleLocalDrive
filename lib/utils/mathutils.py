
"""

@author: eocampo
This module manages OS operations.  All OS specfic should br handled here.

Modification History
date-author-description

"""

__version__ = '20181113'

# This function calculates a perc based on 100% , in which x100 repersents 100%
# By contract all parameters are numeric
def get_perc_100(x100,yper):

    if x100 == 0 or yper == 0:
        return -1
    if x100 < yper:
        return -2

    return round(100 * yper/x100, 0)