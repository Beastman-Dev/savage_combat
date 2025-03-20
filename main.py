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
        # self.attributes = {"spirit": self.spirit, "strength": self.strength, "vigor": self.vigor}
        # self.skills = {"athletics": self.athletics, "fighting": self.fighting, "shooting": self.shooting}
        # self.defenses = {"parry": self.parry, "toughness": self.toughness, "armor": self.armor_value}
        self.attacks = {"unarmed": ("melee", (0,0,0), 0)}

    # Function for adding an attack to the dictionary of attacks for a specified creature
    def add_attack(self, attack_name: str, attack_type: str, damage: tuple, armor_piercing: int = 0) -> None:
        self.attacks[attack_name] = (attack_type, damage, armor_piercing)

    # Function to call for all trait rolls, which always includes the wild die -> returns the highest of the two rolls
    def trait_roll(self, trait: int) -> int:
        return Die.roll_die(trait, True)

    # Function to call for attack rolls -> returns 0 for failure, 1 for success, and 2 for raise
    def attack_roll(self, target, attack_type: str, adjacent: bool = False) -> int:
        if attack_type == "melee":
            result = self.trait_roll(self.fighting) - target.parry
        elif attack_type == "throwing":
            result = self.trait_roll(self.athletics) - 4
        elif attack_type == "ranged":
            if adjacent:
                result = self.trait_roll(self.shooting) - target.parry
            else:
                result = self.trait_roll(self.shooting) - 4
        else:
            raise ValueError("Invalid attack type. Use 'melee', 'throwing', or 'ranged'")
        if result < 0:
            return 0
        elif result < 4:
            return 1
        else:
            return 2

    # Function to call for all damage rolls, which includes parameters for dice_count, dice_sides, and modifier as well as adding strength to melee attacks
    def damage_roll(self, attack_type: str, dice_count: int, dice_sides: int, modifier: int = 0) -> int:
        total_damage = 0
        for i in range(dice_count):
            total_damage += Die.roll_die(dice_sides)
        if attack_type == "melee":
            total_damage += self.trait_roll(self.strength)
        total_damage += modifier
        return total_damage

class Player(Creature):
    def __init__(self, name: str, agility: int, smarts: int, spirit: int, strength: int, vigor: int, athletics: int, fighting: int, shooting: int, armor_value: int) -> None:
        super().__init__(name, spirit, strength, vigor, athletics, fighting, shooting, armor_value)
        self.agility = agility
        self.smarts = smarts
        self.attributes = {"agility": self.agility, "smarts": self.smarts, "spirit": self.spirit, "strength": self.strength, "vigor": self.vigor}

class Die:
    def __init__(self, sides: int, wild_die: bool = False) -> int:
        self.sides = sides
        self.wild_die = wild_die
    
    def roll_die(self) -> int:
        roll = random.randint(1, self.sides)
        if roll == self.sides:
            roll += self.roll_die()
        if self.wild_die:
            wild_roll = random.randint(1, 6)
            if wild_roll > roll:
                roll = wild_roll
        return roll

class Combat:
    def __init__(self, player: Player, opponent: Creature) -> None:
        self.player = player
        self.opponent = opponent

    def attack_resolution(self, attack_type: str, adjacent = False) -> int:
        attack_values = self.attack_values(attack_type, adjacent)
        attack_value = attack_values[0]
        defense_value = attack_values[1]
        if attack_value >= defense_value + 4:
            return 2
        elif attack_value >= defense_value:
            return 1
        else:
            return 0

    def calculate_damage(self, dice_notation: str) -> int:
        # Use a regular expression to parse the dice notation
        pattern = r'(\d+)d(\d+)([+-]\d+)?'
        match = re.fullmatch(pattern, dice_notation.strip())

        if not match:
            raise ValueError("Invalid dice notation. Use format like '2d6+2'")

        # Extract the number of dice, the number of sides, and the modifier
        # Set the total starting value to the modifier (or 0 if no modifier)
        num_dice = int(match.group(1))
        sides = int(match.group(2))
        total = int(match.group(3)) if match.group(3) else 0

        # Roll the dice and add the modifier
        for i in range(num_dice):
            roll = self.roll_die(sides)
            total += roll
        return total

    def damage_effect(self, damage: int) -> str:
        wounds = math.floor((damage - self.opponent.toughness) / 4)
        self.opponent.wounds += wounds
        if self.opponent.wounds >= 4:
            self.opponent.status = "Incapacitated"
        elif wounds == 0 and self.opponent.status == "Shaken":
            self.opponent.wounds += 1
            if self.opponent.wounds >= 4:
                self.opponent.status = "Incapacitated"
        elif wounds >= 0:
            self.opponent.status = "Shaken"
        if self.opponent.wounds >=1 and self.opponent.status == "Uninjured":
            self.opponent.status = "Wounded"
        return self.opponent.status
        

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

goblin_grunt: Creature = Creature("Goblin Grunt", 6, 4, 6, 6, 6, 8)

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