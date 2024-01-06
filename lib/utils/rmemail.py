"""
@author: eocampo
This module implements email functionality.

Modification History
date-author-description

"""
__version__ = '20181113'

import sys
import socket
import os

import smtplib

import utils.strutils as su
import utils.fileutils as fu
import utils.netutils as nu

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address
from email.utils import make_msgid
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

RET_WARN = 101

class Email(object):

    def __init__(self, smcfg, logger):

        self.appName     = self.__class__.__name__.lower()
        self.smtp_cfg    = smcfg         # Host Configuration.
        self.log         = logger
        self.host        = smcfg['Smtp'] # Client app config. Host Name
        self.smtp_server = None          # handler to Host (smtp)
        self.msg         = None
        self.toaddr      = []            # Hold recipients addresses.

    # ---------------------------------------  SMTP Connectivity ------------------------------------#
    # All checks STMP related variables are check in this method. No need to check in client module.
    # host = Mail Server (STMP)
    # port = stmp port
    # dbg = debug mail
    # timeout = max time to wait to establish connectivity.
    # Returns None or a server handler

    def _connect_smtp(self):

        ret = 1

        self.log.debug(f"host = {self.smtp_cfg['Smtp']}\nport = {self.smtp_cfg['Port']}"
                       "\ndbg = {self.smtp_cfg['Stmp_Dbg']}\ntimeout = {self.smtp_cfg['Time_Out'])}")

        if nu.is_valid_ip(self.smtp_cfg['Stmp']) is False:

            self.log.error(f"Config: Invalid STMP Ip {self.smtp_cfg['Stmp']}")
            return ret

        try:
            self.smtp_server = smtplib.SMTP(self.smtp_cfg['Stmp'],
                               su.to_int_zero(self.smtp_cfg['Port']),
                               timeout=su.to_int_zero(self.smtp_cfg['Time_Out']))

            if su.to_int_zero(self.smtp_cfg['Stmp_Dbg']) == 1:
                self.smtp_server.set_debuglevel(1)

            ret = 0

        except socket.gaierror:
            self.log.error(f"Error connecting to {self.smtp_cfg['Stmp']}")
            self.log.error(f'Except {sys.exc_info()}')

        except socket.timeout:
            self.log.error(f"Timeout {self.smtp_cfg['Time_Out'])} sec. Connecting to {self.smtp_cfg['Smtp']}")
            self.log.error(f'Except {sys.exc_info()}')

        except:
            self.log.error(f'Except {sys.exc_info()}')

        finally:
            return ret

    def _login_smtp(self):

        self.log.debug(f"user {self.smtp_cfg['Mail_User']}\npwd = {self.smtp_cfg['Pwd']}")

        rc = 1
        try:
            self.smtp_server.login(self.smtp_cfg['Mail_User'], self.smtp_cfg['Pwd'])
            rc = 0

        except smtplib.SMTPAuthenticationError:
            self.log.error(f"Authenticating user {self.smtp_cfg['Mail_User']}")
            self.log.error(f'Except {sys.exc_info()}')

        except:
            self.log.error(f'Except {sys.exc_info()}')

        finally:
            return rc

    def _set_mail_hdr(self):

        self.msg['Subject'] = "EO TODO Implement mechanism"
        self.msg['From']    = self.smtp_cfg['From_Addr']

    # Opens a file and returns a comma(,) separated string.
    # Sets the message label if a file is present and string is not empty.
    # Checks for valid email address.
    def _set_addr(self, fn, label):

        addr     = []
        val_addr = []
        bad_addr = []
        if not fu.file_exists(fn):
            self.log.warning(f'{label} File {fn} does not exists')
            return 1

        addr = fu.read_file_list(fn, self.log)

        if len(addr) < 1:
            self.log.warning(f'File {fn} does not exists has no records')
            return 2

        for a in addr:
            val_addr.append(a) if su.is_valid_email(addr) else bad_addr.append(a)

        if len(bad_addr) > 0:
            self.log.error(f'fn = {fn} Invalid Adresses {bad_addr}')

        if len(val_addr) < 0:
            return 3

        addr = ','.join(str(s) for s in val_addr)
        self.msg[label] = addr
        self.log.info(f'Loaded from {fn} -- {len(val_addr)} valid emails ')
        self.log.debug('{label} == {addr}')
        self.toaddr += val_addr

        return 0

        # msg_from = nu.domain_split(self.smtp_cfg['Mail_User'])
        #if msg_from is not None:
        #    self.msg['From'] = msg_from[0]

        # else:
        #     self.msg['From'] = msg_from

    # This method send plain msgs's w/no images embeded in the body.
    def send_plain_email(self,mbody, attach=[], rd = 'plain'):

        toaddr = []

        # Establish SMTP  Connection
        ret = self._connect_smtp()
        if ret != 0:
            return ret

        # Start creating the Message
        self.msg = MIMEMultipart()
        self._set_mail_hdr()
        for fn, lbl in ((self.smtp_cfg['To_Addr'], 'To'),
                        (self.smtp_cfg['Cc_Addr'], 'Cc'),
                        (self.smtp_cfg['Bcc_Addr'],'Bcc')):

            ret = self._set_addr(self, fn, lbl)
            self.log.debug(f'_set_addr ret = {ret} lbl = {lbl} fn ={fn}')

        self.msg.attach(MIMEText(mbody, rd))

        # Add Attachments if any.
        for f in attach:
            fn = os.path.basename(f)
            # instance of MIMEBase and named as part
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            # part.add_header('Content-Disposition', 'attachment; filename="%s"' % fn)
            part.add_header('Content-Disposition', f'attachment; filename={fn}')

            self.msg.attach(part)
            self.log.debug(f'Attaching {fn}')

        # Converts the Multipart msg into a string
        text = self.msg.as_string()
        self.smtp_server.sendmail(self.msg['From'], self.toaddr, text)

        self.stmp_server.quit()
