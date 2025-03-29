from ezmse import Card
from pytest import fixture
from pyfakefs.fake_filesystem_unittest import Patcher

@fixture
def fs():
    with Patcher() as patcher:
        yield patcher.fs

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
    card.imagePath = "myimage.jpg"
    try:
        card._Card__assertValidImage(card.imagePath)
    except:
        assert False
    
def test_checkImageValidity_subDirectory(card,fs):
    fs.create_file("src/myimage.jpg")
    card.imagePath = "src/myimage.jpg"
    try:
        card._Card__assertValidImage(card.imagePath)
    except:
        assert False