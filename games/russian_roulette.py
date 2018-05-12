import random
import logging

# Set up Logger
rr_logger = logging.getLogger('wednesday.rr')
rr_logger.setLevel(logging.INFO)

alive_messages = ["Unfortunately, you survived. Who's next?",
                  "You lived!",
                  "Congratulations. You'll see another Wednesday"]
dead_messages = ['You died. Good riddance...',
                 'RIP in pepperoni',
                 'Clean yourself up. You dead.']


def get_alive_msg():
    return ' ---> ' + random.choice(alive_messages)


def get_dead_msg():
    return ' ---> ' + random.choice(dead_messages)


class RussianRoulette:
    def __init__(self):
        self.chamber = [False, False, False, False, False, False]
        self.current_chamber = 0

    def is_loaded(self):
        for c in self.chamber:
            if c:
                return c

    def load(self):
        chamber_to_load = random.choice(range(0, 5, 1))
        self.chamber[chamber_to_load] = True

    def reset(self):
        self.chamber = [False, False, False, False, False, False]
        self.current_chamber = 0

    def pull_trigger(self):
        dead = self.chamber[self.current_chamber]
        if not dead:
            self.current_chamber = self.current_chamber + 1
        else:
            self.reset()
        return dead
