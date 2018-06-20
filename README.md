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
obhud --volume {up} | {down} | {toggle}
obhud --brightness {up} | {down}
obhud --battery {low} | {full}
obhud --ac {connected} | {disconnected}
obhud --touchpad {on} | {off} | {toggle}
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
    <keybind key="XF86TouchpadToggle">
      <action name="Execute">
        <command>obhud --touchpad toggle</command>
      </action>
    </keybind>
````

To make use of the battery-related commands, enter them in the 
Tint2 preferences:

![tint2](http://nwg.pl/obhud/images/tint2.png)

## Commands description

### obhud --volume up

Increases volume with the `amixer set Master 10%+ unmute` command, 
displays graphical notification:

![volume](http://nwg.pl/obhud/images/volume.png)

### obhud --volume down

Decreases volume with the `amixer set Master 10%-` command, displays
graphical notification.

### obhud --volume toggle

Turns sound on/off with the `amixer set Master toggle` command, displays
graphical notification.

![volume-toggle](http://nwg.pl/obhud/images/volume-toggle.png)

### obhud --brightness up

Increases brightness with the `xbacklight +10` command, displays
graphical notification:

![brightness](http://nwg.pl/obhud/images/brightness.png)

### obhud --brightness down

Decreases brightness with the `xbacklight -10` command, displays
graphical notification.

### obhud --battery low

Displays graphical notification (10 seconds long), then suspends 
the system with `systemctl suspend`.

![battery-low](http://nwg.pl/obhud/images/battery-low.png)

### obhud --battery full

Displays graphical notification.

### obhud --ac connected

Displays graphical notification:

![ac-connected](http://nwg.pl/obhud/images/ac-connected.png)

### obhud --ac disconnected

Displays graphical notification.

### obhud --touchpad toggle

**NOTE:** *If it comes to the touchpad button, it may behave differently on different machines:
either always return the `XF86TouchpadToggle` value, or `XF86TouchpadOn` and 
`XF86TouchpadOff` every second press. Check which way it works on your laptop with 
the `xev` command (`xorg-xev` package).*

The `obhud --touchpad toggle` command first checks the touchpad status, then turns
it on / off accordingly, and displays graphical notification:

![touchpad-on](http://nwg.pl/obhud/images/touchpad-on.png)

### obhud --touchpad on

Turns the touchpad on with the `synclient TouchpadOff=0` command, displays
graphical notification.

### obhud --touchpad off

Turns the touchpad off with the `synclient TouchpadOff=1` command, displays
graphical notification.

## Installation
I only packaged this script for Arch Linux. Please search
the [obhud](https://aur.archlinux.org/packages/obhud) package in AUR.

Feel free to make packages for other Linux distributions. Just let me
know for them to be linked here.

## Configuration
If you'd like to change default bash comands (e.g. to 
increase/decrease volume/brightness by 5% instead of 10%), you can
edit the `~/.config/obhud/obhud.conf` file. Leave double `%%` as is.
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
touchpad_on = synclient TouchpadOff=0
touchpad_off = synclient TouchpadOff=1

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

