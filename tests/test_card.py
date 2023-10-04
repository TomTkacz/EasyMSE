from ezmse import Card
from pytest import fixture

@fixture()
def card():
    return Card()

def test_init(card):
    assert card.name == "[name]"