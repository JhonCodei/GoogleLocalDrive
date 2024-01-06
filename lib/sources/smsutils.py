import os
import sys
import time
import utils.strutils as su
import serial

class SMSUtil(object):
    """
    # docstring for SMSUtil|
    ------------------------
    - Connect
    - Disconnect
    - Listen Serial
    - Sends commands
    - Send SMS
    """

    def __init__(self, portcom, phone, text, logger, tm=5):
        super(SMSUtil, self).__init__()

        self.portcom = portcom
        self.log     = logger
        self.timeout = tm
        self.com     = None
        self.phone   = phone
        self.text    = text

    def serial_connect(self):
        try:
            self.com = serial.Serial(self.portcom, 9600, timeout = self.timeout)
            self.log.info(f"serial -> {self.portcom}, connected")
        except Exception as e:
            self.log.error(f" Error connect, detail -> {e}")

    def serial_disconnect(self):
        if self.com != None:
            self.com.close()
            self.log.info(f" Disconnect port -> {self.portcom}")

    def listen_serial(self):
        self.serial_connect()
        if self.com != None:
            while True:
                self.log.critical(f"leer => {self.com.readline()}")
                print(f"leer => {self.com.readline()}")
        self.log.error("No connected!!!")

    def send_commands(self, commands, stepsleep=0):
        self.com.write(su.__str__encode__(f'{commands}\r'))
        self.log.info(f" send command -> {commands} , sleep -> {stepsleep}.")
        time.sleep(stepsleep)

    def send_sms(self):
        cmds = ['ATZ', 'AT+CMGF=1', f'AT+CMGS="{self.phone}"', f'{self.text}', chr(26)]
        mxln = len(cmds) - 1
        i    = 0
        self.serial_connect()
        for s in cmds:
            if i != mxln:
                self.send_commands(s, 2)
                i = i + 1
            else:
                self.send_commands(s)
        self.serial_disconnect()
