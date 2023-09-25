import PIL
from os import mkdir,remove,getcwd,listdir
from os.path import isfile,isdir
from subprocess import Popen
from pathlib import Path
from shutil import copy
from configparser import ConfigParser

rootDirectory = Path(__file__).parent.resolve()
config = ConfigParser()
config.read(rootDirectory / 'include' / 'config.ini')

def setMSEFolder(path):
    if type(path) is str:
        path = Path(path)
    if isdir(path/'data') and isdir(path/'resource') and isfile(path/'magicseteditor.com') and isfile(path/'magicseteditor.exe'):
        config['file-locations']['mse-folder'] = str(path)
        config['file-locations']['mse-exe'] = str(path / 'magicseteditor.exe')
        config['file-locations']['mse-com'] = str(path / 'magicseteditor.com')
        with open(rootDirectory / 'include' / 'config.ini', 'w') as f:
            config.write(f)
        config.read(rootDirectory / 'include' / 'config.ini')
    else:
        print("folder must contain the files 'magicseteditor.exe' 'magicseteditor.com' and the directories 'data' 'resource'")

if isfile(rootDirectory / 'include' / 'set.mse-set'):
    config['file-locations']['mse-set'] = str(rootDirectory / 'include' / 'set.mse-set')
    
if config['file-locations']['mse-folder'] == '':
    setMSEFolder(Path(getcwd()))
    
class Card:
    def __init__(self,name="[name]",rulesText="[rulesText]",type="[type]",superType="[superType]",castingCost=1,power=1,toughness=1,rarity="Common",color="Blue",illustrator="[illustrator]"):
        self.name = name
        self.rulesText = rulesText
        self.type = type
        self.superType = superType
        self.castingCost = castingCost
        self.power = power
        self.toughness = toughness
        self.rarity = rarity
        self.color = color
        self.illustrator = illustrator
        
    def export(self):
        cardWriteCommand = ''':load set.mse-set\nmy_card := new_card([name: "name", super_type: "Legendary", casting_cost: "3G", pt: "3/4", card_color: "blue"])\nwrite_image_file(my_card, file: "card.jpg")'''
        copy( rootDirectory / 'include' / 'set.mse-set', getcwd() )
        with open("ezmse-in.txt","w") as f:
            f.writelines(iter(cardWriteCommand))
        with open("ezmse-in.txt","r") as f:
            with Popen(["magicseteditor.com","--cli"],stdin=f) as process:
                pass
        remove("ezmse-in.txt")
        remove("set.mse-set")