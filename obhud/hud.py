import sys
import os
import values

from commands import volume, brightness, battery, ac, touchpad, check_dimensions, config_load, autoconfig_tint2, \
    autoconfig_keys, autoconfig_all, screens, load_preferences, create_preferences


def main():
    values.tmp = os.getenv("HOME") + "/tmp".rstrip()

    config_load()

    values.preferences_file = os.getenv("HOME") + "/.config/obhud/preferences.pkl"

    check_dimensions()

    if len(sys.argv) <= 2 or sys.argv[1] != "--volume" and sys.argv[1] != "--brightness" and sys.argv[
        1] != "--battery" and sys.argv[1] != "--ac" and sys.argv[1] != "--touchpad" and sys.argv[
        1] != "--autoconfig" and sys.argv[1] != "--screens":
        print("\nUsage:")
        print("--volume {up} | {down} | {toggle}")
        print("--brightness {up} | {down}")
        print("--battery {low} | {full}")
        print("--ac {connected} | {disconnected}")
        print("--touchpad {toggle} | {on} | {off}")
        print("--autoconfig {keys} | {tint2} | {all}")
        print("--screens {switch} | {single} | {clone} | {lr} | {rl} | {detect}")
        print("\nSee \033[1;34mhttps://github.com/nwg-piotr/obhud\033[0m for more.\n")

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

    elif sys.argv[1] == "--touchpad":
        if sys.argv[2] == "on" or sys.argv[2] == "off" or sys.argv[2] == "toggle":
            touchpad(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")

    elif sys.argv[1] == "--autoconfig":
        if sys.argv[2] == "tint2":
            autoconfig_tint2()
        elif sys.argv[2] == "keys":
            autoconfig_keys()
        elif sys.argv[2] == "all":
            autoconfig_all()
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")

    elif sys.argv[1] == "--screens":

        if os.path.isfile(values.preferences_file):
            values.preferences = load_preferences()
        else:
            print("Creating preferences...")
            create_preferences()
            values.preferences = load_preferences()

        if sys.argv[2] == "detect" or sys.argv[2] == "switch" or sys.argv[2] == "lr" or \
                sys.argv[2] == "rl" or sys.argv[2] == "clone" or sys.argv[2] == "single":
            screens(sys.argv[2])
        else:
            print("Unknown command \'" + sys.argv[2] + "\'")


if __name__ == "__main__":
    main()
