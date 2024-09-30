class StringTemplate:
    
    __raw=""
    
    def __init__(self,inputString=""):
        
        self.__raw = inputString
    
    # really messy, honestly probably only works for my specific problem
    def __call__(self,*values):
        
        outputString=""
        splitString = self.__raw.split("|")
        insertHere = splitString[0]=="|"
        insertTextIndex = 0
        insertValueIndex = 0
        
        while (insertValueIndex < len(values)-1):
            if insertHere:
                outputString += values[insertValueIndex]
                insertValueIndex += 1
            else:
                outputString += splitString[insertTextIndex]
                insertTextIndex += 2
            insertHere = not insertHere
        
        insertTextIndex -= 1
        for i in range(insertTextIndex,len(splitString),1):
            outputString += splitString[i]
            if i < len(values):
                outputString += values[i]
        
        return outputString
    
    def raw(self):
        return self.raw