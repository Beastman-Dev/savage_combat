# Unit tests

from main import *

def test_get_data():
    player = Player({"agility": 10, "smarts": 6, "spirit": 8, "strength": 6, "vigor": 6}, {"athletics": 8, "fighting": 10, "shooting": 8}, 2)
    assert player.get_data() == ({"agility": 10, "smarts": 6, "spirit": 8, "strength": 6, "vigor": 6}, {"athletics": 8, "fighting": 10, "shooting": 8}, 2)
    opponent = Opponent(5, 5, 2)
    assert opponent.get_data() == (5, 5, 2)

def test_roll_die():
    player = Player({"agility": 10, "smarts": 6, "spirit": 8, "strength": 6, "vigor": 6}, {"athletics": 8, "fighting": 10, "shooting": 8}, 2)
    assert player.roll_die(6) in range(1, 7)