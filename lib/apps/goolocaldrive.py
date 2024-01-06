"""
Routes:
    CLIENT_SECRET_FILE -> example: data\input\goolocaldrive\credentials.json
    TOKEN_FILE         -> example: data\input\goolocaldrive\token.json
"""
__version__ = '20231118'

import sys
import os
import time

from datetime import datetime

import proc.process      as p
import utils.fileutils   as fu
import utils.netutils    as nu
import utils.strutils    as su

#from utils.emailutils    import EmailUtils
#from transport           import sshutil

from apps.pybase        import _PyBaseApp
#from statements.goolocaldrive  import _SQLGooLocalDrive

import io

from urllib.error import HTTPError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


current_date     = datetime.now().strftime('%Y%m%d')
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
SCOPE_DEL        = "||"

class GooLocalDrive(_PyBaseApp):
    def __init__(self):
        super(GooLocalDrive, self).__init__()
        self.exitOnError = False

        # Environmental variables:
        self.env_vars = {}

        # Configuration variables:
        self.config = {
                        'SCOPES'            : '',
                        'CLIENT_SECRET_FILE': '',
                        'TOKEN_FILE'        : '',
                        'API_NAME'          : '',
                        'API_VERSION'       : '',
                        'PATH_DOWNLOAD'     : '',
                        'FOLDER_DRIVE_ID'   : '',
                    }

        self.callqry = None
        self.em_cfg  = {}
        # Allowable commands for this application
        self.cmdStep = {
                        'C': self.create_update_credentials,
                        'G': self.getListFiles,
                        'R': self.__runcloud_to_localdrive,
                        'L': self.__run_list_drive
                        }
    # Use only for configuration values that need some manipulations/checks.
    
    def set_config_vars(self):
        #if self.runSeq2 is None or len(self.runSeq2) == 0: self.runSeq2 = 1 # required only in multiple similar sequences

        self.SCOPES             = self.config_vars['SCOPES'].split(SCOPE_DEL)
        self.CLIENT_SECRET_FILE = os.path.join(self.input_dir, self.appName, self.config_vars["CLIENT_SECRET_FILE"])
        self.TOKEN_FILE         = os.path.join(self.input_dir, self.appName, self.config_vars["TOKEN_FILE"])
        self.API_NAME           = self.config_vars['API_NAME']
        self.API_VERSION        = self.config_vars['API_VERSION']
        self.PATH_DOWNLOAD      = self.config_vars['PATH_DOWNLOAD']
        self.FOLDER_DRIVE_ID    = self.config_vars['FOLDER_DRIVE_ID']
        self.CREDS              = None
        self.SERVICE_API        = None

        self.SRC_FIELDS = "files(id, name, mimeType)"
        self.SRC_QUERY  = None

        self.mimeType_Folder = 'application/vnd.google-apps.folder'

        self.FolderFinder = []
        return 0
    # end set_config_vars
    
    """'''''''''''''''''''''''''"""
    """ 1) -> GooLocalDrive """
    """'''''''''''''''''''''''''"""
    def search_query(self, id):
        self.SRC_QUERY  = f"'{id}' in parents"
    # end search_query


    def file_helper_extension(self, name, type):
        dct = {
            'application/vnd.google-apps.spreadsheet': ".xlsx"
            ,'application/vnd.google-apps.document': ".docx"
            ,'application/vnd.google-apps.presentation': ".pptx"
        }
        if dct[type] is None: return None

        return f"{name}{dct[type]}"
    #end file_helper_extension


    def mimeType_conversion(self, type):
        dct = {
            'application/vnd.google-apps.spreadsheet': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ,'application/vnd.google-apps.document': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ,'application/vnd.google-apps.presentation': "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        }
        if dct[type] is None: return None
        return f"{dct[type]}"
    #end mimeType_conversion


    def create_update_credentials(self):
        """ *** WARNING ***
        If the token file does not exist, the application will send a request on the screen for API authorization
        """
        rc = 101
        try:
            if fu.file_exists(self.TOKEN_FILE):
                self.CREDS = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
                rc = 0
            else:
                self.log.info(f"File {self.TOKEN_FILE} not exist, creating ...")

            if not self.CREDS or not self.CREDS.valid:    
                self.log.warning(f"Tokken not valid {self.CREDS} ")
                if self.CREDS and self.CREDS.expired and self.CREDS.refresh_token:        
                    self.log.warning(f"Tokken expired, refresh... ")
                    self.CREDS.refresh(Request())        
                else:
                    self.log.warning(f"Tokken expired, create... ")
                    flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRET_FILE, self.SCOPES)
                    self.CREDS = flow.run_local_server(port=0)
                
                self.log.warning(f"Tokken expired, write... ")
                
                fu.create_file(self.TOKEN_FILE, self.CREDS.to_json(), self.log)
        except Exception:
            self.log.error(f'Except {sys.exc_info()}')
            self.CREDS = None
            rc = 101
        finally:
            return rc
    # end setCredentials


    def set_service_api(self):
        rc = 0
        try:
            self.SERVICE_API = build(self.API_NAME, self.API_VERSION , credentials = self.CREDS)
        except Exception as ex:
            self.log.error(f'Ocurrió un error {ex}')
            rc = 1
        finally:
            return rc
    # end set_service_api


    def getListFiles(self, Query, fields):    
        lst = []
        try:
            ##### getAllFilesFrom Folder id #############    
            results =  self.SERVICE_API.files().list(q = Query, fields = fields).execute()
            lst = results.get('files', [])        
            if not lst:
                self.log.error("No items")
        except Exception as ex:
            self.log.error(f'Error Exception -> {ex}')
        except HttpError as error:
            self.log.error(f'Error HttpError -> {error}')
        finally:
            return lst
    # end getListFiles
        
    
    def request_download(self, element_id, element_name, element_type):
        rc = None
        try:
            if "vnd.google-apps" not in element_type:
                rc = self.SERVICE_API.files().get_media(fileId=element_id)
            else:
                element_type_tmp = self.mimeType_conversion(element_type)
                if element_type_tmp is None:
                    self.log.error(f"File {element_name}, mimeType {element_type_tmp} invalid extension, ignore file ...")
                else:
                    rc = self.SERVICE_API.files().export_media(fileId=element_id, mimeType=element_type_tmp)
        except Exception as ex:
            self.log.error(f"File {element_name}, mimeType {element_type_tmp} \n {ex}")
            rc = None
        finally:
            return rc
    #end request_download

    
    def downloader_file(self, ofn, requestIO, element_id, element_name):
        rc = 101
        try:
            fh = io.FileIO(ofn, 'wb')
            downloader = MediaIoBaseDownload(fh, requestIO)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                self.log.info(f"Downloaded {int(status.progress() * 100)}% of {element_name}")
            rc = 0
        except Exception as ex:
            self.log.error(f"Downloader file id: {element_id} name: {element_name}, error -> {ex}")
            self.log.error(f"Downloader file id: {element_id} name: {element_name}, ignore file ...")
            rc = 101
        finally:
            return rc
    #end downloader_file


    def file_name_helper(self, element_name, element_type):
        rc = None
        try:
            if fu.file_extension_exist(element_name) is False:
                element_name_tmp = self.file_helper_extension(element_name, element_type)
                if element_name_tmp is None:
                    self.log.error(f"File {element_name} invalid extension, ignore file ...")
                    rc = None
                else: rc = element_name_tmp  
            else: rc = element_name
        except Exception as ex:
            self.log.error(f"File {element_name} invalid extension, ignore file ... detail => {ex}")
            rc = None
        finally:
            return rc
    #end file_name_helper

    
    def __cloud_to_localdrive__download(self, element_id, destination_path):
        rc = 101
        self.search_query(element_id)
        self.log.info(f" self.SRC_QUERY -> {self.SRC_QUERY} ")

        try:
            items = self.getListFiles(self.SRC_QUERY, self.SRC_FIELDS)

            if not items:
                self.log.error('No files found.')
                return rc

            self.log.debug(f"read list -> {items}")

            for item in items:
                rc = 0
                element_id   = item['id']
                element_name = item['name']
                element_type = item['mimeType']

                self.log.debug(f"working with element -> id: {element_id} \n name: {element_name} \n type: {element_type} \n")

                if element_type == self.mimeType_Folder:
                    # It's a subfolder, recursively download its contents
                    if element_id not in self.FolderFinder: self.FolderFinder.append(element_id)

                    subfolder_path = os.path.join(destination_path, element_name)
                    os.makedirs(subfolder_path, exist_ok=True)
                    self.__cloud_to_localdrive__download(element_id, subfolder_path)
                else:
                    # It's a file, download it
                    element_name = self.file_name_helper(element_name, element_type)

                    if element_name is None: continue

                    # join a new path with name file
                    ofn = os.path.join(destination_path, element_name)

                    if fu.file_exists(ofn):
                        self.log.info(f"{ofn} exist...build new name and rename file")
                        nofn = fu.file_altername_extension(ofn)
                        fu.file_rename(ofn, nofn)

                    requestIO = self.request_download(element_id, element_name, element_type) 

                    if requestIO is None:
                        self.log.error(f"File {element_name} invalid extension, ignore file ...")
                        continue        

                    downloader = self.downloader_file(ofn, requestIO, element_id, element_name)

                    if downloader == 0:
                        self.delete_from_id(element_id)
            #end For
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
            rc = 101
        finally:
            return rc      
    # end __cloud_to_localdrive__download
    
    
    def delete_from_id(self, fileId):
        try:
            self.SERVICE_API.files().delete(fileId=fileId).execute()
            self.log.info(f'Element with ID {fileId} deleted successfully.')
        except Exception as e:
            self.log.error(f'An error occurred: {e}')
    # end delete_from_id
            

    def __runcloud_to_localdrive(self):
        ret = 0
        
        ret = self.create_update_credentials()

        if ret != 0: ret = self.create_update_credentials() # call again when credentials has been updated
        
        if ret == 0: ret = self.set_service_api()

        if ret == 0:
            ret = self.__cloud_to_localdrive__download(self.FOLDER_DRIVE_ID, self.PATH_DOWNLOAD)

            # list contains folder downloaded...
            self.log.info(f" self.FolderFinder -> {self.FolderFinder}")
            if len(self.FolderFinder) > 0:
                for fd in self.FolderFinder:
                    self.delete_from_id(fd)
            self.FolderFinder = []
            ret = 0
        else:
            self.log.error("API has not been initialized")
        return ret
    # end __runcloud_to_localdrive


    def __run_list_drive(self):
        ret = 0
        
        ret = self.create_update_credentials()

        if ret != 0: ret = self.create_update_credentials() # call again when credentials has been updated
        
        if ret == 0: ret = self.set_service_api()

        if ret == 0:
            self.search_query(self.FOLDER_DRIVE_ID)

            self.log.info(f" self.SRC_QUERY -> {self.SRC_QUERY} ")
            items = self.getListFiles(self.SRC_QUERY, self.SRC_FIELDS)

            print(items)
            
            ret = 0
        else:
            self.log.error("API has not been initialized")
        return ret
    # end __run_list_drive


def main(Args):
    a = GooLocalDrive()
    rc = a.main(Args)
    return rc


if __name__ == '__main__':
    rc = main(sys.argv)
    sys.exit(rc)
