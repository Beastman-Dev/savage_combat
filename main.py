# Combat manager for Savage Worlds

# Imports
from config import *
import re
import random
import math

# Classes

class Combatant:
    def __init__(self, name: str, spirit: int, vigor: int, athletics: int, fighting: int, shooting: int, armor_value: int) -> None:
        self.name = name
        self.spirit = spirit
        self.vigor = vigor
        self.athletics = athletics
        self.fighting = fighting
        self.shooting = shooting
        self.armor_value = armor_value
        self.parry = int(self.fighting) / 2 + 2
        self.toughness = int(self.vigor) / 2 + 2
        self.status = "Uninjured"
        self.wounds = 0
        self.attributes = {"spirit": self.spirit, "vigor": self.vigor}
        self.skills = {"athletics": self.athletics, "fighting": self.fighting, "shooting": self.shooting}
        self.defenses = {"parry": self.parry, "toughness": self.toughness, "armor": self.armor_value}

class Player(Combatant):
    def __init__(self, name: str, agility: int, smarts: int, spirit: int, strength: int, vigor: int, athletics: int, fighting: int, shooting: int, armor_value: int) -> None:
        super().__init__(name, spirit, vigor, athletics, fighting, shooting, armor_value)
        self.agility = agility
        self.smarts = smarts
        self.strength = strength
        self.attributes = {"agility": self.agility, "smarts": self.smarts, "spirit": self.spirit, "strength": self.strength, "vigor": self.vigor}


class Combat:
    def __init__(self, player: Player, opponent: Combatant) -> None:
        self.player = player
        self.opponent = opponent

    # Rolling die with explosions
    def roll_die(self, die_type: int) -> int:
        roll = random.randint(1, die_type)
        if roll == die_type:
            roll += self.roll_die(die_type)
        return roll

    def result_selection(self, trait_value: int) -> int:
        trait_roll = self.roll_die(trait_value)
        wild_die = self.roll_die(6)
        if wild_die > trait_roll:
            return wild_die
        else:
            return trait_roll

    def attack_values(self, attack_type: str, adjacent = False) -> tuple:
        if attack_type == "melee":
            attack_value = self.result_selection(self.player.skills["fighting"])
            defense_value = self.opponent.parry
        elif attack_type == "throwing":
            attack_value = self.result_selection(self.player.skills["athletics"])
            defense_value = 4
        elif attack_type == "ranged":
            attack_value = self.result_selection(self.player.skills["shooting"])
            if adjacent:
                defense_value = self.opponent.parry
            else:
                defense_value = 4
        else:
            raise ValueError("Invalid attack type. Use 'melee', 'throwing', or 'ranged'")
        return attack_value, defense_value

    def attack_resolution(self, attack_value: int, defense_value: int) -> int:
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
        self.opponent: Combatant = Combatant(name, spirit, vigor, athletics, fighting, shooting, armor)

    def create_combat(self):
        combat = Combat(self.player, self.opponent)
        return combat


def resolve_attack():
    attack_type = input("Enter the type of attack (melee, throwing, or ranged): ")
    if attack_type not in ["melee", "throwing", "ranged"]:
        print("Invalid attack type. Please enter 'melee', 'throwing', or 'ranged'.")
        resolve_attack()
    if attack_type == "ranged":
        adjacent = input("Is the opponent adjacent? (y/n): ")
        if adjacent == "y":
            adjacent = True
        else:
            adjacent = False
    attack_values = combat.attack_values(attack_type, adjacent)
    attack_value = attack_values[0]
    defense_value = attack_values[1]
    result = combat.attack_resolution(attack_value, defense_value)
    if result == 2:
        print("Attack hits with a raise!")
    elif result == 1:
        print("Attack hits!")
    else:
        print("Attack misses.")
    if result > 0:
        damage = input("Enter the damage dice notation (e.g. 2d6+2): ")
        total_damage = combat.calculate_damage(damage)
        print(f"Total damage: {total_damage}")
    return result

game = Game()
game.player_inputs()
game.opponent_inputs()
combat = game.create_combat()
print(combat.player.name)
print(combat.opponent.name)

# Step 1: Initialize game and collect player inputs
# Step 2: Display current values and prompt to start combat loop
# Step 3: Initiate combat loop and prompt for opponent data
# Step 4: Select player attack or player defense
# Step 5: Prompt for type of attack and any relevant parameters
# Step 6: Print attack resolution step-by-step
# Step 7: Return to Step 4