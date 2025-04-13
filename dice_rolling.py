import random

# Function to roll a die with a specified number of sides and an optional exploding parameter
# Takes in the number of sides and a boolean for exploding option, which defaults to True
# Returns the result of the roll as a list (in case of an explosion)
def roll_die(sides: int, exploding: bool = True) -> list:
    rolls = []
    roll = random.randint(1, sides)
    rolls.append(roll)
    if exploding == True:
        while roll == sides:
            roll = random.randint(1, sides)
            rolls.append(roll)
    return rolls

# Function to roll a trait die and a wild die, returning both rolls
# Takes in the number of sides on the trait die
# Returns each roll as a list to account for explosions
def roll_wild(sides: int) -> list:
    trait_roll = roll_die(sides)
    wild_roll = roll_die(6)
    return trait_roll, wild_roll

# Function to roll multiple dice with a specified number of sides and an optional exploding parameter
# Takes in the number of dice, the number of sides, and a boolean for exploding option, which defaults to True
# Returns the result of all rolls, including any explosions, as a list
def roll_dice(count: int, sides: int, exploding: bool = True) -> list:
    rolls = []
    for i in range(count):
        roll = roll_die(sides, exploding)
        for item in roll:
            rolls.append(item)
    return rolls

