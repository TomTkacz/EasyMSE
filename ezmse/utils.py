class StringTemplate:
    
    __raw=""
    
    def __init__(self,inputString=""):
        
        self.__raw = inputString
    
    def __call__(self,*values):
        
        outputString=""
        splitString = self.__raw.split("|")
        insertHere = splitString[0]=="|"
        
        for i,v in enumerate(values):
            if insertHere:
                outputString += v
            else:
                outputString += splitString[i]
            insertHere = not insertHere
        
        return outputString
    
    def raw(self):
        return self.raw