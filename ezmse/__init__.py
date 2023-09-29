from . import file,config

from os import remove,getcwd
from subprocess import Popen
from shutil import copy
import PIL

cfg = config.config

class Card:
    
    __fieldNames = ['name','text','type','super_type','casting_cost','pt','card_color','rarity','illustrator','set_code']
        
    def __init__(self,name="[name]",text="[text]",type="[type]",superType="[superType]",castingCost=1,power=1,toughness=1,rarity="Common",color="Blue",illustrator="[illustrator]",setCode="[setCode]"):
        
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
        
    def export(self,fileName="card.jpg"):
        
        self.__formatFields()
        formatted_items = [f"{key}: {value}" for key, value in self.__formattedFields.items()]
        paramString = "[" + ", ".join(formatted_items) + "]"
        cardWriteCommand = f":load set.mse-set\nmy_card := new_card({paramString})\nwrite_image_file(my_card, file: \"{fileName}\")"
        
        copy( config.rootDirectory / 'include' / 'set.mse-set', getcwd() )
        
        with open("ezmse-in.txt","w") as f:
            f.writelines(iter(cardWriteCommand))
            
        with open("ezmse-in.txt","r") as f:
            with Popen(["magicseteditor.com","--cli"],stdin=f):
                pass
        
        sh = file.SetHandler(cfg["file-locations"]["mse-set"])
        with open(sh.getStylePath() / 'style','r',encoding="utf-8-sig") as f:
            imageInfo = file.parse(f.read())['card style']['image']
            # handle image info...
                
        remove("ezmse-in.txt")
        remove("set.mse-set")