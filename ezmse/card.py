from .config import *
from .utils import StringTemplate
from .set import SetConfiguration

from os import remove,rename,mkdir,chdir,remove
from os.path import isfile,isdir,basename
from pathlib import Path
from subprocess import Popen,DEVNULL
from shutil import copy,rmtree

cfg = config

class Card:
    
    __CARD_WRITE_COMMAND = StringTemplate(
        """:load set.mse-set
            my_card := new_card(|)
            write_image_file(my_card, file: \"|\")
        """
    )
    
    __fieldNames = ['name','text','type','super_type','casting_cost','pt','card_color','rarity','illustrator','set_code']
        
    def __init__(self,image=None,name="[name]",text="[text]",type="[type]",superType="[superType]",
                 castingCost=1,power=1,toughness=1,rarity="Common",color="Blue",illustrator="[illustrator]",
                 setCode="[setCode]",config=None):
        
        self.name = name
        self.text = text
        self.type = type
        self.superType = superType
        self.castingCost = castingCost
        self.power = power
        self.toughness = toughness
        self.rarity = rarity
        self.color = color
        self.illustrator = illustrator
        self.setCode = setCode
        self.image = image
        self.config = config if config else SetConfiguration()
        
        self.__formattedFields = {}
        
        # initializes the keys of the __formattedFields dict to be the __fieldNames
        for fieldName in Card.__fieldNames:
            self.__formattedFields.setdefault(fieldName)
    
    # formats card fields for displaying
    def __formatFields(self):
        self.__formattedFields['name'] = f"\"{self.name}\""
        self.__formattedFields['text'] = f"\"{self.text}\""
        self.__formattedFields['type'] = f"\"{self.type}\""
        self.__formattedFields['super_type'] = f"\"{self.superType[0].upper()}{self.superType[1:]}\""
        self.__formattedFields['casting_cost'] = f"\"{self.castingCost}\""
        self.__formattedFields['pt'] = f"\"{self.power}/{self.toughness}\""
        self.__formattedFields['card_color'] = f"\"{self.color.lower()}\""
        self.__formattedFields['rarity'] = f"\"{self.rarity.lower()}\""
        self.__formattedFields['illustrator'] = f"\"{self.illustrator}\""
        self.__formattedFields['set_code'] = f"\"{self.setCode}\""
        
    # creates a string of card parameters that MSE's "new_card" command can recognize
    def __generateNewCardParamsString(self):
        formattedParams = [f"{fieldName}: {value}" for fieldName, value in self.__formattedFields.items()]
        return "[" + ", ".join(formattedParams) + "]"
    
    def __checkImageValidity(self):
        return self.image is not None and type(self.image) is str and isfile(self.image) and ( self.image.endswith(".jpg") or self.image.endswith(".png") )
    
    def __getImageInfo(self):
        imagePath = Path(self.image)
        imageName = basename(self.image)
        imageFileExtension = imageName[-3:]
        return (imagePath,imageName,imageFileExtension)

    # exports the card to an image file
    def export(self,fileName="card.jpg"):
        
        self.__formatFields()
        paramsString = self.__generateNewCardParamsString()
        mseFolderPath = cfg['file-locations']['mse-folder']
        
        if not isdir(mseFolderPath):
            raise FileNotFoundError("no path found to Magic Set Editor :(")
            
        mseFolderPath = Path(mseFolderPath)
        tempDirectory = Path(mseFolderPath / 'temp')
        isValidImage = self.__checkImageValidity()
        defaultImageScriptReplaced = False
        
        if not isfile( mseFolderPath / 'set.mse-set' ):
            self.config.build(mseFolderPath)
            setSetLocation( str(mseFolderPath / 'set.mse-set') )
        
        if str(mseFolderPath / 'set.mse-set') != cfg['file-locations']['mse-set']:
            copy( cfg['file-locations']['mse-set'], mseFolderPath )

        try:
            mkdir(tempDirectory)
        except:
            pass
        
        # copies either a built or default MSE set file into directory containing MSE folders
        # (needed for generating a card)
        if isfile(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts') and isValidImage:
            
            imagePath,imageName,imageFileExtension = self.__getImageInfo()
            
            # remove previous custom card image, if any
            if isfile(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom.{imageFileExtension}'):
                remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom.{imageFileExtension}')
            
            # copy custom image into the proper .mse-include folder and name it custom.[file extension]
            copy(imagePath, mseFolderPath / 'data' / 'magic-default-image.mse-include')
            chdir(mseFolderPath / 'data' / 'magic-default-image.mse-include')
            rename(mseFolderPath / 'data' / 'magic-default-image.mse-include' / imageName, f'custom.{imageFileExtension}')
            
            # copy existing MSE script in .mse-include folder into a temp folder
            # and have custom-image-script-[image file format] take its place
            copy(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts', tempDirectory)
            remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts')
            copy(packageRootDirectory / 'include' / f'custom-image-script-{imageFileExtension}', mseFolderPath / 'data' / 'magic-default-image.mse-include')
            rename(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom-image-script-{imageFileExtension}', 'scripts')
            chdir(mseFolderPath)
            
            defaultImageScriptReplaced = True
        
        else:
            raise FileNotFoundError("no *.mse-include/scripts file could be found.")
        
        # write MSE commands to ezmse-in.txt, using it as stdin for MSE's CLI
        with open(tempDirectory / 'ezmse-in.txt','w') as f:
            f.writelines(iter( self.__CARD_WRITE_COMMAND(paramsString,fileName) ))
        with open(tempDirectory / 'ezmse-in.txt','r') as f:
            with open(mseFolderPath / "out.txt", 'w') as log:
                with Popen([str(mseFolderPath / 'magicseteditor.com'),'--cli'],stdin=f,stdout=log):
                    pass
        
        # restore original script file and clean up
        if defaultImageScriptReplaced:
            remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts')
            copy(tempDirectory / 'scripts', mseFolderPath / 'data' / 'magic-default-image.mse-include')
            
        rmtree(tempDirectory)
        remove(mseFolderPath / 'set.mse-set')