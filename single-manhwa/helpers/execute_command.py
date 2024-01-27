import subprocess
from shlex import split
from collections import namedtuple
from functools import reduce

proc_output = namedtuple('proc_output', 'stdout stderr')


def pipeline(starter_command, *commands):
    if not commands:
        try:
            starter_command, *commands = starter_command.split('|')
        except AttributeError:
            pass
    starter_command = _parse(starter_command)
    starter = subprocess.Popen(starter_command, stdout=subprocess.PIPE)
    last_proc = reduce(_create_pipe, map(_parse, commands), starter)
    return proc_output(*last_proc.communicate())


def _create_pipe(previous, command):
    proc = subprocess.Popen(
        command, stdin=previous.stdout, stdout=subprocess.PIPE)
    previous.stdout.close()
    return proc


def _parse(cmd):
    try:
        return split(cmd)
    except Exception:
        return cmd
