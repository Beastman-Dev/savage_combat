# Combat manager for Savage Worlds

# Imports
from config import *

# Global variables
spirit = 0
vigor = 0
athletics = 0
fighting = 0
shooting = 0
armor_value = 0
opponent_parry = 0
opponent_toughness = 0

# Calculated values
parry = fighting / 2 + 2
base_toughness = vigor / 2 + 2
total_toughness = base_toughness + armor_value

def player_inputs():
    print("For the following prompts, enter the numer corresponding to the die type.")
    print("Example: to enter a d4, just type the number 4.")
    spirit = input("What is your Spirit attribute?: ")
    vigor = input("What is your Vigor attribute?: ")
    athletics = input("What is your Athletics skill?: ")
    fighting = input("What is your Fighting skill?: ")
    shooting = input("What is your Shooting skill?: ")
    armor_value = input("Enter your armor value (0 for none): ")

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
    elif attack_type == "2":
    elif attack_type == "3":    

    else:
        print("Please enter 1, 2, or 3...")
        define_attack()

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