"""
SSHTunnel Util
- build tunnel connection over ssh

pip install sshtunnel
"""

__version__ = "20190831"

import sshtunnel
import sys

sshtunnel.SSH_TIMEOUT    = 5.0 # Should be in configure File
sshtunnel.TUNNEL_TIMEOUT = 5.0 # Should be in configure File

class SSHTunnel:

    def __init__(self, sshcs, logger, encode=str):

        self.ssh_str  = sshcs
        self.tunnel   = None
        self.log      = logger
        self.encode   = encode
        self.sep      = ','

    def establish_ssh_tunnel(self):

        connection_success = False

        while not connection_success:
            try:
                self.tunnel = sshtunnel.SSHTunnelForwarder(
                                (self.ssh_str['ssh_host'], self.ssh_str['ssh_port']),
                                ssh_password=self.ssh_str['ssh_pwsd'],
                                ssh_username=self.ssh_str['ssh_user'],
                                remote_bind_address=(self.ssh_str['ssh_rmip'],
                                                        self.ssh_str['ssh_rmpt']))
                connection_success = True
            except Exception as e:
                self.log.error(f"Error ssh connection => {e}")
                self.log.error(f'Except {sys.exc_info()}')
            finally:
                self.start_ssh()
                return self.tunnel.local_bind_port


    def start_ssh(self):
        self.tunnel.start()
        self.log.info(" ssh connection started !")


    def stop_ssh(self):
        self.tunnel.stop()
        self.log.info(" ssh connection has been closed ! ")
