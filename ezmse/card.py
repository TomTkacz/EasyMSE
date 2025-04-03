from .config import mseConfig,packageRootDirectory
from .utils import StringTemplate
from .set import SetConfiguration,SYM,DEFAULT_STYLE
from .error import *

from os import mkdir
from os.path import isfile
from pathlib import Path
from subprocess import Popen,DEVNULL
from shutil import rmtree

DEFAULT_IMAGEPATH = packageRootDirectory/"include"/"default_image.png"

# configures and exports cards
class Card:
    
    __CARD_WRITE_COMMAND = StringTemplate(
        """:load |
            import_image(\"|\")
            my_card := new_card(|)
            write_image_file(my_card, file: \"|\")
        """
    )

    def __getitem__(self,key):
        if key in self.__dict__['_Card_overwrittenFields'].keys():
            return self.__dict__['_Card_overwrittenFields'][key]
        if key in self.__dict__['_Card__formattedFields'].keys():
            return self.__dict__['_Card__formattedFields'][key]
        return None

    def __setitem__(self,key,value):
        self.__dict__['_Card__overwrittenFields'][key] = value
        
    
    def __init__(self,style=DEFAULT_STYLE):

        self.name = "[name]"
        self.text = "[text]"
        self.superType = "[superType]"
        self.type = "[type]"
        self.subType = "[subType]"
        self.castingCost = "RGB"
        self.power = 0
        self.toughness = 0
        self.rarity = "Common"
        self.colors = "Green"
        self.illustrator = "[illustrator]"
        self.setCode = "XXX"
        self.flavorText = ""
        self.imagePath = DEFAULT_IMAGEPATH.resolve().as_posix() # should always be a string, not Path

        try:
            self.setConfig = SetConfiguration(style)
        except Exception as e:
            print(f"{str(e)} Proceeding with default styling ({DEFAULT_STYLE}).")
            self.setConfig = SetConfiguration()
        
        self.__formattedFields = {}

        # holds user-specified fields to be directly written to the final 'new_card' params string
        # can be accessed by subscripting the card object
        # e.g. card['name'] = "some name" (overwrites the value of card.name)
        self.__overwrittenFields = {} 

    # formats card fields for parsing/displaying
    def __formatFields(self):
        
        self.__formattedFields['name'] = f"{self.name}"
        self.__formattedFields['text'] = rf"{SYM(self.text,True)}\n<i-flavor>{self.flavorText}</i-flavor>"
        self.__formattedFields['type'] = f"{self.superType} {self.type} - {self.subType}"
        self.__formattedFields['super_type'] = f"{self.superType}"
        self.__formattedFields['casting_cost'] = f"{self.castingCost}"
        self.__formattedFields['pt'] = f"{self.power}/{self.toughness}"
        self.__formattedFields['card_color'] = f"{ ','.join([color.lower() for color in self.colors]) if isinstance(self.colors,list) else self.colors.lower() }"
        self.__formattedFields['rarity'] = f"{self.rarity.lower()}"
        self.__formattedFields['illustrator'] = f"{self.illustrator}"
        self.__formattedFields['set_code'] = f"{self.setCode}"
        self.__formattedFields['image'] = Path(self.imagePath).stem

        # overwrite custom fields
        for k,v in self.__overwrittenFields.items():
            self.__formattedFields[k] = v

        # surround all values with double quotes
        for k,v in self.__formattedFields.items():
            self.__formattedFields[k] = f"\"{v}\""
        
    # creates a string of parameters that MSE's "new_card" command recognizes 
    def __generateNewCardParamsString(self):
        formattedParams = [f"{fieldName}: {value}" for fieldName, value in self.__formattedFields.items()]
        return "[" + ", ".join(formattedParams) + "]"

    def __assertValidImage(self,imagePath):
        fullPathString = Path(imagePath).resolve().as_posix()
        if not isfile(imagePath):
            raise FileNotFoundError(f"The file '{fullPathString}' could not be found.")
        if not ( imagePath.endswith(".jpg") or imagePath.endswith(".png") ):
            raise ImageTypeNotSupportedError(f"Failed to load '{fullPathString}'. Only PNG and JPG image types are supported.")

    # exports the card to an image file
    def export(self,fileName="card.jpg",generateLog=False):

        try:
            self.__assertValidImage(self.imagePath)
        except Exception as e:
            print(f"{e} Proceeding with default image.")
            self.imagePath = DEFAULT_IMAGEPATH.resolve().as_posix()

        self.__formatFields()
        paramsString = self.__generateNewCardParamsString()
        
        mseFolderPath = Path(mseConfig['file-locations']['mse-folder'])
        setPath = Path(mseConfig['file-locations']['mse-set'])

        tempDirectory = Path(mseFolderPath/"temp")
        imagePath = Path(self.imagePath).resolve().as_posix() # in case user enters relative path

        try:
            mkdir(tempDirectory)
        except:
            pass
        
        if not isfile(setPath) or not str(setPath).endswith(".mse-set"):
            self.setConfig.build(tempDirectory)
            setPath = tempDirectory/"set.mse-set"
        
        # write MSE commands to temp/ezmse-in.txt, using it as stdin for MSE's CLI
        with open(tempDirectory / 'ezmse-in.txt','w',encoding="utf8") as f:
            f.writelines(iter( self.__CARD_WRITE_COMMAND(setPath,imagePath,paramsString,fileName) ))
        with open(tempDirectory / 'ezmse-in.txt','r') as f:

            log = None
            if generateLog:
                log = open(mseFolderPath / "log.txt", 'w')

            with Popen([str(mseFolderPath / 'magicseteditor.com'),'--cli'],stdin=f,stdout = log if log else DEVNULL):
                pass

            if log:
                log.close()
        
        rmtree(tempDirectory)