from pathlib import Path
import zipfile

class PackageHandler():
    def __init__(self):
        self.path = Path("C:/Users/antom/OneDrive/Desktop/ezmse/ezmse/include/set.mse-set")
        # self.path = Path(packagePath) if type(packagePath) is str else packagePath
        
    def read(self,fileName):
        package = zipfile.ZipFile(str(self.path),'r')
        packageData = package.read(fileName)
        result = {}
        keyStack = []
        
        for line in bytes.decode(packageData,encoding="utf-8-sig").split('\n'):
            
            indent = line.count('\t')
            if indent == 0:
                currentDict = result
                keyStack = []
            else:
                d = result
                for k in keyStack:
                    child = d.get(k)
                    if type(child) is dict:
                        d = d.get(k)
                    else:
                        break
                currentDict = d
            
            lineStripped = line.strip()
            if lineStripped.startswith('#'):
                continue

            keyValueList = lineStripped.split(': ', 1)
            if len(keyValueList) == 1:
                key = keyValueList[0]
                value = None
            elif len(keyValueList) == 2:
                key,value = tuple(keyValueList)
                
            keyStack.append(key)
                            
            if not value:
                currentDict.setdefault(key,{})
            else:
                currentDict.setdefault(key,value)
                        
        return result