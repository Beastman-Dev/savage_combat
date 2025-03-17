# Unit tests

from main import *

def player_creation():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    assert (player.name, player.agility, player.smarts, player.spirit, player.strength, player.vigor, player.athletics, player.fighting, player.shooting, player.armor_value) == ("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)

def opponent_creation():
    opponent = Combatant("Opponent", 6, 6, 6, 6, 6, 2)
    assert (opponent.name, opponent.spirit, opponent.vigor, opponent.athletics, opponent.fighting, opponent.shooting, opponent.armor_value) == ("Opponent", 6, 6, 6, 6, 6, 2)

def combat_creation():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    opponent = Combatant("Opponent", 6, 6, 6, 6, 6, 2)
    combat = Combat(player, opponent)
    assert (combat.player.name, combat.opponent.name) == ("Player", "Opponent")
    assert combat.roll_die(4) > 0
    assert combat.result_selection(6) > 0

if __name__ == "__main__":
    print("Testing player creation...")
    print(f"   Errors: {player_creation()}")
    print(f"Testing opponent creation...")
    print(f"   Errors: {opponent_creation()}")
    print(f"Testing combat creation...")
    print(f"   Errors: {combat_creation()}")
    print("All tests passed!")
