"""
Obhud - a script for handling laptop-specific keys and events in Openbox Window Manager

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
website: http://nwg.pl

Project: https://github.com/nwg-piotr/obhud

Obhud is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or any later version.

Obhud is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

import sys
import subprocess


def main():
    """
    For simplicity it'd be good to always use commands like `obhud --arg1 arg2`, but we want the timer to run
    independently.
    """
    if len(sys.argv) >= 3:
        if sys.argv[1] != "--timer":

            # Possibly we're just seeing the battery low alert, and the system is about to suspend.
            # Let's kill the task on AC connected.
            if sys.argv[1] == "--ac" and sys.argv[2] == "connected":
                subprocess.call(["pkill", "-9", "-f", "python hud.py"])

            subprocess.call(["python", "hud.py"] + sys.argv[1:])

        else:
            subprocess.call(["pkill", "-9", "-f", "python timer.py"])
            #subprocess.Popen(["nohup", "python", "timer.py", sys.argv[2]], stdout=open('/dev/null', 'w'))
            subprocess.call(["python", "timer.py", sys.argv[2]])
    else:
        subprocess.call(["python", "hud.py"])


if __name__ == "__main__":
    main()
