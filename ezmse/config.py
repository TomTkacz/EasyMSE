from configparser import ConfigParser
from os.path import isfile,isdir,abspath
from os import getcwd,listdir
from pathlib import Path
from .error import *

packageRootDirectory = Path(__file__).parent.resolve()
configPath = packageRootDirectory / 'include' / 'config.ini'

if not isfile(configPath):
    print("Could not locate ezmse's include/config.ini file. Try reinstalling ezmse.")

class MSEConfig(ConfigParser):

    def __init__(self):
        super().__init__()
        self.read(packageRootDirectory / 'include' / 'config.ini')
    
    def update(self):
        with open(packageRootDirectory / 'include' / 'config.ini', 'w') as f:
            self.write(f)

    def wipe(self,section=None,option=None):
        if not section:
            for section in self.sections():
                for option in self.options(section):
                    self[section][option] = ''
        elif not option:
            for option in self.options(section):
                self[section][option] = ''
        self[section][option] = ''
        self.update()

    def __validatePaths(self):
        folderPath = Path( self['file-locations']['mse-folder'] )
        setPath = Path( self['file-locations']['mse-set'] )
        exePath = Path( self['file-locations']['mse-exe'] )
        comPath = Path( self['file-locations']['mse-com'] )
        
        if self['file-locations']['mse-folder']=='' or not isdir(folderPath) or not isdir(folderPath/"data") or not isdir(folderPath/"resource"):
            raise DirectoryNotFoundError(f"Directory ({str(folderPath)}) must contain MSE's 'data' and 'resource' folders.")
        
        if self['file-locations']['mse-set']=='' or not isfile(setPath.absolute()) or not str(setPath).endswith(".mse-set"):
            raise SetNotFoundError(f"No valid .mse-set file found at {setPath.cwd()}")
        
        if self['file-locations']['mse-exe']=='' or not isfile(exePath) or ( not str(exePath).endswith("mse.exe") and not str(exePath).endswith("magicseteditor.exe") ):
            raise EXENotFoundError(f"No valid MSE .exe found at {str(exePath.absolute())}")
        
        if self['file-locations']['mse-com']=='' or not isfile(comPath) or ( not str(comPath).endswith("mse.com") and not str(comPath).endswith("magicseteditor.com") ):
            raise COMNotFoundError(f"No valid MSE .com found at {str(comPath.absolute())}")
        
    # try to implicitly resolve path errors
    def resolvePaths(self,updateConfigFile=False):

        cwdPath = Path(getcwd())

        try:
            self.__validatePaths()

        except DirectoryNotFoundError:
            if isdir(cwdPath / "data" ) and isdir(cwdPath/"resource"):
                self['file-locations']['mse-folder'] = str(cwdPath)
                self.resolvePaths()

        except SetNotFoundError:

            for f in listdir(getcwd()):
                if f.endswith(".mse-set"):
                    self['file-locations']['mse-set'] = str( cwdPath / f )
                    self.resolvePaths()
                    break

        except EXENotFoundError:

            if isfile( cwdPath / "mse.exe" ):
                self['file-locations']['mse-exe'] = str( cwdPath / "mse.exe" )
                self.resolvePaths()
            elif isfile( cwdPath / "magicseteditor.exe" ):
                self['file-locations']['mse-exe'] = str( cwdPath / "magicseteditor.exe" )
                self.resolvePaths()

        except COMNotFoundError:

            if isfile( cwdPath / "mse.com" ):
                self['file-locations']['mse-com'] = str( cwdPath / "mse.com" )
                self.resolvePaths()
            elif isfile( cwdPath / "magicseteditor.com" ):
                self['file-locations']['mse-com'] = str( cwdPath / "magicseteditor.com" )
                self.resolvePaths()

        if updateConfigFile:
            self.update()
        
mseConfig = MSEConfig()
mseConfig.resolvePaths(True)
mseConfig.update()