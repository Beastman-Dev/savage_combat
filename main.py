# Combat manager for Savage Worlds

# Imports
from config import *
import os
import random

class Player:
    def __init__(self, attributes: dict, skills: dict, armor_value: int) -> None:
        self.attributes = attributes
        self.skills = skills
        self.armor_value = armor_value
        self.parry = self.skills["fighting"] / 2 + 2
        self.base_toughness = self.attributes["vigor"] / 2 + 2
        self.total_toughness = self.base_toughness + self.armor_value

class Opponent:
    def __init__(self, parry: int, toughness: int, armor_value: int) -> None:
        self.parry = parry
        self.toughness = toughness
        self.armor_value = armor_value

class Combat:
    def __init__(self, player: Player, opponent: Opponent) -> None:
        self.player = player
        self.opponent = opponent

    def attack_values(self, attack_type: str, adjacent = False) -> tuple:
        if attack_type == "melee":
            self.attack_value = self.player.skills["fighting"]
            self.defense_value = self.opponent.parry
        elif attack_type == "throwing":
            self.attack_value = self.player.skills["athletics"]
            self.defense_value = 4
        elif attack_type == "ranged":
            self.attack_value = self.player.skills["shooting"]
            if adjacent:
                self.defense_value = self.opponent.parry
            else:
                self.defense_value = 4

    def attack(self, attack_value: int, defense_value: int) -> int:
        if attack_value >= defense_value + 4:
            return 2
        elif attack_value >= defense_value:
            return 1
        else:
            return 0



class Game:
    def __init__(self):
        pass

    # Rolling trait die and wild die with explosions
    def roll_die(self, die_type: int) -> tuple:
        roll = random.randint(1, die_type)
        if roll == die_type:
            roll += roll_die(die_type)
        wild = random.randint(1, 6)
        if wild == 6:
            wild += roll_die(6)
        return roll, wild

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

def test_combatants(self):
    self.player = Player({"agility": 10, "smarts": 6, "spirit": 8, "strength": 6, "vigor": 6}, {"athletics": 8, "fighting": 10, "shooting": 8}, 2)
    self.opponent = Opponent(5, 5, 2)

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

def opponent_inputs(self):
    print("For the following prompts, enter just the number.")
    print("Note: this is optional, so if you don't know just hit [Enter].")
    opponent_parry = input("What is your opponent's parry?: ")
    opponent_toughness = input("What is your opponent's toughness?: ")
    opponent_armor = input("What is your opponent's armor value?: ")
    self.opponent: Opponent = Opponent(opponent_parry, opponent_toughness, opponent_armor)



# Step 1: Initialize game and collect player inputs
# Step 2: Display current values and prompt to start combat loop
# Step 3: Initiate combat loop and prompt for opponent data
# Step 4: Select player attack or player defense
# Step 5: Prompt for type of attack and any relevant parameters
# Step 6: Print attack resolution step-by-step
# Step 7: Return to Step 4