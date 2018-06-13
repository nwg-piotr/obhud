# Openbox HUD

This script is intended to simplify assigning 
laptop-specific keys and events to actions and display ~~slightly gnomish~~
graphical messages in [Openbox](http://openbox.org) window manager. 
This way one can, for instance, change volume level or screen brightness 
and see a graphical confirmation by just binding a key to a single 
command. Furthermore - assigning a command in [Tint2](https://gitlab.com/o9000/tint2) 
preferences allows to see alerts concerning the AC and
battery state, and also suspend on critical battery level.

![preview](http://nwg.pl/obhud/images/preview1.png)

## Usage
````
obltk --volume {up} | {down} | {toggle}
obltk --brightness {up} | {down}
obltk --battery {low} | {full}
obltk --ac {connected} | {disconnected}
````
You can either assign commands to keys with [obkey](https://code.google.com/archive/p/obkey)...

![obkey](http://nwg.pl/obhud/images/obkey1.png)

...or just paste the XML below 
into the `<keyboard></keyboard>` section of your `rc.xml` file:

````xml
    <keybind key="XF86MonBrightnessDown">
      <action name="Execute">
        <command>obhud --brightness down</command>
      </action>
    </keybind>
    <keybind key="XF86MonBrightnessUp">
      <action name="Execute">
        <command>obhud --brightness up</command>
      </action>
    </keybind>
    <keybind key="XF86AudioRaiseVolume">
      <action name="Execute">
        <command>obhud --volume up</command>
      </action>
    </keybind>
    <keybind key="XF86AudioLowerVolume">
      <action name="Execute">
        <command>obhud --volume down</command>
      </action>
    </keybind>
    <keybind key="XF86AudioMute">
      <action name="Execute">
        <command>obhud --volume toggle</command>
      </action>
    </keybind>
````

To make use of the battery-related commands, enter them in the 
Tint2 preferences:

![tint2](http://nwg.pl/obhud/images/tint2.png)

## Commands description

### obltk --volume up

Increases volume with the `amixer set Master 10%+ unmute` command, 
displays graphical notification:

![volume](http://nwg.pl/obhud/images/volume.png)

### obltk --volume down

Decreases volume with the `amixer set Master 10%-` command, displays
graphical notification.

### obltk --volume toggle

Decreases volume with the `amixer set Master toggle` command, displays
graphical notification.

### obltk --brightness up

Increases brightness with the `xbacklight +10` command, displays
graphical notification:

![brightness](http://nwg.pl/obhud/images/brightness.png)

### obltk --brightness down

Decreases brightness with the `xbacklight -10` command, displays
graphical notification.

### obltk --battery low

Displays graphical notification (10 seconds long), then suspends 
the system with `systemctl suspend`.

![battery-low](http://nwg.pl/obhud/images/battery-low.png)

### obltk --battery full

Displays graphical notification.

### obltk --ac connected

Displays graphical notification:

![ac-connected](http://nwg.pl/obhud/images/ac-connected.png)

### obltk --ac disconnected

Displays graphical notification.

## Installation
I only packaged this script for Arch Linux so far. Please search
the [obhud](https://aur.archlinux.org/packages/obhud) package in AUR.

Feel free to make packages for other Linux distributions. Just let me
know for them to be linked here.

## Configuration
If you'd like to change default bash comands (e.g. to 
increase/decrease volume/brightness by 5% instead of 10%), you can
edit the ~/.config/obhud/obhud.conf file. Leave double `%%` as is.
````commandline
[Commands]
# You can modify default commands in the ~/config/obhud/obhud.conf file.
# In case you got lost, just delete it. It'll be re-created from
# default /etc/obhud/obhud.conf file.
volume_up = amixer set Master 10%%+ unmute -q
volume_down = amixer set Master 10%%- -q
volume_toggle = amixer set Master toggle -q
brightness_up = xbacklight +10
brightness_down = xbacklight -10
```` 
## Troubleshooting
For the `xbacklight` command to work, you may need the 
`/etc/X11/xorg.conf.d/10-backlight.conf` file:
````commandline
Section "Device"
    Identifier  "Card0"
    Driver      "intel"
    Option      "Backlight"  "intel_backlight"
EndSection
````

## Credits
I used icons from [numix-gtk-theme](https://www.archlinux.org/packages/community/any/numix-gtk-theme)
by [Numix Project](http://numixproject.org) as the base of the icon set. Thanks!

