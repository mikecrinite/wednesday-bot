import random
import logging

# Russian roulette
chamber = [False, False, False, False, False, False]
current_chamber = 0


def is_loaded():
    for c in chamber:
        if c:
            return c


def load():
    chamber_to_load = random.choice(range(0, 5, 1))
    chamber[chamber_to_load] = True


def reset():
    global chamber, current_chamber
    chamber = [False, False, False, False, False, False]
    current_chamber = 0


def pull_trigger():
    global current_chamber
    dead = chamber[current_chamber]
    if not dead:
        current_chamber = current_chamber + 1
    else:
        reset()
    return dead


# Set up Logger
rr_logger = logging.getLogger('wednesday.rr')
rr_logger.setLevel(logging.INFO)
load()
