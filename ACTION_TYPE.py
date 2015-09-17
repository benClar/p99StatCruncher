from enum import Enum


class ACTION_TYPE(Enum):

    MELEE = 0,
    DOT = 1

    def melee_attack_word(action):
        melee_actions = ['pierce', 'crush']
        if action in melee_actions:
            return ACTION_TYPE.MELEE
        return False
