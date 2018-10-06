import os
import subprocess
import pickle

from tkinter import Tk, Frame, Canvas
from PIL import Image, ImageTk

import configparser

import lxml.etree as ET  # depends on python-lxml

import values

volume_get_level = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $2 }\' > ~/tmp'
volume_get_status = 'amixer sget Master | grep \'Right:\' | awk -F\'[][]\' \'{ print $4 }\' > ~/tmp'

brightness_get_level = 'xbacklight -get > ~/tmp'
light_get_brightness = 'light -G > ~/tmp'

touchpad_get_status = 'synclient -l | grep TouchpadOff | awk \'{print $3}\' > ~/tmp'


class Hud(Tk):

    def __init__(self, icon, message):
        super().__init__()
        self.geometry(values.hud_geometry)
        self.frame = Frame(self)
        self.frame.pack()
        self.canvas = Canvas(self.frame, bg="gray16", width=values.hud_side, height=values.hud_side,
                             highlightthickness=1, highlightbackground="gray30")
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.pack()

        self.overrideredirect(1)

        image = Image.open(icon)
        image = image.resize((values.hud_side, values.hud_side), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)

        self.canvas.create_image(values.hud_side / 2, values.hud_side / 2, image=self.img)
        self.canvas.create_text(values.hud_side / 2, int(190 * values.hud_scale),
                                font="Helvetica" + str(int(14 * values.hud_scale)),
                                text=message, fill='light gray')

    def callback(self, event):
        os.system('pkill -9 -f \'ffplay\'')
        self.destroy()


def play_sound(audio_file):
    subprocess.Popen(["nohup", "ffplay", "-loop", "8", "-nodisp", "-autoexit", "icons/" + audio_file],
                     stdout=open('/dev/null', 'w'))


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
    # We will use the optional light-git package if installed or xbacklight if not
    if command == "up":
        if values.light_installed:
            os.system(values.light_increase)
        else:
            os.system(values.brightness_up)
    elif command == "down":
        if values.light_installed:
            os.system(values.light_decrease)
        else:
            os.system(values.brightness_down)

    if values.light_installed:
        os.system(light_get_brightness)
    else:
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
    elif command == "LOW":
        play_sound("battery-low.mp3")
        show_hud("battery-low", "Battery low", 10000)
        os.system('systemctl suspend')
    elif command == "full":
        show_hud("battery-full", "Battery full", 2000)


def ac(command):
    if command == "connected":
        os.system('pkill -9 -f \'ffplay\'')
        show_hud("ac-connected", "AC connected", 1500)
    elif command == "disconnected":
        show_hud("ac-disconnected", "AC disconnected", 1500)


def alarm(message):
    play_sound("timer.mp3")
    show_hud("timer", message, 30000)


def screens(command):
    if command == 'detect':
        screens_detect(False)

    elif command == "right":
        screens_right(False)

    elif command == "left":
        screens_left(False)

    elif command == "above":
        screens_above(False)

    elif command == "below":
        screens_below(False)

    elif command == "clone":
        screens_clone(False)

    elif command == "single":
        screens_single(False)

    elif command == "switch":
        screens_switch()

    elif command == "switchv":
        screens_switchv()


def measure_screen():
    os.system('xrandr | grep \'*\' > ~/tmp')
    resolution_string = open(values.tmp, 'r').read()
    # os.remove(values.tmp)

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
                    and config.has_option("Commands", "light_increase") \
                    and config.has_option("Commands", "light_decrease") \
                    and config.has_option("Commands", "touchpad_on") \
                    and config.has_option("Commands", "touchpad_off"):

                values.volume_up = config.get("Commands", "volume_up")
                values.volume_down = config.get("Commands", "volume_down")
                values.volume_toggle = config.get("Commands", "volume_toggle")
                values.brightness_up = config.get("Commands", "brightness_up")
                values.brightness_down = config.get("Commands", "brightness_down")
                values.light_increase = config.get("Commands", "light_increase")
                values.light_decrease = config.get("Commands", "light_decrease")
                values.touchpad_on = config.get("Commands", "touchpad_on")
                values.touchpad_off = config.get("Commands", "touchpad_off")

            else:
                raise IOError('Missing configuration key')

    except IOError:
        print("~/.config/obhud/obhud.conf not found or invalid, copying default...")
        os.system('cp -rf /etc/obhud ~/.config')
        config_load()


