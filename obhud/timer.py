import time
import os
from tkinter import *
import values
from commands import check_dimensions
from PIL import Image, ImageTk

timer_file = os.getenv("HOME") + "/.config/obhud/timer.sh"


class Dialog(Tk):
    def __init__(self):
        super().__init__()
        self.title("Obhud: Timer & Stopwatch")

        image = Image.open('icons/icon.png')
        img = ImageTk.PhotoImage(image)
        self.tk.call('wm', 'iconphoto', self._w, img)

        self.geometry("+%d+%d" % (
            int(values.screen_width / 2 - values.hud_side / 2),
            int(values.screen_height - values.hud_side - values.hud_margin_v)))

        Label(self, text="Hours:").grid(row=0, sticky=E, padx=5)
        Label(self, text="Minutes:").grid(row=1, sticky=E, padx=5)
        Label(self, text="Seconds:").grid(row=2, sticky=E, padx=5)

        self.hh = Spinbox(self, from_=0, to=99)
        self.mm = Spinbox(self, from_=0, to=59)
        self.ss = Spinbox(self, from_=0, to=59)

        self.hh.grid(row=0, column=1, padx=2, pady=2)
        self.mm.grid(row=1, column=1, padx=2, pady=2)
        self.ss.grid(row=2, column=1, padx=2, pady=2)

        self.b1 = Button(self, text="Start timer", command=self.start_timer)
        self.b2 = Button(self, text="Stopwatch", command=self.start_stopwatch)
        self.b3 = Button(self, text="Clear/Close", command=self.clear_close)

        self.b1.grid(row=0, column=2, padx=5, pady=5)
        self.b2.grid(row=1, column=2, padx=5)
        self.b3.grid(row=2, column=2, padx=5, pady=5)

        values.dialog_action = None

    def start_timer(self):
        values.dialog_action = int(float(self.hh.get()) * 3600) + int(float(self.mm.get()) * 60) + int(float(self.ss.get()))
        self.destroy()

    def start_stopwatch(self):
        values.dialog_action = -1
        self.destroy()

    def clear_close(self):
        values.dialog_action = 0
        self.destroy()


def main():
    values.tmp = os.getenv("HOME") + "/tmp".rstrip()

    check_dimensions()

    os.system('cp -rf icons/timer.svg ~/.config/obhud/timer.svg')

    if len(sys.argv) > 1:

        argument = sys.argv[1]

        if argument == "gui":
            gui = Dialog()
            gui.mainloop()

            if values.dialog_action is not None:
                argument = str(values.dialog_action) + "s"

        unit = argument[len(argument) - 1:]
        value = argument[0:len(argument) - 1]

        # By default we use the GUI above, but obhud should accept CLI commands, too: obhud --timer XXh | XXm | XXs
        try:
            seconds = int(value)

            if unit == 'h':
                seconds = seconds * 3600
            elif unit == 'm':
                seconds = seconds * 60
            elif unit != 's':
                raise ValueError()

            os.system('cp -rf /etc/obhud/timer.sh ~/.config/obhud/timer.sh')
            if seconds > 0:
                # Start Timer on any positive value
                countdown(seconds)
            elif seconds < 0:
                # Start Stopwatch on any negative value
                stopwatch()
            else:
                timer_clear()

        except ValueError:
            print("Improper format: `" + argument[
                1] + "`\nExamples: `1h` | `15m` | `90s` | `hours:minutes:seconds`| `minutes:seconds`| `seconds`\nMax value: `99h` | `99:59:59`")

        exit(0)


def countdown(seconds):
    finish_at = int(time.time()) + seconds

    while int(time.time()) <= finish_at:
        os.system("echo -e \"printf \'%8s\n%8s \' Timer: \"" + formatted_time(
            finish_at - int(time.time())) + ' > ' + timer_file)
        time.sleep(1)

    timer_clear()
    os.system("obhud --alarm timer")


def stopwatch():
    done = False
    started_at = int(time.time())

    while not done:
        os.system("echo -e \"printf \'%8s\n%8s \' Stopwatch: \"" + formatted_time(
            int(time.time()) - started_at) + ' > ' + timer_file)
        time.sleep(1)


def timer_clear():
    os.system('cp -rf icons/timer.svg ~/.config/obhud/timer.svg')
    values.timer_active = False


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
            minutes_str = "0" + str(minutes) + ":"
        else:
            minutes_str = str(minutes) + ":"

        if seconds < 10:
            seconds_str = "0" + str(seconds)
        else:
            seconds_str = str(seconds)

        return hours_str + minutes_str + seconds_str



if __name__ == "__main__":
    main()
