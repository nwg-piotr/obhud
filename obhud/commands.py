import os

from tkinter import Tk, Frame, Canvas  # Dependencies!
from PIL import Image, ImageTk  # Dependencies!

import values

volume_get_level = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $2 }\' > ~/tmp'
volume_up = 'amixer set Master 10%+'
volume_down = 'amixer set Master 10%-'
volume_toggle = 'amixer set Master toggle'
volume_get_status = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $4 }\' > ~/tmp'

brightness_get_level = 'xbacklight -get > ~/tmp'
brightness_up = 'xbacklight +10'
brightness_down = 'xbacklight -10'


class Hud(Tk):

    def __init__(self, icon, message):
        super().__init__()
        self.geometry(values.hud_geometry)
        self.frame = Frame(self)
        self.frame.pack()
        self.canvas = Canvas(self.frame, bg="gray16", width=values.hud_side, height=values.hud_side,
                             highlightthickness=1, highlightbackground="gray30")
        self.canvas.pack()

        self.overrideredirect(1)

        image = Image.open(icon)
        image = image.resize((values.hud_side, values.hud_side), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)

        self.canvas.create_image(values.hud_side / 2, values.hud_side / 2, image=self.img)
        self.canvas.create_text(values.hud_side / 2, int(190 * values.hud_scale),
                                font="Helvetica" + str(int(14 * values.hud_scale)),
                                text=message, fill='light gray')


def show_hud(icon, message, timeout):
    hud = Hud("icons/" + icon + ".png", message)
    hud.after(timeout, lambda: hud.destroy())
    hud.mainloop()


def volume(command):
    if command == "up":
        os.system(volume_up)
    elif command == "down":
        os.system(volume_down)
    elif command == "toggle":
        os.system(volume_toggle)

    os.system(volume_get_level)
    volume_lvl = open(values.tmp, 'r').read()
    os.remove(values.tmp)
    volume_lvl = volume_lvl.split("%")[0]

    volume_int = int(round(float(volume_lvl.rstrip())))
    if volume_int == 100:
        volume_icon = "volume-high"
    elif volume_int >= 50:
        volume_icon = "volume-medium"
    elif volume_int > 0:
        volume_icon = "volume-low"
    else:
        volume_icon = "volume-zero"

    if command != "toggle":

        show_hud(volume_icon, volume_lvl + "%", 1000)

    else:
        os.system(volume_get_status)
        volume_status = open(values.tmp, 'r').read()
        volume_status = volume_status.rstrip()
        os.remove(values.tmp)

        if volume_status == "off":
            show_hud("volume-muted", "Muted", 1000)
        else:
            show_hud(volume_icon, volume_lvl + "%", 1000)


def brightness(command):
    """
    For this to work we need the xorg-xbacklight package.
    You may also need the /etc/X11/xorg.conf.d/10-backlight.conf file as below:

    Section "Device"
        Identifier  "Card0"
        Driver      "intel"
        Option      "Backlight"  "intel_backlight"
    EndSection
    """
    if command == "up":
        os.system(brightness_up)
    elif command == "down":
        os.system(brightness_down)

    os.system(brightness_get_level)
    brightness_lvl = open(values.tmp, 'r').read()
    os.remove(values.tmp)

    try:
        brightness_str = str(int(round(float(brightness_lvl.rstrip())))) + "%"
    except ValueError:
        brightness_str = "xbacklight?"

    show_hud("display-brightness", brightness_str, 1000)


def battery(command):
    if command == "low":
        show_hud("battery-low", "Battery low", 10000)
        os.system('systemctl suspend')
    elif command == "full":
        show_hud("battery-full", "Battery full", 2000)


def ac(command):
    if command == "connected":
        show_hud("ac-connected", "AC connected", 1500)
    elif command == "disconnected":
        show_hud("ac-disconnected", "AC disconnected", 1500)


def measure_screen():
    os.system('xrandr | grep \'*\' > ~/tmp')
    resolution_string = open(values.tmp, 'r').read()
    os.remove(values.tmp)

    resolution = resolution_string.split()[0]
    width, height = resolution.split('x')

    return int(width), int(height), float(int(width) / 1920)


def check_dimensions():
    # Get screen width, height and graphics scaling factor (as a percentage of full hd screen width)
    values.screen_dimensions = measure_screen()
    values.screen_width = values.screen_dimensions[0]
    values.screen_height = values.screen_dimensions[1]
    values.hud_side = int(values.screen_dimensions[0] * 0.13)  # HUD window side in pixels
    values.hud_scale = values.screen_dimensions[2]
    values.hud_margin_v = int(values.screen_height * 0.13)  # HUD vertical margin in pixels

    # Create the window geometry, e.g. "300x150+50+50"
    values.hud_geometry = str(values.hud_side) + "x" + str(values.hud_side) + "+" + str(
        int(values.screen_width / 2 - values.hud_side / 2)) + "+" + str(
        values.screen_height - values.hud_side - values.hud_margin_v)
