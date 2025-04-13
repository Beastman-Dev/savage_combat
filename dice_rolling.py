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