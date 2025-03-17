# Unit tests

from main import *

def test_get_data():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    assert player.get_data() == ("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    opponent = Combatant("Opponent", 6, 6, 6, 6, 6, 2)
    assert opponent.get_data() == ("Opponent", 6, 6, 6, 6, 6, 2)

def test_roll_die():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    assert player.roll_die(6) in range(1, 7)