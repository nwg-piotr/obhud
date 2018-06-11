import sys
import os
import values

from commands import volume, brightness, battery, ac, check_dimensions


def main():

    values.tmp = os.getenv("HOME") + "/tmp".rstrip()
    print(values.tmp)

    check_dimensions()

    if len(sys.argv) <= 2 or sys.argv[1] != "--volume" and sys.argv[1] != "--brightness" and sys.argv[
                1] != "--battery" and sys.argv[1] != "--ac":
        print("Usage:")
        print("--volume {up} | {down} | {toggle}")
        print("--brightness {up} | {down}")
        print("--battery {low} | {full}")
        print("--ac {connected} | {disconnected}")

        sys.exit(0)

    elif sys.argv[1] == "--volume":
        if sys.argv[2] == "up" or sys.argv[2] == "down" or sys.argv[2] == "toggle":
            volume(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")

    elif sys.argv[1] == "--brightness":
        if sys.argv[2] == "up" or sys.argv[2] == "down":
            brightness(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")

    elif sys.argv[1] == "--battery":
        if sys.argv[2] == "low" or sys.argv[2] == "full":
            battery(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")

    elif sys.argv[1] == "--ac":
        if sys.argv[2] == "connected" or sys.argv[2] == "disconnected":
            ac(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")


if __name__ == "__main__":
    main()