import os
import sys

VERSION = 1

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


@staticmethod
def time_convert_regular(sec):
    "Returns: {0} Hours {1} Minutes {2} Seconds"
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    ts = "{0} Hours {1} Minutes {2} Seconds".format(int(hours),int(mins), int(sec))
    return ts

@staticmethod
def time_convert_short(sec):
    "Returns: {0}H {1}M {2}S"
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    ts = "{0}H {1}M {2}S".format(int(hours),int(mins), int(sec))
    return ts   

@staticmethod
def time_convert_small(sec):
    "Returns: {0}:{1}:{2}s"
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    ts = "{0}:{1}:{2}".format(int(hours),int(mins), int(sec))
    return ts

@staticmethod
def time_convert_hour(sec):
    "Returns: {Only Hours in int}"
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return int(hours)