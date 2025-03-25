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
    results = enemy.roll_die(6)
    assert sum(results) > 0

def roll_wild():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    result, wild = enemy.roll_wild(6)
    assert sum(result) > 0
    assert type(wild) == bool

def roll_dice():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert sum(enemy.roll_dice(6, 2)) > 0

def attack_roll():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    result, wild = player.attack_roll(enemy, "melee")
    assert result in range(0,3)
    assert type(wild) == bool

def damage_roll():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    assert sum(player.damage_roll("melee", 1, 4)) > 0

def damage_calculation():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 0)
    attack_type = "melee"
    weapon_damage = (1, 4, 0)
    armor_piercing = 0
    assert player.damage_calculation(enemy, attack_type, weapon_damage, armor_piercing) >= 0

def apply_damage():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 0)
    assert player.apply_damage(enemy, 0) == "Uninjured"
    assert player.apply_damage(enemy, 5) == "Shaken"
    assert player.apply_damage(enemy, 9) == "Wounded"
    assert player.apply_damage(enemy, 21) == "Incapacitated"

def attack_resolution():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 0)
    assert player.attack_resolution(enemy, "unarmed") in ["Uninjured", "Shaken", "Wounded", "Incapacitated"]

if __name__ == "__main__":
    print("Testing player creation...")
    print(f"   Errors: {player_creation()}")
    print(f"Testing enemy creation...")
    print(f"   Errors: {enemy_creation()}")
    print(f"Testing add_attack...")
    print(f"   Errors: {add_attack()}")
    print(f"Testing roll_die...")
    print(f"   Errors: {roll_die()}")
    print(f"Testing roll_wild...")
    print(f"   Errors: {roll_wild()}")
    print(f"Testing roll_dice...")
    print(f"   Errors: {roll_dice()}")
    print(f"Testing attack_roll...")
    print(f"   Errors: {attack_roll()}")
    print(f"Testing damage_roll...")
    print(f"   Errors: {damage_roll()}")
    print(f"Testing damage_calculation...")
    print(f"   Errors: {damage_calculation()}")
    print(f"Testing apply_damage...")
    print(f"   Errors: {apply_damage()}")
    print(f"Testing attack_resolution...")
    print(f"   Errors: {attack_resolution()}")
    print("All tests passed!")
