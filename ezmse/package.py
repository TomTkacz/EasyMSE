from pathlib import Path
import zipfile

class PackageHandler():
    def __init__(self,packagePath):
        self.path = Path(packagePath) if type(packagePath) is str else packagePath
        
    def read(self,fileName):
        package = zipfile.ZipFile(str(self.path),'r')
        packageData = package.read(fileName)
        result = {}
        keyStack = []
        lastIndent = -1
        
        lines = bytes.decode(packageData,encoding="utf-8-sig").rstrip().split('\n')
        
        for line in lines:
            
            if line == '\n':
                continue
                        
            indent = line.count('\t')
            if indent == lastIndent:
                keyStack.pop()
                
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
                key = keyValueList[0][:-1]
                value = None
            elif len(keyValueList) == 2:
                key,value = tuple(keyValueList)
                
            keyStack.append(key)
                            
            if not value:
                currentDict.setdefault(key,{})
            else:
                currentDict.setdefault(key,value)

            lastIndent = indent
                        
        return result