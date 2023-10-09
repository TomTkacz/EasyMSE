# EasyMSE

EasyMSE is a Python package for creating Magic: The Gathering cards from the command line. It interfaces with an installation of Magic Set Editor 2 and its built in CLI to make generating custom cards easier.

# Installation

With Python and PIP installed, open a terminal and enter `pip install ezmse`

You must have [Magic Set Editor 2](https://magicseteditor.boards.net/page/downloads) installed. Your working directory must contain the .exe and .com versions of MSE as well as its data and resource folder. You must also have the [Magic - M15 fonts](https://github.com/MagicSetEditorPacks/Font-Pack) installed on your computer in order for the cards to render properly.

# Usage

## Generating a Card

```python
from ezmse import Card

myCard = Card()
myCard.name = "Cheese, The Destroyer"
myCard.color = "red,black"
myCard.castingCost = "2RB"
myCard.type = "Legendary Creature - Cat"
myCard.rarity = "Rare"
myCard.superType = "Legendary"
myCard.power = 5
myCard.toughness = 6
myCard.illustrator = "Kev Walker"
myCard.setCode = "XXX-XX"
myCard.text = r"Indestructible\n<sym>T</sym>: Draw one BILLION cards"
myCard.image = "cheese.jpg"

myCard.export("card.png")
```

![1696893501127](image/README/1696893501127.png)

# Developing EasyMSE

Open a terminal and clone the repository with `git clone "https://github.com/TomTkacz/EasyMSE.git"`

Navigate to the root folder and enter `pip install -e .[dev]`

Features that need added:

* A more genericized Card class that can generate other types of cards (Planeswalker, Saga, etc.)
* More unit tests! (I'm fairly new to them)
