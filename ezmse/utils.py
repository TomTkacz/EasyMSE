class StringTemplate:
    
    __raw=""
    
    def __init__(self,inputString=""):
        
        self.__raw = inputString
    
    def __call__(self,*values):
        
        outputString=""
        splitString = self.__raw.split("|")
        startsWithBar = self.__raw[0]=="|"

        if startsWithBar:
            for i in range( len(splitString) ):
                try:
                    outputString += str(values[i])
                except:
                    pass
                try:
                    outputString += splitString[i+1]
                except:
                    pass
        else:
            for i,s in enumerate(splitString):
                outputString += s
                try:
                    outputString += str(values[i])
                except:
                    pass
        
        return outputString
    
    def raw(self):
        return self.raw
