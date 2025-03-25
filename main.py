# Combat manager for Savage Worlds

# Imports
from config import *
import re
import random
import math

# Classes

class Creature:
    def __init__(self, name: str, spirit: int, strength: int, vigor: int, athletics: int, fighting: int, shooting: int, armor_value: int = 0) -> None:
        self.name = name
        self.spirit = spirit
        self.strength = strength
        self.vigor = vigor
        self.athletics = athletics
        self.fighting = fighting
        self.shooting = shooting
        self.armor_value = armor_value
        self.parry = int(self.fighting) / 2 + 2
        self.toughness = int(self.vigor) / 2 + 2
        self.status = "Uninjured"
        self.wounds = 0
        self.attacks = {"unarmed": ("melee", (0,0,0), 0)}

    # Function for adding an attack to the dictionary of attacks for a specified creature
    def add_attack(self, attack_name: str, attack_type: str, damage: tuple, armor_piercing: int = 0) -> None:
        self.attacks[attack_name] = (attack_type, damage, armor_piercing)

    # Function to roll a die with a specified number of sides and an optional exploding parameter
    # Takes in the number of sides and a boolean for exploding option, which defaults to True
    # Returns the result of the roll as a list (in case of an explosion)
    def roll_die(self, sides: int, exploding: bool = True) -> list:
        rolls = []
        roll = random.randint(1, sides)
        rolls.append(roll)
        if exploding == True:
            while roll == sides:
                roll = random.randint(1, sides)
                rolls.append(roll)
        return rolls

    # Function to roll a trait die and a wild die, compare the results, and return the higher of the two
    # Takes in the number of sides on the die
    # Returns the higher of the two rolls as a list to account for explosions, and a boolean for the wild die
    def roll_wild(self, sides: int) -> list:
        trait_roll = self.roll_die(sides)
        wild_roll = self.roll_die(6)
        if sum(wild_roll) > sum(trait_roll):
            return wild_roll, True
        return trait_roll, False

    # Function to roll multiple dice with a specified number of sides and an optional exploding parameter
    # Takes in the number of dice, the number of sides, and a boolean for exploding option, which defaults to True
    # Returns the result of all rolls, including any explosions, as a list
    def roll_dice(self, count: int, sides: int, exploding: bool = True) -> list:
        rolls = []
        total = 0
        for i in range(count):
            roll = self.roll_die(sides, exploding)
            for item in roll:
                rolls.append(item)
        return rolls

    # Function to call for resolving attack rolls
    # Takes in the target, attack type, and an optional parameter for adjacency which defaults to False
    # Returns the result of the attack roll: 0 for failure, 1 for success, and 2 for raise; also returnds a boolean value for the wild die
    def attack_roll(self, target, attack_type: str, adjacent: bool = False) -> int:
        if attack_type == "melee":
            roll, wild = self.roll_wild(self.fighting)
            result = sum(roll) - target.parry
        elif attack_type == "throwing":
            roll, wild = self.roll_wild(self.athletics)
            result = sum(roll) - 4
        elif attack_type == "ranged":
            if adjacent:
                roll, wild = self.roll_wild(self.shooting)
                result = sum(roll) - target.parry
            else:
                roll, wild = self.roll_wild(self.shooting)
                result = sum(roll) - 4
        if result < 0:
            return 0, wild
        elif result < 4:
            return 1, wild
        else:
            return 2, wild

    # Function to call for all damage rolls which automatically adds Strength for melee attacks
    # Takes in attack_type, dice_count, dice_sides, and an optional modifier which defaults to 0
    # Returns the total damage dealt
    def damage_roll(self, attack_type: str, dice_count: int, dice_sides: int) -> list:        
        damage_roll = self.roll_dice(dice_count, dice_sides)
        if attack_type == "melee":
            strength_damage = self.roll_die(self.strength)
            for item in strength_damage:
                damage_roll.append(item)
        return damage_roll

    # Function to call for initiating an attack and resolving the results
    # Takes in the target, attack_type, weapon_damage, armor_piercing, and a boolean value for attack_raise which defaults to False
    # Returns the total damage dealt after all modifiers
    def damage_calculation(self, target, attack_type: str, weapon_damage: tuple, armor_piercing: int, attack_raise: bool = False) -> list:

        # Unpack the weapon damage tuple
        dice_count = weapon_damage[0]
        dice_sides = weapon_damage[1]
        modifier = weapon_damage[2]

        # Roll damage based on the weapon -> return list of damage dice rolls
        damage_roll = self.damage_roll(attack_type, dice_count, dice_sides)
        if attack_raise:
            bonus_damage = self.roll_die(6)
            for item in bonus_damage:
                damage_roll.append(item)

        # Reduce target's armor value by the armor piercing value of the attack
        armor_value = target.armor_value - armor_piercing
        if armor_value < 0:
            armor_value = 0

        # Calculate the total damage dealt
        damage_dealt = sum(damage_roll) + modifier - armor_value

        # If damage is less than 0, set it to 0
        if damage_dealt < 0:
            damage_dealt = 0

        return damage_roll, damage_dealt

    # Function to apply damage to a creature and update their status
    # Takes in target and the amount of damage dealt
    # Returns the updated status of the creature
    def apply_damage(self, target, damage: int) -> int:
        if damage < target.toughness:
            return -1
        wounds = math.floor((damage - target.toughness) / 4)
        target.wounds += wounds
        if target.wounds >= 4:
            target.status = "Incapacitated"
        elif wounds == 0 and target.status == "Shaken":
            target.wounds += 1
            target.status = "Wounded"
            if target.wounds >= 4:
                target.status = "Incapacitated"
        elif wounds > 0:
            target.status = "Wounded"
        elif wounds == 0 and target.status == "Uninjured":
            target.status = "Shaken"
        if target.wounds > 3:
            target.wounds = 3
        return wounds

    def attack_resolution(self, target, weapon, adjacent = False) -> str:
        attack_type = self.attacks[weapon][0]
        attack_damage = self.attacks[weapon][1]
        armor_piercing = self.attacks[weapon][2]
        attack_result = {}
        attack_raise = False

        # Attack roll -> Result
        # Takes target, attack type, and optional adjacency (defaults to False)
        attack_roll_result = self.attack_roll(target, attack_type, adjacent)
        if attack_roll_result[0] == 0: # If result is 0, return -1 for a "miss"
            attack_result["attack"] = "miss"
            return attack_result
        elif attack_roll_result[0] == 1:
            attack_result["attack"] = "hit"
        elif attack_roll_result[0] == 2:
            attack_result["attack"] = "hit with a raise"
            attack_raise = True
        else:
            raise ValueError("Invalid attack roll result")

        # Damage roll -> Damage
        # Takes in the target, attack_type, weapon_damage, armor_piercing, and a boolean value for attack_raise which defaults to False
        # Returns the total damage dealt after all modifiers
        damage_roll, damage_total = self.damage_calculation(target, attack_type, attack_damage, armor_piercing, attack_raise)
        attack_result["damage roll"] = damage_roll
        attack_result["damage total"] = damage_total

        # Damage effect -> Status
        # Takes in target and the amount of damage dealt
        # Returns the updated status of the creature
        damage_effect = self.apply_damage(target, damage_total)
        if damage_effect == -1:
            attack_result["damage_inflicted"] = "No damage"
        elif damage_effect == 0:
            attack_result["damage_inflicted"] = "Shaken"
        else:
            attack_result["damage_inflicted"] = "Wounded"
            attack_result["wounds_inflicted"] = damage_effect
        
        return attack_result


