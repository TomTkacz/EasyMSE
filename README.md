<div align="center">
    <img src="https://i.imgur.com/ldS8Akl.png">
    <img src="https://github.com/TomTkacz/EasyMSE/actions/workflows/unit-tests.yml/badge.svg">
    <img src="https://img.shields.io/pypi/v/ezmse?label=PyPI%20Version">
    <img src="https://img.shields.io/github/last-commit/TomTkacz/EasyMSE/main?label=Last%20Commit">
</div>
<br>

EasyMSE is a Python package for creating Magic: The Gathering cards from code or the command line. It interfaces with an installation of Magic Set Editor 2 and its built in CLI to make generating custom cards easier.

# Installation

With Python and PIP installed, open a terminal and enter `pip install ezmse`

You must have [MSE2](https://magicseteditor.boards.net/page/downloads) installed (or build it from [source](https://github.com/twanvl/MagicSetEditor2)). By default, MSE2 doesn't have the necessary features<sup>[[1]](https://github.com/haganbmj/MagicSetEditor2/pull/106)[[2]](https://github.com/haganbmj/MagicSetEditor2/pull/104)</sup> needed to use EasyMSE version >=v1.0.0. To enable this additional functionality, you must also download the EasyMSE build of MSE2 (see the following platform-specific sections).

### Windows

On x64 Windows, you can simply replace the MSE2 .exe and .com files with the [EasyMSE build binaries](https://github.com/TomTkacz/MagicSetEditor2/releases/tag/v2.5.6) of MSE2.

### MacOS & Linux

EasyMSE is currently <b>only supported on Windows</b>. The program specifically looks for .exe and .com extensions to the executables, which means a you'd need a modified environment for EasyMSE to work correctly. I hope to implement greater cross-platform support in the future.

# Setup

Your working directory must contain the .exe and .com versions of MSE as well as its data and resource folder. You must also have the [Magic - M15 fonts](https://github.com/MagicSetEditorPacks/Font-Pack) downloaded in order for the cards to render properly. You can either install the fonts system-wide or copy them to the `resource/fonts` folder in your working directory.

# Usage

## Generating a Card

```python
from ezmse import *

card = Card(style="m15-altered")

card.name = "Cheese, the Destroyer"
card.imagePath = "images/cheese.jpg"
card.colors = ["red","blue"]
card.castingCost = "2RU"

card.rarity = "Legendary"
card.type = "Creature"
card.subType = "Cat"

card.power = 12
card.toughness = 12

card.text = "[[T]]: Kill everyone and destroy the world."
card.flavorText = "Meowwww!!!"

card.setCode = "123"
card.illustrator = "Kev Walker"

card.export("test.png")
```

<div align="center">
    <img src="https://i.imgur.com/7E33gXl.png">
</div>
<br>

# Developing EasyMSE

Clone the repository, navigate to the root folder, and enter `pip install -e .[dev]`