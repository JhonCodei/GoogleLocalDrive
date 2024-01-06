"""
-- This Utils only use for fingerprint-devices zkteko

@author: Owk'r

"""
__version__ = "20190825"


import os
import sys
from zk import ZK, const

class ZKUtil(object):

    def __init__(self, logger, ip, port=4370):

        self.log     = logger
        self.sep     = ','

        self.zk_sttg = None
        self.zk_ip   = ip
        self.zk_port = port
        self.zk_conn = None
        self.timeout = 5
        self.passwd  = 0
        self.fc_udp  = False
        self.om_png  = False

    def _zk_connect(self):

        ret = 1

        try:
            self.zk_conn = ZK(self.zk_ip, self.zk_port,
                                self.timeout, self.passwd,
                                self.fc_udp, self.om_png)

            self.zk_conn = self.zk_conn.connect()
            self.log.info(f" connected to machine, ip {self.zk_ip}")
            ret = 0
        except Exception as e:
            self.log.error(f"Except error to connect -> {self.zk_ip}, detail -> {e}")
            self.log.error(f"Except zk error, {sys.exc_info()}")
        finally:
            return ret

    def _zk_is_connected(self):

        try:
            if self.zk_conn:
                return True
            else:
                self.log.error(f"zk conn is {self.zk_conn}")
                return False
        except Exception as e:
            self.log.info(f"Except -> {e} ")
            self.log.error(f" Except {sys.exc_info()}")

    def _zk_disconnect(self):

        ret = 1

        try:
            if self._zk_is_connected():
                self.zk_conn.disconnect()
                self.log.info(f" disconnect from fingerprint, ip => {self.zk_ip}")
                ret = 0
        except Exception as e:
            self.log.info(f"Except -> {e} ")
            self.log.error(f" Except {sys.exc_info()}")
        finally:
            return ret

    def _zk_firmware(self):
        ret = 1

        try:
            if self._zk_is_connected():
                ret = self.zk_conn.get_firmware_version()
        except Exception as e:
            self.log.error(f" Except error , detail -> {e}")
            self.log.error(f" Except {sys.exc_info()}")
        finally:
            return ret

    def _zk_live_attendance(self):

        ret = 1

        try:
            if self._zk_is_connected():
                ret = self.zk_conn.live_capture(30)
        except Exception as e:
            self.log.error(f" Except error , detail -> {e}")
            self.log.error(f" Except {sys.exc_info()}")
        finally:
            return ret

    def _zk_get_attendance(self):

        ret = []

        tmp = {
            '1': "47714351",
            '2': "46373211",
            '4': "47598830",
            '5': "45448470",
            '6': "46027680"
        }

        try:
            if self._zk_is_connected():
                ret = self.zk_conn.get_attendance()

                if len(ret) == 0:
                    self.log.error(f"attendance is len = 0, {ret}")

        except Exception as e:
            self.log.error(f" Except error , detail -> {e}")
            self.log.error(f" Except {sys.exc_info()}")
        finally:
            return ret

    def _zk_clear_attendance(self):

        ret = 1

        try:
            if self._zk_is_connected():
                self.zk_conn.clear_attendance()
                ret = 0
        except Exception as e:
            self.log.error(f"Except error, detail -> {e}")
            self.log.error(f"Except {sys.exc_info()}")
        finally:
            return ret

    def _zk_reboot_machine(self):

        ret = 0

        try:
            if self._zk_is_connected():
                self.log.info(f"trying restart ip: {self.zk_ip}")
                if self.zk_conn.restart():
                    self._zk_disconnect()
                    ret = 0
        except Exception as e:
            self.log.error(f" Except error , detail: {e}")
            self.log.error(f" Except {sys.exc_info()}")
        finally:
            return ret