def autoconfig_tint2(from_menu):
    tint2rc = os.getenv("HOME") + '/.config/tint2/tint2rc'

    timer_found = False

    if os.path.isfile(tint2rc):

        if input("\n You are about to modify the tint2rc file, proceed? (Y/N) ").upper() == "Y":

            try:
                with open(tint2rc, 'r') as file:
                    data = file.readlines()

                for i in range(len(data)):
                    row = data[i]
                    if row.startswith('battery_low_cmd'):
                        data[i] = "battery_low_cmd = obhud --battery LOW\n"
                    elif row.startswith('battery_full_cmd'):
                        data[i] = "battery_full_cmd = obhud --battery full\n"
                    elif row.startswith('ac_connected_cmd'):
                        data[i] = "ac_connected_cmd = obhud --ac connected\n"
                    elif row.startswith('ac_disconnected_cmd'):
                        data[i] = "ac_disconnected_cmd = obhud --ac disconnected\n"

                    # Check for existence of the Timer executor
                    if not timer_found and row.find("obhud/timer.sh") >= 0:
                        timer_found = True

                # Append the Timer executor on the very end
                if not timer_found:

                    if input("\n Add the Timer/Stopwatch executor? (Y/N) ").upper() == "Y":
                        data.append("\n#-------------------------------------\n")
                        data.append("# Executor 99\n")
                        data.append("execp = new\n")
                        data.append("execp_command = ~/.config/obhud/timer.sh\n")
                        data.append("execp_interval = 1\n")
                        data.append("execp_has_icon = 1\n")
                        data.append("execp_cache_icon = 0\n")
                        data.append("execp_continuous = 0\n")
                        data.append("execp_markup = 0\n")
                        data.append("execp_tooltip =\n")
                        data.append("execp_lclick_command = obhud --timer gui\n")
                        data.append("execp_rclick_command =\n")
                        data.append("execp_mclick_command =\n")
                        data.append("execp_uwheel_command =\n")
                        data.append("execp_dwheel_command =\n")
                        data.append("execp_font = Cantarell 8\n")
                        data.append("execp_font_color = #ffffff 100\n")
                        data.append("execp_padding = 0 0\n")
                        data.append("execp_background_id = 5\n")
                        data.append("execp_centered = 1\n")
                        data.append("execp_icon_w = 0\n")
                        data.append("execp_icon_h = 0\n")

                        for i in range(len(data)):
                            row = data[i]
                            # Add the executor to panel items
                            if row.startswith('panel_items'):
                                data[i] = row[:-1] + "E\n"

                # backup the current file
                os.system('mv -f ' + tint2rc + ' ' + tint2rc + '.bck.obhud')

                with open(tint2rc, 'w') as file:
                    file.writelines(data)

                print("\n Tint2 battery and AC commands added to the \'tint2rc\' file.")
                print(" Original file renamed to \'tint2rc.bck.obhud\'.\n")

                os.system('killall -SIGUSR1 tint2 || pkill -SIGUSR1 -x tint2')

                if from_menu:
                    input("\nPress any key... ")

            except IOError:
                print("ERROR: couldn\'t open ~/.config/tint2/tint2rc")

        else:
            print("\nAutoconfig Tint2 cancelled.")
    else:
        print("\nFile not found: ~/.config/tint2/tint2rc\n")


