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

ver_string = "0.2.1"
whatsnew = " *** NEW: optional use of light-git (AUR) instead of xbacklight"

screen_dimensions = None
screen_width = None
screen_height = None
hud_side = None
hud_scale = None
hud_margin_v = None

hud_geometry = None

tmp = ""

volume_up = ''
volume_down = ''
volume_toggle = ''

brightness_up = ''
brightness_down = ''
light_increase = ''
light_decrease = ''
touchpad_on = ''
touchpad_off = ''

preferences_file = ""
preferences = None
screen_primary = ""
screen_secondary = ""

dialog_action = None

light_installed = False
tint2_installed = False
