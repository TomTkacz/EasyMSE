from ezmse import Card
from pytest import fixture

@fixture()
def card():
    return Card()
    
def test_generateNewCardParamsString(card):
    card.name = "TestName"
    card.text = "TestText"
    paramsString = card._Card__generateNewCardParamsString()
    assert paramsString.find('name: "TestName"') and paramsString.find('text: "TestText"')
    
def test_checkImageValidity(card,fs):
    fs.create_file("myimage.jpg")
    card.image = "myimage.jpg"
    assert card._Card__checkImageValidity()
    
def test_checkImageValidity_subDirectory(card,fs):
    fs.create_file("src/myimage.jpg")
    card.image = "src/myimage.jpg"
    assert card._Card__checkImageValidity()