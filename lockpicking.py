from dice_rolling import roll_die, roll_wild, roll_dice
import time
import os

# Picking a lock requires a number of successes on the appropriate skill (Thievery) equal to the difficulty of the lock
# The lockpicking skill is a trait skill, so it uses the wild die
# If the number of failed rolls is greater than the number of successes, progress is reset to 0
# If a critical failure is rolled, the lock is jammed and cannot be picked
# A critical failure happens when both the trait die and the wild die roll a 1

class Lock:
    def __init__(self, difficulty: int) -> None:
        self.difficulty = difficulty
        self.successes = 0
        self.failures = 0
        self.locked = True
        self.jammed = False

    def lock_status(self) -> str:
        if self.jammed:
            return "Jammed"
        elif self.locked:
            return "Locked"
        else:
            return "Unlocked"

    def critical_failure(self) -> str:
        self.jammed = True
        return "Critical failure: lock is jammed!"

    def failure(self) -> str:
        self.failures += 1
        if self.failures > self.successes and self.successes > 0:
            self.successes = 0
            self.failures = 0
            return "Something goes wrong, and you lose all progress."
        else:
            return "Failed attempt, no progress made"

    def success(self, total_roll) -> str:
        current_successes = 0
        while total_roll >= self.difficulty:
            current_successes += 1
            total_roll -= self.difficulty
        self.successes += current_successes
        if self.successes >= self.difficulty:
            self.locked = False
            return "The lock makes a satisfying click and unlocks."
        else:
            return "You have made progress, but the lock remains closed."

    def picking_lock(self, skill: int) -> None:

        # Roll the skill die and the wild die
        trait_roll, wild_roll = roll_wild(skill)
        if sum(trait_roll) > sum(wild_roll):
            check_result = sum(trait_roll)
        else:
            check_result = sum(wild_roll)
        print(f"Roll = {check_result}")
        input("Press Enter to continue...")

        # Check the outcome of the rolls
        if trait_roll[0] == 1 and wild_roll[0] == 1:
            print(self.critical_failure())
            return
        elif check_result < self.difficulty:
            print(self.failure())
            return
        else:
            print(self.success(check_result))
            return

# Example usage
if __name__ == "__main__":

    rounds = 0
    lock = Lock(difficulty=4)
    skill = 4  # Example skill level

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Lockpicking Simulation")
    print("Difficulty Level: ", lock.difficulty)
    print("Skill Level: ", skill)
    print("Press Enter to start picking the lock...")
    input()
    print("Starting lockpicking...")
    print()

    while lock.locked and not lock.jammed:
        os.system('cls' if os.name == 'nt' else 'clear')
        rounds += 1
        print(f"Attempt #{rounds}")
        input("Press Enter to roll the dice...")
        print("Rolling dice...")
        time.sleep(2)
        result = lock.picking_lock(skill)
        if lock.jammed:
            print("Lock is jammed. Cannot pick.")
            break
        if not lock.locked:
            print("Lock picked successfully!")
            break
        print("Lock status: ", lock.lock_status())
        print(f"Current successes: {lock.successes}, Current failures: {lock.failures}")
        input("Press Enter to continue...")
        print("Lock is still locked. Trying again...")
        print()


# The code simulates a lockpicking scenario where the player rolls dice to attempt to pick a lock.
# It includes checks for critical failures, successes, and the overall status of the lock.
# The lockpicking process continues until the lock is either picked successfully or jammed.
# The code is designed to be modular and can be integrated into a larger game system.
# The example usage at the end demonstrates how to create a lock and attempt to pick it using a specified skill level.
# The while loop continues until the lock is either picked successfully or jammed.
# The print statements provide feedback on the results of each attempt, including successes and failures.
# The code is structured to allow for easy modification and expansion, making it suitable for various game mechanics.
# The lockpicking process is encapsulated within the Lock class, which manages the state of the lock and the results of each attempt.
# The code is designed to be easily understandable and maintainable, with clear variable names and comments explaining each step.
# The use of functions for rolling dice allows for flexibility in the mechanics of the game, enabling the addition of new features or changes to existing ones.
# The code is written in Python and follows best practices for readability and organization.