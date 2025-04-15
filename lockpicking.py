from dice_rolling import roll_die, roll_wild, roll_dice
import time
import os

# Picking a lock requires a number of successes on the appropriate skill (Thievery) equal to the difficulty of the lock
# The lockpicking skill is a trait skill, so it uses the wild die
# If the number of failed rolls is greater than the number of successes, progress is reset to 0
# If a critical failure is rolled, the lock is jammed and cannot be picked
# A critical failure happens when both the trait die and the wild die roll a 1

class Lock:
    def __init__(self, quality: int, complexity: int, difficulty: int) -> None:
        self.quality = quality
        self.complexity = complexity
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
        return "\n  !!! Critical failure: lock is jammed !!!\n"

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
        while total_roll >= self.quality:
            current_successes += 1
            total_roll -= self.quality
        self.successes += current_successes
        if self.successes >= self.complexity:
            self.locked = False
            return "The lock makes a satisfying click and unlocks.\n"
        else:
            return "You have made progress, but the lock remains closed."

    def picking_lock(self, skill: int) -> None:

        # Roll the skill die and the wild die
        trait_roll, wild_roll = roll_wild(skill)
        print(f"  Trait roll: {trait_roll} for a total of {sum(trait_roll)}")
        print(f"  Wild roll: {wild_roll} for a total of {sum(wild_roll)}")
        if trait_roll[0] == 1 and wild_roll[0] == 1:
            print(self.critical_failure())
            return
        elif sum(trait_roll) == sum(wild_roll):
            print("  Both rolls are equal, so I'm using that number as the result.")
            check_result = sum(trait_roll)
        elif sum(trait_roll) > sum(wild_roll):
            print("  Trait die roll is higher, so I'm using it as the result.")
            check_result = sum(trait_roll)
        else:
            print("  Wild die roll is higher, so I'm using it as the result.")
            check_result = sum(wild_roll)
        print("  ---------------")
        print(f"  Total Roll = {check_result}")
        print("===================================================================")
        input("Press Enter to continue...")

        # Present the outcome of the rolls
        os.system('cls' if os.name == 'nt' else 'clear')
        if check_result < self.quality:
            print(self.failure())
            return
        else:
            print(self.success(check_result))
            return

def round_title(rounds: int) -> str:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Attempt #{rounds}")
    print("===================================================================")

def page_footer() -> None:
    print("===================================================================")
    input("Press Enter to continue...")

def final_results():
    print("===================================================================")
    print("  Final Results")
    print("===================================================================")
    print(f"  Total successes: {lock.successes}")
    print(f"  Total failures: {lock.failures}")
    if lock.jammed:
        print("  The lock is jammed. You will need to find another way to proceed.")
    elif not lock.locked:
        print("  You have picked the lock and can proceed with your nefarious plans.")
    else:
        print("  The lock remains locked. You'll need to try again or find another way.\n")
    try_again = input("Would you like to try again? (y/n): ").strip().lower()
    if try_again == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting a new lockpicking attempt...")
        main()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Thank you for playing!")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Exiting the program...")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Goodbye!")

        exit()
    print("===================================================================")
    input("Press Enter to exit...")
    final_results()

def main():
    rounds = 0
    lock = Lock(quality=4, complexity = 2, difficulty=4)
    skill = 4  # Example skill level

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Lockpicking Simulation")
    print("===================================================================")
    print(f"  Lock Quality: {lock.quality} (The target number for skill checks.)")
    print(f"  Lock Complexity: {lock.complexity} (Number of successes needed to pick the lock.)")
    print(f"  Skill Level: {skill} (Your skill level for picking locks.)")
    print("===================================================================")
    input("Press Enter to start picking the lock...")
    print("\nStarting to pick the lock...\n")
    time.sleep(1)

    # Main loop for picking the lock
    while lock.locked and not lock.jammed:

        rounds += 1

        # Starting the round
        round_title(rounds)
        input("Press Enter to roll the dice...\n")

        print("   Rolling dice...\n")
        time.sleep(1)
        print("   Rolling dice..\n")
        time.sleep(1)
        print("   Rolling dice.\n")
        time.sleep(1)
        
        # Presenting the outcome of the round
        round_title(rounds)
        result = lock.picking_lock(skill)
        if lock.jammed:
            print("Lock is jammed. Cannot pick.")
            break
        if not lock.locked:
            print(f"Lock picked successfully in {rounds} rounds.")
            break
        page_footer()

        # End-of-round summary
        round_title(rounds)
        print(f"  Lock status: {lock.lock_status()}")
        print(f"  Current successes: {lock.successes}, Current failures: {lock.failures}")
        page_footer()
        print("Lock is still locked. Trying again...")
        print()


# Example usage
if __name__ == "__main__":
    main()


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