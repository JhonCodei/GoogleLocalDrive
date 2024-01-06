"""
Descripcion:
    - Utilizado para la creación de archivos dependientes de un nuevo app que formara parte del framework creado "PYTHON_APPS"
    - Los archivos que se generaran, seran con el codigo base necesario definido en base a la versión actual de framework "PYTHON_APPS"

    #############################
    # Arbol de archivos creados #
    #############################
    ----------------------------------
    ······· config/
    ············· -> [nombre_app].cfg
    ----------------------------------
    ······· lib/
    ············ apps/
    ············· -> [nombre_app].py
    ----------------------------------
    ······· lib/
    ············ statements/
    ············· -> [nombre_app].py
    ----------------------------------
    ······· scripts/
    ············ [nombre_app]/
    ············· -> [nombre_app]_os_win.bat  [Windows]
    ············· -> [nombre_app]_os_unx.sh   [linux / OsX]
    ----------------------------------

"""
__version__ = '20210618'

import sys
import os
import time
import platform

from datetime import datetime

import proc.process      as p
import utils.fileutils   as fu
import utils.netutils    as nu
import utils.strutils    as su

from apps.pybase        import _PyBaseApp

current_date     = datetime.now().strftime('%Y%m%d')
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

class Makeproject(_PyBaseApp):

    def __init__(self):

        super(Makeproject, self).__init__()
        self.exitOnError = False

        # Environmental variables:
        self.env_vars = {}

        # Configuration variables:
        self.config = {
                        'configuracion' : '',
                        'aplicativo'    : '',
                        'statement'     : '',
                        'script'        : '',
                    }

        self.callqry = None
        self.em_cfg  = {}
        # Allowable commands for this application
        self.cmdStep = {
                        'Z': self.opciones_creacion,
                        'C': self.archivo_cfg,
                        'A': self.archivo_app,
                        'S': self.archivo_statement,
                        'X': self.archivo_scripts,
                        }
    # Use only for configuration values that need some manipulations/checks.
    def set_config_vars(self):

        #if len(self.runSeq2) == 0: self.runSeq2 = 1
        print("\n\n")
        self.runSeq2 = su.to_str( input("········································\n···· Ingrese un nombre de aplicativo: #") ).lower()
        
        self.dr_base = self.base_dir
        self.dir_cfg = os.path.join(self.dr_base, self.config_vars["configuracion"] )
        self.dir_app = os.path.join(self.dr_base, self.config_vars["aplicativo"]    )
        self.dir_stm = os.path.join(self.dr_base, self.config_vars["statement"]     )
        self.dir_scp = os.path.join(self.dr_base, self.config_vars["script"]        )

        self._()

        return 0

    """'''''''''''''''''''''''''"""
    """ 1) -> Makeproject """
    """'''''''''''''''''''''''''"""

    def _(self):
        if len( self.runSeq2 ) == 0:
            self.log.error(f"No se ha ingresado ningun nombre, creación cancelada.")
            return 1
        #else: self.runSeq2 = f"borrar_{self.runSeq2}"
    
    def _runAll(self):
        self.archivo_cfg() 
        self.archivo_app()
        self.archivo_statement()
        self.archivo_scripts()
        return 0
    
    def creacion_archivo_contenido(self, dirName, appName, content, op="N"):

        if fu.folder_exists(dirName) is False: nu.make_folder(self.log, dirName)

        full_path = os.path.join(dirName, appName)
        print(f" Verificando archivo -> ' {full_path} '")
        
        if fu.file_exists(full_path) and op == "N":
            self.log.warning(f"El archivo {appName}, ya existe en la ruta {dirName} .")
            print(f"El archivo ' {appName} ', ya existe en la ruta ' {dirName} ' .\n Desea volver a generar el archivo?, tenga en cuenta que se borrara todo contenido. ¿Proceder? \n 0: Si, proceder \n 1: No, cancelar")
            
            crear_otra_vez = su.to_str(input(" Ingrese respuesta: ")).lower()
            
            if crear_otra_vez == "0":
                self.creacion_archivo_contenido(dirName, appName, content, "R")
            else:
                self.log.warning(f"Sin acciones, Cancelado ...")
                return 1
        else:
            self.log.debug(f"creando archivo {appName} en la ruta {dirName} .")
            crear_archivo = fu.create_file( full_path, content, self.log )
            
            if  crear_archivo == 0:
                self.log.info(f"El archivo {appName}, fue creado exitosamente en la ruta {dirName} .")
            else:
                self.log.error(f"{sys.exc_info()}")
                return 1
        return 0

    def opciones_creacion(self):

        appName = self.runSeq2

        if  platform.system() == 'Windows': ScriptName = f"{appName}_os_win.bat"
        else                              : ScriptName = f"{appName}_os_unx.sh"

        msj = f"""········································\n···· OPCIONES DE CREACION: '' {appName} ''\n········································
            C = Crear archivo config/{appName}.cfg
            A = Crear archivo lib/apps/{appName}.py
            S = Crear archivo lib/statements/{appName}.py
            X = Crear archivo scripts/{appName}/{ScriptName}

            T = Crear los archivos: 
                    -   config/{appName}.cfg
                    -   lib/apps/{appName}.py
                    -   lib/statements/{appName}.py
                    -   scripts/{appName}/{ScriptName}

            E = Cancelar crearcion
        """
        print(msj)

        respuesta = su.to_str( input( "Ingrese una respuesta: " ) ).lower()

        if   respuesta == "c"   : self.archivo_cfg()
        elif respuesta == "a"   : self.archivo_app()
        elif respuesta == "s"   : self.archivo_statement()
        elif respuesta == "x"   : self.archivo_scripts()
        elif respuesta == "t"   : self._runAll()
        else                    : self.log.warning("Cancelando acciones")
        
        return 0
    #######################

    def archivo_cfg_contenido(self):
        return f"""[DEFAULT]
        
variable1 = ejemplo1"""

    def archivo_cfg(self):#C
        """ ruta -->  config/app.cfg """

        app     = f"{self.runSeq2}.cfg"
        content = self.archivo_cfg_contenido()

        return self.creacion_archivo_contenido( self.dir_cfg, app, content )

    #######################
    def archivo_app_contenido(self):
        description = '''"""
Description
-----------
"""'''
        llaves   = "{ }"
        cmdSteps = """{
                        'T': self.test,
                       } """
        varCfgs  = """{
                        'variable1'  : '',
                      }"""

        return f"""\
{description}
__version__ = '{current_date}'

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
from statements.{self.runSeq2}  import _SQL{self.runSeq2.capitalize()}

current_date     = datetime.now().strftime('%Y%m%d')
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')


class {self.runSeq2.capitalize()}(_PyBaseApp):

    def __init__(self):

        super({self.runSeq2.capitalize()}, self).__init__()
        self.exitOnError = False

        # Environmental variables:
        self.env_vars = {llaves}

        # Configuration variables:
        self.config = {varCfgs}

        self.callqry = _SQL{self.runSeq2.capitalize()}()
        self.em_cfg  = {llaves}
        # Allowable commands for this application
        self.cmdStep = {cmdSteps}
    # Use only for configuration values that need some manipulations/checks.
    def set_config_vars(self):
        # [if use 2 args in script file]
        if len(self.runSeq2) == 0: self.runSeq2 = 1

        self.variable1  = self.config_vars[f'variable1']

        return 0

    #####################################
    ######## {self.runSeq2.upper()} ###############
    #####################################
    def test(self):

        ret = 0
        print("123-test")
        return ret

def main(Args):

    a = {self.runSeq2.capitalize()}()
    rc = a.main(Args)
    return rc

if __name__ == '__main__':

    rc = main(sys.argv)
    sys.exit(rc)
        """

    def archivo_app(self):#A
        """ ruta -->  lib/apps/app.py """

        app     = f"{self.runSeq2}.py"
        content = self.archivo_app_contenido()
        return self.creacion_archivo_contenido( self.dir_app, app, content )

    #######################
    def archivo_statement_contenido(self):
        return f"""\
class _SQL{self.runSeq2.capitalize()}(object):

    def _example_sql(self):
        return ""
        """

    def archivo_statement(self):#S
        """ ruta -->  lib/statements/app.py """

        app     = f"{self.runSeq2}.py"
        content = self.archivo_statement_contenido()
        return self.creacion_archivo_contenido( self.dir_stm , app, content )

    #######################
    def archivo_scripts_contenido(self):

        PROJECT_BASE = os.path.dirname(self.base_dir)
        PROJECT_APP  = os.path.split(self.base_dir)
        DTM = "{DTM}"

        def os_windows():
            return f"""REM Run Application
            
SET PROJECT_BASE={PROJECT_BASE}
SET PROJECT_APP=%PROJECT_BASE%/{PROJECT_APP[-1]}

REM Debug options
SET LOG_LEVEL=DEBUG

REM Notification options
SET MAIL_LIST=%ADMIN_MAIL%
SET PAGER_LIST=%ADMIN_PGR%
REM export MAIL_ON_ERR=T
REM export PAGE_ON_ERR=T

REM For Timestamps
REM export DTM=`date '+%Y%m%d.%H.%M.%S'`
REM export DT=`date '+%Y%m%d'`
SET DTL=%DATE:~6,8%-%DATE:~3,2%-%DATE:~0,2%
SET LOG_DIR=%PROJECT_APP%/log/%DTL%
REM export LOG_NAME=`basename $0`.${DTM}

REM SET PYTHONINTR=python
SET PYTHONINTR=%PROJECT_APP%/virtual_environment/Scripts/python.exe
SET PYTHONPATH=%PROJECT_APP%/lib

%PYTHONINTR% %PROJECT_APP%/lib/apps/{self.runSeq2}.py T 1"""
            
        def os_unix():
            LOG_FNAME = "{LOG_FNAME%.*}"
            return f"""#Run Application
export PROJECT_BASE={PROJECT_BASE}
export PROJECT_APP=$PROJECT_BASE/{PROJECT_APP[-1]}

# Debug options
export LOG_LEVEL=DEBUG

# Notification options
export MAIL_LIST=$ADMIN_MAIL
export PAGER_LIST=$ADMIN_PGR
#export MAIL_ON_ERR=T
#export PAGE_ON_ERR=T

#For Timestamps
export DTM=`date '+%Y%m%d.%H.%M.%S'`
export DT=`date '+%Y%m%d'`

export LOG_DIR=$PROJECT_APP/log
#export LOG_FNAME=`basename $0`
#export LOG_NAME="${LOG_FNAME}".${DTM}
export PYTHONINTR=$PROJECT_APP/virtual_environment/bin/python3
#$APP_BASE/PycharmProjects/venv/sms/bin/python3.6
export PYTHONPATH=$PROJECT_APP/lib

$PYTHONINTR $PROJECT_APP/lib/apps/{self.runSeq2}.py T 1"""
        
        if  platform.system() == 'Windows': return os_windows()
        else                              : return os_unix()

    def archivo_scripts(self):#X
        """ 
        ruta -->  scripts/app_os_win.bat 
        ruta -->  scripts/app_os_unx.sh
        """

        folder = os.path.join( self.dir_scp, self.runSeq2 )

        if  platform.system() == 'Windows': app = f"{self.runSeq2}_os_win.bat"
        else                              : app = f"{self.runSeq2}_os_unx.sh"
        
        content = self.archivo_scripts_contenido()
        return self.creacion_archivo_contenido( folder , app, content )

def main(Args):

    a = Makeproject()
    rc = a.main(Args)
    return rc

if __name__ == '__main__':

    rc = main(sys.argv)
    sys.exit(rc)