class Player(Creature):
    def __init__(self, name: str, agility: int, smarts: int, spirit: int, strength: int, vigor: int, athletics: int, fighting: int, shooting: int, armor_value: int) -> None:
        super().__init__(name, spirit, strength, vigor, athletics, fighting, shooting, armor_value)
        self.agility = agility
        self.smarts = smarts
        self.attributes = {"agility": self.agility, "smarts": self.smarts, "spirit": self.spirit, "strength": self.strength, "vigor": self.vigor}


class Game:
    def __init__(self):
        pass

    # Create player and opponent objects

    # Collect player inputs    
    def player_inputs(self):
        name = input("Enter your character's name: ")
        if not name:
            name = "Player"
        agility = input ("Agility: ")
        if not agility:
            agility = 6
        smarts = input ("Smarts: ")
        if not smarts:
            smarts = 6
        spirit = input("Spirit: ")
        if not spirit:
            spirit = 6
        strength = input ("Strength: ")
        if not strength:
            strength = 6
        vigor = input("Vigor: ")
        if not vigor:
            vigor = 6
        athletics = input("Athletics: ")
        if not athletics:
            athletics = 6
        fighting = input("Fighting: ")
        if not fighting:
            fighting = 6
        shooting = input("Shooting: ")
        if not shooting:
            shooting = 6
        armor_value = input("Armor Value: ")
        if not armor_value:
            armor_value = 0
        self.player: Player = Player(name, agility, smarts, spirit, strength, vigor, athletics, fighting, shooting, armor_value)

    # Collect opponent inputs (sets default values if none are provided)
    def opponent_inputs(self):
        name = input("Enter your opponent's name: ")
        if not name:
            name = "Opponent"
        spirit = input("Spirit: ")
        if not spirit:
            spirit = 6
        vigor = input("Vigor: ")
        if not vigor:
            vigor = 6
        athletics = input("Athletics: ")
        if not athletics:
            athletics = 6
        fighting = input("Fighting: ")
        if not fighting:
            fighting = 6
        shooting = input("Shooting: ")
        if not shooting:
            shooting = 6
        armor = input("Armor Value: ")
        self.opponent: Creature = Creature(name, spirit, vigor, athletics, fighting, shooting, armor)

    # Interprets attack resolution output and prints the results
    def print_results(self, attacker, defender, weapon, results: dict):
        print(f"{attacker.name} attacks {defender.name} with {weapon}...")
        print(f"Attack: {results['attack']}")
        if results["attack"] != "miss":
            print(f"Damage: {results['damage_inflicted']}")
            if results['damage_inflicted'] == "Wounded":
                print(f"Wounds Inflicted: {results['wounds_inflicted']}")
        print("\n")