def autoconfig_keys(from_menu):
    if os.path.isfile(os.getenv("HOME") + '/.config/openbox/rc.xml'):

        if input("\n You are about to modify the rc.xml file, proceed? (Y/N) ").upper() == "Y":

            try:
                rcxml = os.getenv("HOME") + '/.config/openbox/rc.xml'
                parser = ET.XMLParser(remove_blank_text=True)
                tree = ET.parse(rcxml, parser)
                root = tree.getroot()
                keyboard = root.find('{http://openbox.org/3.4/rc}keyboard')

                for child in keyboard:
                    if child.tag == '{http://openbox.org/3.4/rc}keybind' \
                            and child.get('key') == 'XF86MonBrightnessDown' \
                            or child.get('key') == 'XF86MonBrightnessUp' \
                            or child.get('key') == 'XF86AudioRaiseVolume' \
                            or child.get('key') == 'XF86AudioLowerVolume' \
                            or child.get('key') == 'XF86AudioMute' \
                            or child.get('key') == 'XF86TouchpadToggle' \
                            or child.get('key') == 'XF86TouchpadOn' \
                            or child.get('key') == 'XF86TouchpadOff' \
                            or child.get('key') == 'W-P' \
                            or child.get('key') == 'S-W-P':
                        child.getparent().remove(child)

                keybindings = {'XF86MonBrightnessDown': 'obhud --brightness down',
                               'XF86MonBrightnessUp': 'obhud --brightness up',
                               'XF86AudioRaiseVolume': 'obhud --volume up',
                               'XF86AudioLowerVolume': 'obhud --volume down',
                               'XF86AudioMute': 'obhud --volume toggle',
                               'XF86TouchpadToggle': 'obhud --touchpad toggle',
                               'XF86TouchpadOn': 'obhud --touchpad on',
                               'XF86TouchpadOff': 'obhud --touchpad off',
                               'W-P': 'obhud --screens switch',
                               'S-W-P': 'obhud --screens switchv'}

                for key, command in keybindings.items():
                    bind_key(keyboard, key, command)

                os.system('mv -f ' + rcxml + ' ' + rcxml + '.bck.obhud')

                tree.write(rcxml, encoding='utf-8', with_tail=True, xml_declaration=True, method='xml',
                           pretty_print=True)

                print("\n Key bindings added to the \'rc.xml\' file.")
                print(" Original file renamed to \'rc.xml.bck.obhud\'.\n")

                os.system('openbox --reconfigure')

                if from_menu:
                    input("\nPress any key... ")

            except:
                print("ERROR: couldn\'t open ~/.config/openbox/rc.xml")

        else:
            print("\nAutoconfig keybindings cancelled.")
    else:
        print("\nFile not found: ~/.config/openbox/rc.xml\n")


def bind_key(et_item, key, com):
    keybind = ET.SubElement(et_item, 'keybind')
    keybind.set('key', key)
    action = ET.SubElement(keybind, 'action')
    action.set('name', 'Execute')
    command = ET.SubElement(action, 'command')
    command.text = com


def autoconfig_all():
    print("\nThis will assign obhud commands and notifications to keys in Openbox rc.xml")
    print("configuration file, and also to AC- and battery-related events in Tint2.")
    autoconfig_keys(False)
    autoconfig_tint2(False)


class UserPreferences(object):
    def __init__(self):
        self.screen_primary = "none"
        self.screen_secondary = "none"
        self.secondary_resolution = "none"
        self.secondary_rate = "none"
        self.screens_setup = "none"


def load_preferences():
    with open(values.preferences_file, 'rb') as input_data:
        return pickle.load(input_data)


def create_preferences():
    preferences = UserPreferences()
    with open(values.preferences_file, 'wb') as output:
        pickle.dump(preferences, output, pickle.HIGHEST_PROTOCOL)


def save_preferences():
    with open(values.preferences_file, 'wb') as output:
        pickle.dump(values.preferences, output, pickle.HIGHEST_PROTOCOL)


