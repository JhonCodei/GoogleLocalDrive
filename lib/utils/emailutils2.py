import sys
import socket
import os

import smtplib

import utils.strutils  as su
import utils.fileutils as fu
import utils.netutils  as nu

from email.message        import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address
from email.utils          import make_msgid
from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email                import encoders

# import os
# import smtplib
# import email
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email.utils import COMMASPACE, formatdate
# from email import encoders
#
# import utils.strutils  as su
# import utils.fileutils as fu
# import utils.netutils  as nu

class EmailUtils(object):
    """docstring for EmailUtils."""

    def __init__(self, em_cfg, logger):
        super(EmailUtils, self).__init__()
        self.em_cfg = em_cfg
        self.log    = logger
        self._set_em_config()

    def _set_em_config(self):

        self.em_server  = self.em_cfg['server_mail']    # Server connect
        self.em_port    = su.to_int_zero(self.em_cfg['server_port'])    # Port connect
        self.em_timeout = su.to_int_zero(self.em_cfg['server_timeout']) # Time out connect
        self.em_debug   = su.to_int_zero(self.em_cfg['server_debug'])   # Time out connect
        self.em_type    = self.em_cfg['type']          # type - text or html

        self.em_userlg  = self.em_cfg['user_login']    # user login
        self.em_pswdlg  = self.em_cfg['pswd_login']    # password login

        self.em_from    = self.em_cfg['from_mail']     # sender mail

        #----------------   BCC
        bcc_ls = []
        bcc_mail_spl = self.em_cfg['bcc_mail'].split(";")

        if len(bcc_mail_spl) > 1:
            for bcc in bcc_mail_spl:
                if len(su.to_str(bcc)) != 0:
                    bcc_ls.append(bcc)
        else: bcc_ls = self.em_cfg['bcc_mail']
        #----------------   BCC

        #----------------   CC
        cc_ls  = []
        cc_mail_spl  = self.em_cfg['cc_mail'].split(";")

        if len(cc_mail_spl) > 1:
            for cc in cc_mail_spl:
                if len(su.to_str(cc)) != 0:
                    cc_ls.append(cc)
        else: cc_ls = self.em_cfg['cc_mail']
        #----------------   CC

        #----------------   Address
        adr_ls = []

        adr_mail_spl = self.em_cfg['address_mail'].split(";")

        if len(adr_mail_spl) > 1:
            for adr in adr_mail_spl:
                if len(su.to_str(adr)) != 0:
                    adr_ls.append(adr)
        else: adr_ls = self.em_cfg['address_mail']
        #----------------   Address

        #----------------  Replay Address
        rpy_ls = []
        rpy_mail_spl = self.em_cfg['reply_to_mail'].split(";")

        if len(rpy_mail_spl) > 1:
            for rpy in rpy_mail_spl:
                if len(su.to_str(rpy)) != 0:
                    rpy_ls.append(rpy)

        else: rpy_ls = self.em_cfg['reply_to_mail']
        #----------------  Replay Address

        #----------------  file Attach

        fn_ls  = []
        fn_mail_spl = self.em_cfg['file_attach'].split(";")

        if len(fn_mail_spl) > 0:
            for fna in fn_mail_spl:
                if len(su.to_str(fna)) != 0:
                    fn_ls.append(fna)
        else: fn_ls.append(self.em_cfg['file_attach'])
        #----------------  file Attach

        self.em_bcc     = bcc_ls  # bcc mails - [ list ]
        self.em_cc      = cc_ls   # cc mails - [ list ]
        self.em_addrs   = adr_ls  # targets address email - [ list ]
        self.em_rp_to   = rpy_ls  # Reply to address email - [ list ]

        self.em_files   = [r"/home/ubuntu/Escritorio/python_project/python_apps/data/output/pedidos_2020_05_20200529_092510.csv"]#fn_ls   # Attachments files [ list ]

        self.em_subject = self.em_cfg['subject_mail']  # subject -
        self.em_text    = self.em_cfg['text_body']     # Contect plain text email


        # print(f" em_bcc = {self.em_bcc}\n")
        # print(f" em_cc = {self.em_cc}\n")
        # print(f" em_addrs = {self.em_addrs}\n")
        # print(f" em_rp_to = {self.em_rp_to}\n")
        # print(f" em_files = {self.em_files}\n")
        # print(f" em_subject = {self.em_subject}\n")
        # print(f" em_text = {self.em_text}\n")
        #
        # return False

    def _connect_server_mail(self):#

        ret = 1

        self.log.debug(f" Host = {self.em_server}\nport = {self.em_port} dbg = {self.em_debug}\ntimeout = {su.to_int_zero(self.em_timeout)}")

        try:
            self.smtp_server = smtplib.SMTP(self.em_server, su.to_int_zero(self.em_port))

            # if su.to_int_zero(self.em_debug) == 1:
            #     self.em_server.set_debuglevel(1)
            self.smtp_server.ehlo()
            self.smtp_server.starttls()
            self.smtp_server.ehlo()
        #     mailserver.ehlo()
        # mailserver.starttls()
        # mailserver.ehlo()
            ret = 0

        except socket.gaierror:
            self.log.error(f"Error connecting to {self.em_server}")
            self.log.error(f'Except {sys.exc_info()}')

        except socket.timeout:
            self.log.error(f"Timeout {su.to_int_zero(self.em_timeout)} sec. Connecting to {self.em_server}")
            self.log.error(f'Except {sys.exc_info()}')

        except:
            self.log.error(f'Except {sys.exc_info()}')

        finally:
            return ret

    def _login_smtp(self):#

        self.log.debug(f"user {self.em_userlg}\npwd = {self.em_pswdlg}")

        rc = 1
        try:
            emcn = self.smtp_server.login(self.em_userlg, self.em_pswdlg)
            self.log.critical(f"Connection em milaer -> {emcn}")
            rc = 0
        except Exception as e:
            self.log.error(f'_login_smtp {e}')
        except smtplib.SMTPAuthenticationError:
            self.log.error(f"Authenticating user {self.em_userlg}")
            self.log.error(f'Except {sys.exc_info()}')
        except:
            self.log.error(f'Except {sys.exc_info()}')
        finally:
            return rc

    def _logout_smtp(self):#
        self.smtp_server.quit()

    def _set_mail_hdr(self):#

        self.msg = MIMEMultipart()

        if len(str(self.em_subject)) == 0:
            self.em_subject = '-'

        if len(str(self.em_text)) == 0:
            self.em_text = '-'

        if len(str(self.em_from)) == 0:
            self.log.error(f'Except, Error -> {sys.exc_info()}')
            return 1

        self.msg['Subject'] = self.em_subject
        self.msg['From']    = self.em_from

        if len(self.em_bcc) == 0 and len(self.em_cc) == 0 and len(self.em_addrs):
            self.log.error(f"Nadie a quien enviar.")
            return 1

        if len(self.em_bcc) != 0:
            self.msg['Bcc'] = self.em_bcc

        if len(self.em_cc) != 0:
            self.msg['Cc'] = self.em_cc

        if len(self.em_addrs) != 0:
            self.msg['To'] = self.em_addrs

        if len(self.em_rp_to) != 0:
            self.msg['reply-to'] = self.em_rp_to

    def _is_attach_files(self):#REVISAR

        self.msg.attach(MIMEText(self.em_text, self.em_type))

        if len(self.em_files) != 0:
            for f in self.em_files:
                part = MIMEBase('application', "octet-stream")
                try:
                    with open(f, 'rb') as file:
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(f)}"')
                        self.msg.attach(part)

                        self.log.info(f" Attach file(s) => {len(self.em_files)}")
                except Exception as e:
                    self.log.error(f"Unable to open one of the attachments. Error => {e}")
                    self.log.error(f"Unable to open one of the attachments. Error => {sys.exc_info()[0]}")
                    raise
        else:
            self.log.info("nothing for attachment")

    def _send_mail(self):

        ret = 1

        self._set_mail_hdr()
        self._is_attach_files()

        self._connect_server_mail()

        #text = self.msg.as_string()
        #self.log.critical(f"TEXT => {text}")

        try:
            logIn = self._login_smtp()
            if logIn == 0:
                try:
                    snd = self.smtp_server.sendmail(self.em_from, self.em_addrs, self.msg.as_string())
                    self.log.info(f"send mail -> {snd}")

                    self._logout_smtp() # close connection SMTP

                    ret = 0
                except Exception as e:
                    self.log.error(f"Error send mail -> {e}")

        except Exception as e:
            self.log.error(f" Error en el envio, detalle -> {e}")
        return ret
