import time
import sys
from DPS_Exceptions import ReadException
from ACTION_TYPE import ACTION_TYPE
from Display import StatsCruncherApp

target = "/Users/benjaminclarke/Applications/Wineskin/Project1999.app/Contents/Resources/drive_c/P99/Logs/eqlog_"


class Player_Info(object):

    def __init__(self):
        self.info = {'Damage': 0, ACTION_TYPE.MELEE: 0, ACTION_TYPE.DOT: 0}

    def DPS(self, time):
        return self.info['Damage'] / time

    def add_damage(self, damage, act_type):
        self.info['Damage'] += int(damage)


class Timer(object):

    def __init__(self):
        self.time = 0

    def reset(self):
        self.time = 0


class Group(object):

    def __init__(self):
        self.group = {'group_mem': {'self': Player_Info()}, 'non_group_mem': {}, 'time': Timer()}

    def in_group(self, name):
        if name in self.group['group_mem']:
            return True
        return False

    def convert_self(self, name):
        if name == 'You':
            return 'self'
        return name

    def add_damage(self, name, act_type, damage, mem_type='group_mem'):
        self.info[mem_type][self.convert_self(name)].add_damage(damage, act_type)

    def grp_mem(self, name):
        return self.group['group_mem'][name]

    def add_member(self, mem_name, mem_type='group_mem'):
        self.group[mem_type][mem_name] = Player_Info()

    def remove_member(self, mem_name, mem_type='group_mem'):
        self.group[mem_type].pop(mem_name, 0)


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
    StatsCruncherApp(Group(), get_logs(args)).run()

if __name__ == "__main__":
    run(sys.argv)
