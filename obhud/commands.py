import os

from tkinter import Tk, Frame, Canvas
from PIL import Image, ImageTk

import configparser

import lxml.etree as ET

import values

volume_get_level = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $2 }\' > ~/tmp'
volume_get_status = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $4 }\' > ~/tmp'

brightness_get_level = 'xbacklight -get > ~/tmp'

touchpad_get_status = 'synclient -l | grep TouchpadOff | awk \'{print $3}\' > ~/tmp'


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
        os.system(values.volume_up)
    elif command == "down":
        os.system(values.volume_down)
    elif command == "toggle":
        os.system(values.volume_toggle)

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
    if command == "up":
        os.system(values.brightness_up)
    elif command == "down":
        os.system(values.brightness_down)

    os.system(brightness_get_level)
    brightness_lvl = open(values.tmp, 'r').read()
    os.remove(values.tmp)

    brightness_int = 0
    try:
        brightness_int = int(round(float(brightness_lvl.rstrip())))
        brightness_str = str(brightness_int) + "%"
    except ValueError:
        brightness_str = "xbacklight?"

    if brightness_int == 100:
        brightness_icon = "brightness-full"
    elif brightness_int > 60:
        brightness_icon = "brightness-high"
    elif brightness_int >= 40:
        brightness_icon = "brightness-medium"
    elif brightness_int > 0:
        brightness_icon = "brightness-low"
    else:
        brightness_icon = "brightness-medium"

    show_hud(brightness_icon, brightness_str, 1000)


def touchpad(command):
    if command == "on":
        os.system(values.touchpad_on)
        show_hud("touchpad-on", "Touchpad on", 1000)
    elif command == "off":
        os.system(values.touchpad_off)
        show_hud("touchpad-off", "Touchpad off", 1000)
    elif command == "toggle":
        os.system(touchpad_get_status)
        touchpad_status = open(values.tmp, 'r').read()
        touchpad_status = touchpad_status.rstrip()
        os.remove(values.tmp)

        if touchpad_status == "0":
            os.system(values.touchpad_off)
            show_hud("touchpad-off", "Touchpad off", 1000)
        elif touchpad_status == "1":
            os.system(values.touchpad_on)
            show_hud("touchpad-on", "Touchpad on", 1000)
        else:
            print("Failed checking status")


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


def config_load():
    config = configparser.ConfigParser()
    try:
        with open(os.getenv("HOME") + '/.config/obhud/obhud.conf') as f:
            config.read_file(f)
            if config.has_section("Commands") \
                    and config.has_option("Commands", "volume_up") \
                    and config.has_option("Commands", "volume_down") \
                    and config.has_option("Commands", "volume_toggle") \
                    and config.has_option("Commands", "brightness_up") \
                    and config.has_option("Commands", "brightness_down") \
                    and config.has_option("Commands", "touchpad_on") \
                    and config.has_option("Commands", "touchpad_off"):

                values.volume_up = config.get("Commands", "volume_up")
                values.volume_down = config.get("Commands", "volume_down")
                values.volume_toggle = config.get("Commands", "volume_toggle")
                values.brightness_up = config.get("Commands", "brightness_up")
                values.brightness_down = config.get("Commands", "brightness_down")
                values.touchpad_on = config.get("Commands", "touchpad_on")
                values.touchpad_off = config.get("Commands", "touchpad_off")

                # print("config loaded from ~/.config/obhud/obhud.conf")
            else:
                raise IOError('Missing configuration key')

    except IOError:
        print("~/.config/obhud/obhud.conf not found or invalid, copying default...")
        os.system('cp -rf /etc/obhud ~/.config')
        config_load()


def autoconfig_tint2():
    tint2rc = os.getenv("HOME") + '/.config/tint2/tint2rc'

    if input("This will modify the tint2rc file, proceed? (Y/N) ").upper() == "Y":

        try:
            with open(tint2rc, 'r') as file:
                data = file.readlines()

            for i in range(len(data)):
                row = data[i]
                if row.startswith('battery_low_cmd'):
                    data[i] = "battery_low_cmd = obhud --battery low\n"
                elif row.startswith('battery_full_cmd'):
                    data[i] = "battery_full_cmd = obhud --battery full\n"
                elif row.startswith('ac_connected_cmd'):
                    data[i] = "ac_connected_cmd = obhud --ac connected\n"
                elif row.startswith('ac_disconnected_cmd'):
                    data[i] = "ac_disconnected_cmd = obhud --ac disconnected\n"

            os.system('mv -f ' + tint2rc + ' ' + tint2rc + '.bck.obhud')

            with open(tint2rc, 'w') as file:
                file.writelines(data)

            os.system('killall -SIGUSR1 tint2 || pkill -SIGUSR1 -x tint2')
            print("\nTint2 battery and AC commands added to the \'tint2rc\' file")
            print("Original file renamed to \'tint2rc.bck.obhud\'")

        except IOError:
            print("~/.config/tint2/tint2rc file not found")

    else:
        print("\nAutoconfig Tint2 cancelled")


def autoconfig_keys():
    rcxml = os.getenv("HOME") + '/.config/openbox/rc.xml'
    tree = ET.parse(rcxml)
    root = tree.getroot()
    keyboard = root.find('{http://openbox.org/3.4/rc}keyboard')

    for child in keyboard:
        if child.tag == '{http://openbox.org/3.4/rc}keybind' and child.get('key').startswith('XF86'):
            print(child.tag, child.attrib)
            for action in child:
                print(action.tag, action.attrib)
                for command in action:
                    print(command.tag, command.text)

            child.getparent().remove(child)

    tree.write(os.getenv("HOME") + '/.config/openbox/rc_new.xml', encoding='utf-8', with_tail=True, xml_declaration=True)