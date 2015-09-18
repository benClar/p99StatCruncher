import sys
from DPS_Exceptions import ReadException
from ACTION_TYPE import ACTION_TYPE
from Display import StatsCruncherApp
import time

target = "/Users/benjaminclarke/Applications/Wineskin/Project1999.app/Contents/Resources/drive_c/P99/Logs/eqlog_"


class Player_Info(object):

    def __init__(self):
        self.info = {'curr_Damage': 0, 'total_damage': 0, ACTION_TYPE.MELEE: 0, ACTION_TYPE.DOT: 0, 'time': Timer()}

    def DPS(self):
        return self.info['curr_Damage'] / self.info['time'].curr_time

    def add_damage(self, damage, act_type):
        self.info['curr_Damage'] += int(damage)
        self.info['total_damage'] += int(damage)

    @property
    def total_damage(self):
        return self.info['total_damage']

    def reset(self):
        self.info['time'].reset()
        self.info['curr_Damage'] = 0


class Timer(object):

    def __init__(self):
        self.start = time.time()

    def reset(self):
        self.start = time.time()

    @property
    def curr_time(self):
        return time.time() - self.start


class Group(object):

    def __init__(self, player):
        self._group = {'group_mem': {player: Player_Info()}, 'non_group_mem': {}}
        self.player = player

    @property
    def group_members(self):
        return self._group['group_mem']

    def in_group(self, name):
        if self.convert_self(name) in self.group_members:
            return True
        return False

    def convert_self(self, name):
        if name == 'You':
            return self.player
        return name

    def DPS(self, name):
        """Returns DPS of requested member"""
        assert name in self._group['group_mem']
        return self.grp_mem(name).DPS()

    def add_damage(self, name, act_type, damage, mem_type='group_mem'):
        self._group[mem_type][self.convert_self(name)].add_damage(damage, act_type)

    def grp_mem(self, name):
        return self._group['group_mem'][name]

    def add_member(self, mem_name, mem_type='group_mem'):
        self._group[mem_type][mem_name] = Player_Info()

    def remove_member(self, mem_name, mem_type='group_mem'):
        self._group[mem_type].pop(mem_name, 0)

    def percentage_damage(self, name):
        total = 0
        for member, details in self.group_members.items():
            total += details.total_damage

        if total > 0:
            return (self.grp_mem(name).total_damage / total) * 100
        return 100

    def reset(self, name):
        self.grp_mem(name).reset()


def val_args(args):
    l_args = len(args)
    if l_args > 2 or l_args < 2:
        raise ReadException(str(l_args) + " arguments Supplied")


def get_logs(args):
    """Returns generator to tail log file"""
    global target
    val_args(args)
    logfile = open(target + args[1] + "_project1999.txt", "r")
    logfile.seek(0, 2)
    return logfile


def run(args):
    StatsCruncherApp(args[1], Group(args[1]), get_logs(args)).run()

if __name__ == "__main__":
    run(sys.argv)
