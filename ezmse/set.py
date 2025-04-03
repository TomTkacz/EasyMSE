from json import loads as jsonloads
from zipfile import ZipFile
from pathlib import Path
from os import rename,remove
from os.path import dirname,isfile,isdir
from datetime import datetime

from .config import mseConfig
from .error import DirectoryNotFoundError

DEFAULT_STYLE = "m15-altered" # TODO: have additional checks to ensure the default style is actually there

# configures and creates .mse-set files
class SetConfiguration:
        
    # sets values when writing to the set file
    def __jsonCustomAttribValuesHook(self,obj):

        def set(k,v):
            if k in list(obj.keys()):
                obj[k]=v
                
        currentTimeFormatted = str(datetime.today()).split(".")[0]
                
        set('stylesheet',f"{self.styleName}")
        set('time_created',currentTimeFormatted)
        set('time_modified',currentTimeFormatted)
        set('copyright',f"{currentTimeFormatted[:4]} - TomTkacz on Github (MIT License)")
        
        return obj
    
    def __init__(self,setStyle=DEFAULT_STYLE):

        styleDirectory = Path(mseConfig['file-locations']['mse-folder'])/"data"/f"magic-{setStyle}.mse-style"
        if not isdir(styleDirectory):
            raise DirectoryNotFoundError(f"The directory '{styleDirectory}' was not found.")
        
        self.styleName = setStyle
        self.styleDirectory = styleDirectory

        with open( Path(dirname(__file__))/"include"/"set.json","r") as f:
            
            self._attribs = jsonloads(
                f.read(),
                object_hook = self.__jsonCustomAttribValuesHook
            )["set_default"]
    
    def __getattr__(self, name):
        try:
            return self.__dict__["_attribs"][name]
        except:
            return self.__dict__[name]
        
    def __setattr__(self, name, value):
        try:
            self.__dict__["_attribs"][name] = value
        except:
            self.__dict__[name] = value
    
    def __str__(self):
        return str(self._attribs)
    
    # TODO: get rid of multiple newlines after nested dicts
    def format(self,attribDict=None,indent=0):
        attribDict = self._attribs if not attribDict else attribDict
        tabString = ''.join([char*indent for char in '\t'])
        finalString = ""
        
        for i,(k,v) in enumerate(attribDict.items()):
            if isinstance(v,dict):
                finalString += f"{tabString}{k}:\n{ self.format(v,indent+1) }\n"
            else:
                finalString += f"{tabString}{k}: {v}"
                finalString = finalString+"\n" if i<len(dict(attribDict.items()))-1 else finalString
        return finalString
    
    def build(self,dir="."):
        
        rawSetPath = Path(dir) / "set"
        setZipPath = Path(dir) / "set.zip"
        mseSetPath = Path(dir) / "set.mse-set"
        
        with open(rawSetPath,"w") as f:
            f.write(self.format())
        
        # compress formatted set file to zip
        with ZipFile(setZipPath,mode='w') as zip:
            zip.write(str(rawSetPath),"set")
        
        if isfile(mseSetPath):
            remove(mseSetPath)
        
        # give the file the 'mse-set' extension
        rename(setZipPath, mseSetPath)
        remove(rawSetPath)

# isSymbolString indicates whether t contains symbols
# as opposed to t being the symbol itself
def SYM(t,isSymbolString=False):
    if not isSymbolString:
        return f"<sym>{t}</sym>"
    return str(t).replace("[[","<sym>").replace("]]","</sym>")