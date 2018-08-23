import sys
import time
import os


timer_file = os.getenv("HOME") + "/.config/obhud/timer.sh"


def main():

    if len(sys.argv) > 1:

        try:
            seconds = int(sys.argv[1])
            os.system('cp -rf /etc/obhud/timer.sh ~/.config/obhud/timer.sh')
            countdown(seconds)

        except ValueError:
            print("Not a number: " + sys.argv[1])

        exit(0)


def countdown(seconds):
    finish_at = int(time.time()) + seconds

    while int(time.time()) <= finish_at:
        os.system("echo -e \"printf \'%8s\n%8s \' Timer: \"" + formatted_time(finish_at - int(time.time())) + ' > ' + timer_file)
        time.sleep(1)

    # Just in case
    # os.system("echo -e \"printf \'%8s\n%8s \' Timer: 00:00:00\"" + ' > ' + timer_file)
    os.system("echo \"printf \'\'\"" + ' > ' + timer_file)
    os.system("obhud --timer ring")


def formatted_time(time_in_seconds):

    if time_in_seconds > 359999:
        return "Overflow"

    else:
        hours = int(time_in_seconds / 3600)
        rest = time_in_seconds % 3600
        minutes = int(rest / 60)
        seconds = rest % 60

        if hours < 10:
            hours_str = "0" + str(hours) + ":"
        else:
            hours_str = str(hours) + ":"

        if minutes < 10:
            minutes_str = "0" + str(minutes)  + ":"
        else:
            minutes_str = str(minutes)  + ":"

        if seconds < 10:
            seconds_str = "0" + str(seconds)
        else:
            seconds_str = str(seconds)

        return hours_str + minutes_str + seconds_str


if __name__ == "__main__":
    main()