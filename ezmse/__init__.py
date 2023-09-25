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

if isfile(rootDirectory / 'include' / 'set.mse-set'):
    config['file-locations']['mse-set'] = str(rootDirectory)+'/include/set.mse-set'
    
if config['file-locations']['mse-folder'] == '':
    if isdir('data') and isdir('resource') and isfile('magicseteditor.com') and isfile('magicseteditor.exe'):
        config['file-locations']['mse-folder'] = getcwd()
        config['file-locations']['mse-exe'] = getcwd()+'/magicseteditor.exe'
        config['file-locations']['mse-com'] = getcwd()+'/magicseteditor.com'
    with open(rootDirectory / 'include' / 'config.ini', 'w') as f:
        config.write(f)
    config.read(rootDirectory / 'include' / 'config.ini')
    
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
        cardWriteCommand = ''':load set.mse-set\nmy_card := new_card([name: "name"])\nwrite_image_file(my_card, file: "card.jpg")'''
        copy( rootDirectory / 'include' / 'set.mse-set', getcwd() )
        with open("ezmse-in.txt","w") as f:
            f.writelines(iter(cardWriteCommand))
        with open("ezmse-in.txt","r") as f:
            with Popen(["magicseteditor.com","--cli"],stdin=f) as process:
                pass
        remove("ezmse-in.txt")
        remove("set.mse-set")