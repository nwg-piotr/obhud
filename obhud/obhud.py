import sys
import subprocess


def main():
    """
    For simplicity it'll be good to always use commands like `obhud --arg1 arg2`, but we want the timer to run
    independently.
    """
    if len(sys.argv) >= 3:
        if sys.argv[1] != "--timer":

            # Possibly we're just seeing the battery low alert, and the system is about to suspend.
            # Let's kill the task on AC connected.
            if sys.argv[1] == "--ac" and sys.argv[2] == "connected":
                subprocess.call(["pkill", "-9", "-f", "python hud.py"])

            subprocess.call(["python", "hud.py", sys.argv[1], sys.argv[2]])

        else:
            subprocess.call(["pkill", "-9", "-f", "python timer.py"])
            #subprocess.Popen(["nohup", "python", "timer.py", sys.argv[2]], stdout=open('/dev/null', 'w'))
            subprocess.call(["python", "timer.py", sys.argv[2]])
    else:
        subprocess.call(["python", "hud.py"])


if __name__ == "__main__":
    main()
