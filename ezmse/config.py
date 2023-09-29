from configparser import ConfigParser
from os.path import isfile,isdir
from os import getcwd
from pathlib import Path

rootDirectory = Path(__file__).parent.resolve()
config = ConfigParser()
config.read(rootDirectory / 'include' / 'config.ini')

def update():
    with open(rootDirectory / 'include' / 'config.ini', 'w') as f:
        config.write(f)
    config.read(rootDirectory / 'include' / 'config.ini')
    
def wipe(section=None,option=None):
    if not section:
        for section in config.sections():
            for option in config.options(section):
                config[section][option] = ''
    elif not option:
        for option in config.options(section):
                config[section][option] = ''
    config[section][option] = ''
    update()

def setMSEFolder(path):
    if type(path) is str:
        path = Path(path)
    if isdir(path/'data') and isdir(path/'resource') and isfile(path/'magicseteditor.com') and isfile(path/'magicseteditor.exe'):
        config['file-locations']['mse-folder'] = str(path)
        config['file-locations']['mse-exe'] = str(path / 'magicseteditor.exe')
        config['file-locations']['mse-com'] = str(path / 'magicseteditor.com')
        update()
    else:
        print("folder must contain the files 'magicseteditor.exe' 'magicseteditor.com' and the directories 'data' 'resource'")

if config['file-locations']['mse-folder'] == '':
    setMSEFolder(Path(getcwd()))
     
if isfile(rootDirectory / 'include' / 'set.mse-set'):
    config['file-locations']['mse-set'] = str(rootDirectory / 'include' / 'set.mse-set')
    update()