"""
@author: jalcarraz
This module implements email functionality.

Modification History
date-author-description

pip install pymysql

"""
__version__ = '20190823'

# ===============================================================================
# DEFAULT import
# ===============================================================================
import sys
# ===============================================================================
# DEFAULT import
# ===============================================================================

# ===============================================================================
# SQLLITE Driver
# ===============================================================================
import sqlite3

class DBSQLLite(object):

    def __init__(self, cs, logger, encode=str):

        self.conn_str = cs
        self.db_conn  = None
        self.log      = logger
        self.encode   = encode
        self.sep      = ','

    # Returns 0 if successful
    def conn_to_db(self):

        ret = 1
        try:
            # self.dbConn = sqlite3.connect(self.connStr,isolation_level=None)
            self.db_conn = sqlite3.connect(self.conn_str)
            self.db_conn.text_factory = self.encode
            self.log.debug(f'Connecting to {self.conn_str}')
            ret = 0

        except:
            self.log.error(f'Except Connect String {self.conn_str}')
            self.log.error(f'Except {sys.exc_info()}')

        finally:
            return ret

    # Use this query for select options
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def run_qry(self, qry_str, s=[]):

        if (type(s) != list):
            s = [s, ]

        res_lst = None
        if self.db_conn is None:
            self.log.error(f'self.dbConn has not been set')
            return res_lst

        try:
            tmp    = []
            cursor = self.db_conn.cursor()
            res    = cursor.execute(qry_str, s)
            for row in res:
                tmp.append(row)

        except sqlite3.OperationalError:
            self.log.error(f'Except {sys.exc_info()}')

        else:
            res_lst = tmp
        finally:
            return res_lst

    # Use this method for DML insert, update, delete
    # qryStr: SQL command to execute
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def exe_qry(self, qry_str, s=[]):

        rc = -1

        if (type(s) != list or type(s) != tuple):
            s = list(s)

        if (self.db_conn == None):
            self.log.error(f'self.dbConn has not been set')
            return 1

        try:
            cursor = self.db_conn.cursor()
            # cursor.execute(qry_str, s)
            cursor.executemany(qry_str, s)
            rc = cursor.rowcount
            self.db_conn.commit()
            self.log.info(f'rc is {rc}')
            return rc

        # IntegrityError columns are not unique
        # ProgrammingError: Incorrect number of bindings supplied
        except sqlite3.OperationalError:
            # self.dbConn.rollback()
            # raise sqlite3.OperationalError
            self.log.error(f'Except OperationalError  {sys.exc_info()}')

        except sqlite3.IntegrityError:
            # self.dbConn.rollback()              # EO might help in DB lock issue.
            # raise sqlite3.IntegrityError, msg
            self.log.error(f'Except IntegrityError {sys.exc_info()}')

        except:
            self.log.error(f'Except OperationalError  {sys.exc_info()}')
        finally:
            self.db_conn.rollback()  # WIll get in here only
            return rc


    def close_db_conn(self):
        if (self.db_conn != None):
            self.db_conn.commit()
            self.log.debug(f'Closing Conn {self.conn_str}')
            self.db_conn.close()


