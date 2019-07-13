import random
import time


def random_sleep(a=5, b=1):
    # Simulate time to compute
    time.sleep(random.randint(1, 5))
    # Return random output
    return random.randint(0, a + b)