# Functional testing

def test_player():
    player = Player("Player", 10, 6, 8, 6, 6, 8, 10, 8, 2)
    player.add_attack("long sword", "melee", (2, 6, 0), 0)
    return player

def test_enemy():
    enemy = Creature("enemy", 6, 6, 6, 6, 6, 6, 2)
    enemy.add_attack("short spear", "melee", (1, 4, 0), 0)
    enemy.add_attack("short bow", "ranged", (2, 6, 0), 0)
    return enemy

def test_attack(weapon: str = "long sword"):
    player = test_player()
    enemy = test_enemy()
    attack_results = player.attack_resolution(enemy, weapon)
    return player, enemy, attack_results

game = Game()
weapon = "long sword"
player, enemy, results = test_attack(weapon)
game.print_results(player, enemy, weapon, results)

# player, goblin = test_combatants()
# for i in range(10):
#     try:
#         print(player.attack_resolution(goblin, "Long Sword"))
#         print(goblin.status)
#     except Exception as e:
#         print(e)



'''
### Steps for Combat Manager ###
Step 1: Initialize game and collect player inputs
Step 2: Display current values and prompt to start combat loop
Step 3: Initiate combat loop and prompt for opponent data
Step 4: Select player attack or player defense
Step 5: Prompt for type of attack and any relevant parameters
Step 6: Print attack resolution step-by-step
Step 7: Return to Step 4
'''
