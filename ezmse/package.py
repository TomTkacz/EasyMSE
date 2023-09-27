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
        plainText = False
        scriptIndent = -1
        
        lines = bytes.decode(packageData,encoding="utf-8-sig").rstrip().split('\n')
        
        for line in lines:
            
            if line.strip() == '':
                continue
            
            lineStripped = line.strip()
            if lineStripped.startswith('#'):
                continue
                        
            indent = line.count('\t')
            if indent == lastIndent and len(keyStack)>0 and not plainText:
                keyStack.pop()
            
            if indent <= scriptIndent:
                plainText = False
                scriptIndent = -1
            
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

            if not plainText:
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
            else:
                try:
                    currentDict['code'].append(lineStripped)
                except:
                    currentDict.setdefault('code',[lineStripped])
                    
            if 'script:' in line and not plainText:
                plainText = True
                scriptIndent = indent

            lastIndent = indent
                        
        return result