# Combat manager for Savage Worlds

# Imports
from config import *
import os

class Player:
    def __init__(self, attributes: dict, skills: dict, armor_value: int) -> None:
        self.attributes = attributes
        self.skills = skills
        self.armor_value = armor_value

class Game:
    def __init__(self):
        pass

    def player_inputs(self):
        attributes = {}
        skills = {}
        print("Enter your Traits (attributes and skills):")
        print("Enter the number corresponding to the die type of each trait.")
        print("Example: to enter a d4, just type the number 4.")
        attributes("agility") = input ("What is your Agility attribute?: ")
        attributes("smarts") = input ("What is your Smarts attribute?: ")
        attributes("spirit") = input("What is your Spirit attribute?: ")
        attributes("strength") = input ("What is your Strength attribute?: ")
        attributes("vigor") = input("What is your Vigor attribute?: ")
        skills("athletics") = input("What is your Athletics skill?: ")
        skills("fighting") = input("What is your Fighting skill?: ")
        skills("shooting") = input("What is your Shooting skill?: ")
        armor_value = input("Enter your armor value (0 for none): ")
        self.player: Player = Player(attributes, skills, armor_value)

# Global variables
agility = 0
smarts = 1
spirit = 2
strength = 3
vigor = 4
athletics = 5
fighting = 6
shooting = 7
armor_value = 8
opponent_parry = 0
opponent_toughness = 1

# Calculated values
parry = fighting / 2 + 2
base_toughness = vigor / 2 + 2
total_toughness = base_toughness + armor_value

def test_player():
    agility = 10
    smarts = 6
    spirit = 8
    strength = 6
    vigor = 6
    athletics = 8
    fighting = 10
    shooting = 8
    armor_value = 2
    return agility, smarts, spirit, strength, vigor, athletics, fighting, shooting, armor_value

def player_inputs():
    print("Enter your Traits (attributes and skills):")
    print("Enter the number corresponding to the die type of each trait.")
    print("Example: to enter a d4, just type the number 4.")
    agility = input ("What is your Agility attribute?: ")
    smarts = input ("What is your Smarts attribute?: ")
    spirit = input("What is your Spirit attribute?: ")
    strength = input ("What is your Strength attribute?: ")
    vigor = input("What is your Vigor attribute?: ")
    athletics = input("What is your Athletics skill?: ")
    fighting = input("What is your Fighting skill?: ")
    shooting = input("What is your Shooting skill?: ")
    armor_value = input("Enter your armor value (0 for none): ")
    return agility, smarts, spirit, strength, vigor, athletics, fighting, shooting, armor_value

def opponent_inputs():
    print("For the following prompts, enter just the number.")
    print("Note: this is optional, so if you don't know just hit [Enter].")
    opponent_parry = input("What is your opponent's parry?: ")
    opponent_toughness = input("What is your opponent's toughness?: ")

def type_of_attack():
    print("What type of attack?:\n")
    print("   1. Melee\n   2. Throwing\n   3. Ranged\n")
    attack_type = input("Enter 1, 2, or 3: ")
    if attack_type == "1":
        melee_attack()
    elif attack_type == "2":
        throwing_attack()
    elif attack_type == "3":
        ranged_attack()
    else:
        print("Please enter 1, 2, or 3...")
        type_of_attack()

def melee_attack():
    defense_value = opponent_parry
    attack_value = fighting

def ranged_attack():
    adjacent = input("Is the target of your attack adjacent to you (Y/N)?: ")
    if adjacent == "Y":
        defense_value = opponent_parry
    elif adjacent == "N":
        defense_value = base_difficulty
    else:
        print("Please enter Y or N...")
        ranged_attack()

def throwing_attack():
    defense_value = base_difficulty
    attack_value = athletics



# Step 1: Take player inputs
player = test_player()
agility, smarts, spirit, strength, vigor, athletics, fighting, shooting, armor_value
print(f"Attributes: Agility: d{player[0]}, Smarts: d{player[1]}, Spirit: d{player[2]}, Strength: d{player[3]}, Vigor: d{player[4]}\nSkills: Athletics: d{player[5]}, Fighting: d{player[6]}, Shooting: d{player[7]}\nArmor: {player[8]}")
# Step 2: Display current values and prompt to start combat loop
# Step 3: Initiate combat loop and prompt for opponent data
# Step 4: Select player attack or player defense
# Step 5: Prompt for type of attack and any relevant parameters
# Step 6: Print attack resolution step-by-step
# Step 7: Return to Step 4