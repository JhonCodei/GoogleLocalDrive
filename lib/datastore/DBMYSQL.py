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
# MYSQL Driver
# ===============================================================================
import pymysql as mysql

class DBMYSQL(object):

    def __init__(self, dbcs, logger, encode=str):
        self.conn_str = dbcs
        self.db_conn  = None
        self.log      = logger
        self.encode   = encode
        self.sep      = ','

    # Returns 0 if successful
    def conn_to_db(self):

        rt = 1

        try:
            self.log.info(f"conn_str : {self.conn_str}")
            #self.db_conn = mysql.connect(**self.conn_str)
            self.db_conn = mysql.connect(
                user=self.conn_str['user'],
                passwd=self.conn_str['passwd'],
                db=self.conn_str['db'],
                host=self.conn_str['host'],
                port=self.conn_str['port'],
                charset=self.conn_str['charset']
            )

            self.log.debug(f'Connecting to {self.conn_str}')
            rt = 0
        except Exception as e:
            self.log.error(f'Except Connect String {e}')
            self.log.error(f'Except {sys.exc_info()}')

        finally:
            self.log.debug(f"CONN DB -> {self.db_conn}")
            return rt

    # Use this query for select options
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def run_qry(self, qry_str, s=[]):

        if (type(s) != list):
            s = [s, ]

        self.log.critical(f"execute sql => {qry_str}")

        res_lst = None

        if self.db_conn is None:
            self.log.error(f'self.dbConn has not been set')
            return res_lst

        try:
            tmp    = []
            cursor = self.db_conn.cursor()
            self.log.critical(f"run query => {qry_str}")
            cursor.execute(qry_str, s)
            res    = cursor.fetchall()

            for row in res:
                tmp.append(row)

        except mysql.ProgrammingError:
            self.log.error(f'Except {sys.exc_info()}')

        except Exception as e:
            self.log.error(f'Except {e}')
        else:
            res_lst = tmp

        finally:
            return res_lst


    # Use this method for DML insert, update, delete
    # qryStr: SQL command to execute
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def exe_qry(self, qry_str, s=[]):

        rc = -1
        self.log.critical(f"execute sql => {qry_str}")

        if (type(s) != list or type(s) != tuple): s = list(s)

        if (self.db_conn == None):
            self.log.error(f'self.dbConn has not been set')
            return 1

        try:
            cursor = self.db_conn.cursor()
            cursor.executemany(qry_str, s)

            rc = cursor.rowcount
            self.db_conn.commit()

            self.log.info(f'rc is {rc}')
            return rc

        # IntegrityError columns are not unique
        # ProgrammingError: Incorrect number of bindings supplied
        except mysql.ProgrammingError:
            self.log.error(f'Except ProgrammingError  {sys.exc_info()}')
        except:
            self.log.error(f'Except OperationalError  {sys.exc_info()}')
        finally:
            self.db_conn.rollback()  # WIll get in here only xd
            return rc

    # Use this method for DML insert, update, delete
    # qryStr: SQL command to execute
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def exe_qry_str(self, qry_str):

        rc = -1
        self.log.critical(f"execute sql => {qry_str}")

        if (self.db_conn == None):
            self.log.error(f'self.dbConn has not been set')
            return 1

        try:
            cursor = self.db_conn.cursor()
            cursor.executemany(qry_str)

            rc = cursor.rowcount
            self.db_conn.commit()

            self.log.info(f'rc is {rc} == exe_qry_str')
            return rc

        # IntegrityError columns are not unique
        # ProgrammingError: Incorrect number of bindings supplied
        except mysql.ProgrammingError:
            self.log.error(f'Except ProgrammingError  {sys.exc_info()}')
        except:
            self.log.error(f'Except OperationalError  {sys.exc_info()}')
        finally:
            self.db_conn.rollback()  # WIll get in here only xd
            return rc

    def del_qry(self, qry_str, s=[]):

        rc = -1

        self.log.critical(f'run Query => {qry_str}')

        if (type(s) != list or type(s) != tuple):
            s = list(s)

        if (self.db_conn == None):
            self.log.error(f'self.dbConn has not been set')
            return 1

        try:
            cursor = self.db_conn.cursor()
            cursor.execute(qry_str, s)

            rc = cursor.rowcount
            self.db_conn.commit()

            self.log.info(f'rc is {rc}')
            return rc

        # IntegrityError columns are not unique
        # ProgrammingError: Incorrect number of bindings supplied
        except mysql.ProgrammingError:
            self.log.error(f'Except ProgrammingError  {sys.exc_info()}')
        except:
            self.log.error(f'Except OperationalError  {sys.exc_info()}')
        finally:
            self.db_conn.rollback()  # WIll get in here only xd
            return rc

    def close_db_conn(self):
        if (self.db_conn != None):
            self.db_conn.commit()
            self.log.debug(f' closing connection db, detail => {self.conn_str}')
            self.db_conn.close()
