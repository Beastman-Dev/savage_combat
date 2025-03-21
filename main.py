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
    # Returns the result of the roll
    def roll_die(self, sides: int, exploding: bool = True) -> int:
        roll = random.randint(1, sides)
        print(f"  You rolled a {roll}")
        if exploding == True and roll == sides:
            print("The die exploded! Rolling again...")
            roll += self.roll_die(sides, True)
        return roll

    # Function to roll multiple dice, add them together, and return the total
    # Takes in the number of dice and the number of sides
    # Returns the sum total of the dice rolls
    def roll_dice(self, count: int, sides: int) -> int:
        total = 0
        for i in range(count):
            total += self.roll_die(sides)
        return total

    # Function to roll a trait die and a wild die, compare the results, and return the higher of the two
    # Takes in the number of sides on the die
    # Returns the higher of the two rolls
    def roll_wild(self, sides: int) -> int:
        print("\nRolling the trait die...")
        result = self.roll_die(sides)
        print("\nRolling the wild die...")
        wild = self.roll_die(6)
        if wild > result:
            print("\nThe wild roll was better.")
            return wild
        print("\nThe trait roll was better.")
        return result

    # Function to call for resolving attack rolls
    # Takes in the target, attack type, and an optional parameter for adjacency which defaults to False
    # Returns the result of the attack roll: 0 for failure, 1 for success, and 2 for raise
    def attack_roll(self, target, attack_type: str, adjacent: bool = False) -> int:
        if attack_type == "melee":
            result = self.roll_wild(self.fighting) - target.parry
        elif attack_type == "throwing":
            result = self.roll_wild(self.athletics) - 4
        elif attack_type == "ranged":
            if adjacent:
                result = self.roll_wild(self.shooting) - target.parry
            else:
                result = self.roll_wild(self.shooting) - 4
        else:
            raise ValueError("Invalid attack type. Use 'melee', 'throwing', or 'ranged'")
        if result < 0:
            return 0
        elif result < 4:
            return 1
        else:
            return 2

    # Function to call for all damage rolls which automatically adds Strength for melee attacks
    # Takes in attack_type, dice_count, dice_sides, and an optional modifier which defaults to 0
    # Returns the total damage dealt
    def damage_roll(self, attack_type: str, dice_count: int, dice_sides: int, modifier: int = 0) -> int:
        
        total_damage = self.roll_dice(dice_count, dice_sides)
        if attack_type == "melee":
            total_damage += self.roll_die(self.strength, True)
        total_damage += modifier
        return total_damage

    # Function to call for initiating an attack and resolving the results
    # Takes in the target, attack_type, and any additional parameters
    # Returns the damage value modified by armor and armor piercing
    def attack(self, target, attack_method: str, adjacent: bool = False) -> str:
        attack_type = self.attacks[attack_method][0]
        damage = self.attacks[attack_method][1]
        # Reduce target's armor value by the armor piercing value of the attack
        armor_value = target.armor_value - self.attacks[attack_method][2]
        if armor_value < 0:
            armor_value = 0
        # Resolve the attack roll - result is 0 for failure, 1 for success, and 2 for raise
        attack_result = self.attack_roll(target, attack_type, adjacent)
        # If result is 0, return "Miss"
        if attack_result == 0:
            return "Miss"
        # Calculate the damage dealt
        damage_dealt = self.damage_roll(attack_type, damage[0], damage[1], damage[2])
        # Add 1d6 bonus damage if attack result was a raise
        if attack_result == 2:
            damage_dealt += self.roll_die(6)
        # Reduce damage by target's armor value, after ap is calcualted (above)
        damage_dealt -= armor_value
        # If damage is less than 0, set it to 0
        if damage_dealt < 0:
            damage_dealt = 0
        return damage_dealt

    def apply_damage(self, damage: int) -> str:
        wounds = math.floor((damage - self.toughness) / 4)
        self.wounds += wounds
        if self.wounds >= 4:
            self.status = "Incapacitated"
        elif wounds == 0 and self.status == "Shaken":
            self.wounds += 1
            if self.wounds >= 4:
                self.status = "Incapacitated"
        elif wounds >= 0:
            self.status = "Shaken"
        if self.wounds >=1 and self.status == "Uninjured":
            self.status = "Wounded"
        return self.status

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

    def create_combat(self):
        combat = Combat(self.player, self.opponent)
        return combat

#creature = Creature(name, spirit, strength, vigor, athletics, fighting, shooting, armor)
player_fighter: Creature = Creature("Player Fighter", 6, 6, 6, 6, 6, 6, 2)
goblin_grunt: Creature = Creature("Goblin Grunt", 6, 4, 6, 6, 6, 8)
goblin_grunt.add_attack("Short Spear", "melee", (1, 4, 0), 0)
goblin_grunt.add_attack("Short Bow", "ranged", (2, 6, 0), 0)
player_fighter.add_attack("Long Sword", "melee", (2, 6, 0), 0)

print(player_fighter.roll_wild(player_fighter.fighting))

# print(f"Player attacks goblin: {player_fighter.attack_roll(goblin_grunt, "melee")}!")
# print(f"Player damages goblin: {player_fighter.damage_roll("melee", 1, 8)}!")
# print(f"Goblin attacks player: {goblin_grunt.attack_roll(player_fighter, 'melee')}!")
# print(f"Goblin damages player: {goblin_grunt.damage_roll("melee", 1, 4)}!")
# print(f"Goblin status: {goblin_grunt.status}!")
# print(f"Player status: {player_fighter.status}!")
# print(f"Goblin wounds: {goblin_grunt.wounds}!")
# print(f"Player wounds: {player_fighter.wounds}!")

# for i in range(10):
#     print(f"Rolling a d4: {Die(4).roll_die()}")

# game = Game()
# game.player_inputs()
# game.opponent_inputs()
# combat = game.create_combat()
# print(combat.player.name)
# print(combat.opponent.name)

# Step 1: Initialize game and collect player inputs
# Step 2: Display current values and prompt to start combat loop
# Step 3: Initiate combat loop and prompt for opponent data
# Step 4: Select player attack or player defense
# Step 5: Prompt for type of attack and any relevant parameters
# Step 6: Print attack resolution step-by-step
# Step 7: Return to Step 4