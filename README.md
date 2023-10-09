# EasyMSE

EasyMSE is a Python package for creating Magic: The Gathering cards from the command line. It interfaces with a pre-installed executable of [Magic Set Editor 2](https://magicseteditor.boards.net/) and its built in CLI to make generating custom cards easier.

# Installation

With Python and PIP installed, open a terminal and enter `pip install ezmse`

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

Clone the repository with `$ git clone "https://github.com/TomTkacz/EasyMSE.git"`
Navigate to the root folder, open a terminal, and enter `$ pip install -e .[dev]`