def screens_detect(silent):
    os.system('xrandr | grep \' connected\' > ~/tmp')
    screens_string = open(values.tmp, 'r').read()
    os.remove(values.tmp)

    my_screens = screens_string.rstrip().split('\n')

    # primary screen details: we only need the name
    screen0 = my_screens[0].split()[0]
    values.preferences.screen_primary = screen0

    if len(my_screens) > 1:
        # secondary screen details: name, resolution and frequency

        # take the name from above
        screen1 = my_screens[1].split()[0]
        values.preferences.screen_secondary = screen1

        # find missing resolution and frequency; xrandr may return '*+' or ' +' in appropriate lines!
        os.system('xrandr | grep -e \'*+\' -e \' +\' > ~/tmp')
        resolution_string = open(values.tmp, 'r').read().rstrip()
        os.remove(values.tmp)

        # second line should contain secondary display data
        both_screens = resolution_string.split("\n")

        secondary_screen = both_screens[1].split()

        values.preferences.secondary_resolution = secondary_screen[0]
        values.preferences.secondary_rate = secondary_screen[1].split(".")[0]

    else:
        values.preferences.screen_secondary = "none"
        values.preferences.secondary_resolution = 'none'
        values.preferences.secondary_rate = 'none'

    save_preferences()

    if not silent:
        print(values.preferences.screen_primary, end="")
        print(
            " | " + values.preferences.screen_secondary + " " + values.preferences.secondary_resolution + " " + values.preferences.secondary_rate)


def screens_right(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --mode ' \
              + values.preferences.secondary_resolution + ' --rate ' \
              + values.preferences.secondary_rate + ' --right-of ' + values.preferences.screen_primary
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = "right"
        save_preferences()
        show_hud("screens-right", "Secondary right", 1500)
    else:
        screens_single(silent)


def screens_left(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --mode ' \
              + values.preferences.secondary_resolution + ' --rate ' \
              + values.preferences.secondary_rate + ' --left-of ' + values.preferences.screen_primary
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'left'
        save_preferences()
        show_hud("screens-left", "Secondary left", 1500)
    else:
        screens_single(silent)


def screens_above(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --mode ' \
              + values.preferences.secondary_resolution + ' --rate ' \
              + values.preferences.secondary_rate + ' --above ' + values.preferences.screen_primary
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'above'
        save_preferences()
        show_hud("screens-above", "Secondary above", 1500)
    else:
        screens_single(silent)


def screens_below(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --mode ' \
              + values.preferences.secondary_resolution + ' --rate ' \
              + values.preferences.secondary_rate + ' --below ' + values.preferences.screen_primary
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'below'
        save_preferences()
        show_hud("screens-below", "Secondary below", 1500)
    else:
        screens_single(silent)


def screens_clone(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --mode ' \
              + values.preferences.secondary_resolution + ' --rate ' \
              + values.preferences.secondary_rate + ' --same-as ' + values.preferences.screen_primary
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'clone'
        save_preferences()
        show_hud("screens-clone", "Clone screen", 1500)
    else:
        screens_single(silent)


def screens_single(silent):
    screens_detect(True)
    if values.preferences.screen_secondary != "none":
        cmd = 'xrandr --auto --output ' + values.preferences.screen_secondary + ' --off'
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'single'
        save_preferences()
    else:
        cmd = 'xrandr --auto'
        if not silent:
            print(cmd)
        os.system(cmd)
        values.preferences.screens_setup = 'single'
        save_preferences()
        if not silent:
            print("Secondary screen not detected")
    show_hud("screens-single", "Single screen", 1500)


def screens_switch():
    load_preferences()
    if values.preferences.screens_setup != "none":
        if values.preferences.screens_setup == 'above' or values.preferences.screens_setup == 'below' or values.preferences.screens_setup == 'left':
            screens_single(True)
        elif values.preferences.screens_setup == 'single':
            screens_clone(True)
        elif values.preferences.screens_setup == 'clone':
            screens_right(True)
        elif values.preferences.screens_setup == 'right':
            screens_left(True)
        elif values.preferences.screens_setup == 'left':
            screens_single(True)
    else:
        values.preferences.screens_setup = 'single'
        save_preferences()


def screens_switchv():
    load_preferences()
    if values.preferences.screens_setup != "none":
        if values.preferences.screens_setup == 'left' or values.preferences.screens_setup == 'right' or values.preferences.screens_setup == 'below':
            screens_single(True)
        elif values.preferences.screens_setup == 'single':
            screens_clone(True)
        elif values.preferences.screens_setup == 'clone':
            screens_above(True)
        elif values.preferences.screens_setup == 'above':
            screens_below(True)
        elif values.preferences.screens_setup == 'below':
            screens_single(True)
    else:
        values.preferences.screens_setup = 'single'
        save_preferences()
