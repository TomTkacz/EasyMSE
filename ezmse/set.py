import json
from pathlib import Path
from os import rename,remove
from os.path import dirname,isfile
from datetime import datetime
import zipfile

# gives the user more fine-grained control over a card's properties
# by allowing them to build a set file
class SetConfiguration:
    
    __attribs={}
    
    @classmethod
    def __jsonCustomAttribValuesHook(self,obj):
        
        def set(k,v):
            if k in list(obj.keys()):
                obj[k]=v
                
        currentTimeFormatted = str(datetime.today()).split(".")[0]
                
        set('time_created',currentTimeFormatted)
        set('time_modified',currentTimeFormatted)
        
        return obj
    
    # def __getattr__(self, name):
    #     try:
    #         return self.__attribs[name]
    #     except KeyError:
    #         return self.name
    
    # def __setattr__(self, name, value):
    #     try:
    #         self.__attribs[name] = value
    #     except KeyError:
    #         self.name = value
    
    def __str__(self):
        return str(self.__attribs)
    
    def __init__(self): 
        
        with open( Path(dirname(__file__))/"include"/"setconfigs"/"set.json","r") as f:
            
            self.__attribs = json.loads(
                f.read(),
                object_hook = SetConfiguration.__jsonCustomAttribValuesHook
            )
    
    # TODO: get rid of multiple newlines after nested dicts
    def format(self,attribDict=None,indent=0):
        attribDict = self.__attribs["Default"] if not attribDict else attribDict
        tabString = ''.join([char*indent for char in '\t'])
        finalString = ""
        for i,(k,v) in enumerate(attribDict.items()):
            if isinstance(v,dict):
                finalString += f"{tabString}{k}:\n{ self.format(v,indent+1) }\n"
            else:
                finalString += f"{tabString}{k}: {v}"
                finalString = finalString+"\n" if i<len(dict(attribDict.items()))-1 else finalString
        return finalString
    
    def printAttribs(self):
        print(self.__attribs)
    
    def build(self,dir="."):
        
        rawSetPath = Path(dir) / "set"
        setZipPath = Path(dir) / "set.zip"
        mseSetPath = Path(dir) / "set.mse-set"
        
        with open(rawSetPath,"w") as f:
            f.write(self.format())
        
        # compress formatted set fipe to zip
        zip = zipfile.ZipFile(setZipPath,mode='w')
        zip.write(str(rawSetPath),"set")
        zip.close()
        
        if isfile(mseSetPath):
            remove(mseSetPath)
        
        # give the file the 'mse-set' extension
        rename(setZipPath, mseSetPath)
        remove(rawSetPath)