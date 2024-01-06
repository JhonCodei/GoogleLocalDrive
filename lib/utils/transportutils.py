from transport import sshutil
from LocalDrive.lib.datastore import DBSQLLite
from LocalDrive.lib.datastore import DBMYSQL

class DBTransport(object):
    """docstring for DBTransport."""

    def __init__(self, conn_ssh, conn_db, logger):# qry, ls
        super(DBTransport, self).__init__()
        self.conn_ssh_str = conn_ssh
        self.conn_db_str  = conn_db
        self.log          = logger

    def ssh_get_data(self, qry, ls=[]):

        rc = 0

        tunnel = sshutil.SSHTunnel(self.conn_ssh_str, self.log)
        self.lc_port = tunnel.establish_ssh_tunnel()

        self.conn_db_str.update([ ('port', self.lc_port) ])# add to db_str
        self.log.debug(f"cnn db => {self.conn_db_str}")

        db = DBMYSQL.DBMYSQL(self.conn_db_str, self.log, encode=str)

        rc = db.conn_to_db()
        if rc != 0:
            self.log.error(f"conn db ->{rc}")
            return rc

        res = db.run_qry(qry, ls)

        db.close_db_conn()
        tunnel.stop_ssh()

        return res

    def ssh_exec_qry(self, qry):

        rc = 0

        tunnel = sshutil.SSHTunnel(self.conn_ssh_str, self.log)
        self.lc_port = tunnel.establish_ssh_tunnel()

        self.conn_db_str.update([ ('port', self.lc_port) ])# add to db_str
        self.log.debug(f"cnn db => {self.conn_db_str}")

        db = DBMYSQL.DBMYSQL(self.conn_db_str, self.log, encode=str)

        rc = db.conn_to_db()
        if rc != 0:
            self.log.error(f"conn db ->{rc}")
            return rc

        res = db.run_qry(qry, [])

        db.close_db_conn()
        tunnel.stop_ssh()

        return res


    def ssh_insert_data(self, qry, ls=[]):

        rc = 0

        tunnel = sshutil.SSHTunnel(self.conn_ssh_str, self.log)
        self.lc_port = tunnel.establish_ssh_tunnel()

        self.conn_db_str.update([ ('port', self.lc_port) ])# add to db_str

        self.log.debug(f"cnn db => {self.conn_db_str}")

        db = DBMYSQL.DBMYSQL(self.conn_db_str, self.log, encode=str)

        rc = db.conn_to_db()
        if rc != 0:
            self.log.error(f"conn db ->{rc}")
            return rc

        rc = db.exe_qry(qry, ls)

        self.log.info(f" RC = {rc}")

        db.close_db_conn()
        tunnel.stop_ssh()

        return rc

    def ssh_delete_data(self, qry, ls=[]):

        rc = 0

        tunnel = sshutil.SSHTunnel(self.conn_ssh_str, self.log)
        self.lc_port = tunnel.establish_ssh_tunnel()

        self.conn_db_str.update([ ('port', self.lc_port) ])# add to db_str

        self.log.debug(f"cnn db => {self.conn_db_str}")

        db = DBMYSQL.DBMYSQL(self.conn_db_str, self.log, encode=str)

        rc = db.conn_to_db()
        if rc != 0:
            self.log.error(f"conn db ->{rc}")
            return rc

        rc = db.del_qry(qry, ls)

        self.log.info(f" RC = {rc}")

        db.close_db_conn()
        tunnel.stop_ssh()

        return rc
