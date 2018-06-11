import os
import sys
import psutil  # depends on python-psutil


def is_running():

    for q in psutil.process_iter():
        if q.name() == 'python':
            if len(q.cmdline()) > 1 and 'hud.py' in q.cmdline()[1]:
                return True

    return False


if len(sys.argv) >= 3:
    command = "python hud.py " + sys.argv[1] + " " + sys.argv[2]
else:
    command = "python hud.py"

if not is_running():
    # print("Script not running, launching...")
    os.system(command)
else:
    # print("Script already running, restarting...")
    os.system("pkill -9 -f \'python hud.py\'")
    os.system(command)

