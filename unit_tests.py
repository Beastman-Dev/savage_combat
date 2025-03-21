# Unit tests

from main import *

def player_creation():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    assert (player.name, player.agility, player.smarts, player.spirit, player.strength, player.vigor, player.athletics, player.fighting, player.shooting, player.armor_value) == ("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)

def enemy_creation():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert (enemy.name, enemy.spirit, enemy.strength, enemy.vigor, enemy.athletics, enemy.fighting, enemy.shooting, enemy.armor_value) == ("enemy", 6, 6, 6, 6, 6, 6, 2)

def add_attack():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    enemy.add_attack("Short Spear", "melee", (1, 4, 0), 0)
    assert enemy.attacks["Short Spear"] == ("melee", (1, 4, 0), 0)

def roll_die():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert enemy.roll_die(6) > 0

def roll_dice():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert enemy.roll_dice(6, 2) > 0

def roll_wild():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert enemy.roll_wild(6) > 0

def attack_roll():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert player.attack_roll(enemy, "melee") in range(0,3)

def damage_roll():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert player.damage_roll("melee", 1, 4) > 0

def attack():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 0)
    assert player.attack(enemy, "unarmed") >= -1
    
def apply_damage():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 0)
    assert player.apply_damage(enemy, 5) == "Shaken"
    assert player.apply_damage(enemy, 9) == "Wounded"
    assert player.apply_damage(enemy, 21) == "Incapacitated"

if __name__ == "__main__":
    print("Testing player creation...")
    print(f"   Errors: {player_creation()}")
    print(f"Testing enemy creation...")
    print(f"   Errors: {enemy_creation()}")
    print(f"Testing add_attack...")
    print(f"   Errors: {add_attack()}")
    print(f"Testing roll_die...")
    print(f"   Errors: {roll_die()}")
    print(f"Testing roll_dice...")
    print(f"   Errors: {roll_dice()}")
    print(f"Testing roll_wild...")
    print(f"   Errors: {roll_wild()}")
    print(f"Testing attack_roll...")
    print(f"   Errors: {attack_roll()}")
    print(f"Testing damage_roll...")
    print(f"   Errors: {damage_roll()}")
    print(f"Testing attack...")
    print(f"   Errors: {attack()}")
    print(f"Testing apply_damage...")
    print(f"   Errors: {apply_damage()}")
    print("All tests passed!")
