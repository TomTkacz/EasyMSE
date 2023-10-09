from . import config

from os import remove,rename,mkdir,chdir,remove
from os.path import isfile,isdir,basename
from pathlib import Path
from subprocess import Popen
from shutil import copy,rmtree

cfg = config.config

class Card:
    
    __fieldNames = ['name','text','type','super_type','casting_cost','pt','card_color','rarity','illustrator','set_code']
        
    def __init__(self,image=None,name="[name]",text="[text]",type="[type]",superType="[superType]",castingCost=1,power=1,toughness=1,rarity="Common",color="Blue",illustrator="[illustrator]",setCode="[setCode]"):
        
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
        
        self.__formattedFields = {}
        
        for fieldName in Card.__fieldNames:
            self.__formattedFields.setdefault(fieldName)
            
    def __formatFields(self):
        self.__formattedFields['name'] = f"\"{self.name}\""
        self.__formattedFields['text'] = f"\"{self.text}\""
        self.__formattedFields['type'] = f"\"{self.type}\""
        self.__formattedFields['super_type'] = f"\"{self.superType}\""
        self.__formattedFields['casting_cost'] = f"\"{self.castingCost}\""
        self.__formattedFields['pt'] = f"\"{self.power}/{self.toughness}\""
        self.__formattedFields['card_color'] = f"\"{self.color}\""
        self.__formattedFields['rarity'] = f"\"{self.rarity}\""
        self.__formattedFields['illustrator'] = f"\"{self.illustrator}\""
        self.__formattedFields['set_code'] = f"\"{self.setCode}\""
        
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

    def export(self,fileName="card.jpg"):
        
        self.__formatFields()
        paramsString = self.__generateNewCardParamsString()
        cardWriteCommand = f":load set.mse-set\nmy_card := new_card({paramsString})\nwrite_image_file(my_card, file: \"{fileName}\")"
        mseFolderPath = cfg['file-locations']['mse-folder']
        
        if isdir(mseFolderPath):
            
            mseFolderPath = Path(mseFolderPath)
            tempDirectory = Path(mseFolderPath / 'temp')
            isValidImage = self.__checkImageValidity()
            defaultImageScriptReplaced = False
            imagePath,imageName,imageFileExtension = self.__getImageInfo()

            mkdir(tempDirectory)
            copy( config.rootDirectory / 'include' / 'set.mse-set', mseFolderPath )
            
            if isfile(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts') and isValidImage:
                if isfile(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom.{imageFileExtension}'):
                    remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom.{imageFileExtension}')
                copy(imagePath, mseFolderPath / 'data' / 'magic-default-image.mse-include')
                chdir(mseFolderPath / 'data' / 'magic-default-image.mse-include')
                rename(mseFolderPath / 'data' / 'magic-default-image.mse-include' / imageName, f'custom.{imageFileExtension}')
                copy(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts', tempDirectory)
                remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts')
                copy(config.rootDirectory / 'include' / f'custom-image-script-{imageFileExtension}', mseFolderPath / 'data' / 'magic-default-image.mse-include')
                rename(mseFolderPath / 'data' / 'magic-default-image.mse-include' / f'custom-image-script-{imageFileExtension}', 'scripts')
                chdir(mseFolderPath)
                defaultImageScriptReplaced = True
                
        else:
            mseFolderPath = None
            
        if mseFolderPath:
            with open(tempDirectory / 'ezmse-in.txt','w') as f:
                f.writelines(iter(cardWriteCommand))

            with open(tempDirectory / 'ezmse-in.txt','r') as f:
                with Popen([str(mseFolderPath / 'magicseteditor.com'),'--cli'],stdin=f):
                    pass
            if defaultImageScriptReplaced:
                remove(mseFolderPath / 'data' / 'magic-default-image.mse-include' / 'scripts')
                copy(tempDirectory / 'scripts', mseFolderPath / 'data' / 'magic-default-image.mse-include')
                
            rmtree(tempDirectory)
            remove(mseFolderPath / 'set.mse-set')
        else:
            print("no path found to Magic Set Editor :(")