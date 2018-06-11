# Openbox HUD

This script is intended to simplify assigning 
laptop-specific keys and events to actions and display a GNOME-like
graphical messages in [Openbox](http://openbox.org) window manager. 
This way one can, for instance, change volume level or screen brightness 
and see a graphical confirmation by just binding a key to a single 
command. Furthermore - assigning a command in [Tint2](https://gitlab.com/o9000/tint2) 
preferences allows to see alerts concerning the AC and
battery state, and also suspend on critical battery level.

![preview](http://nwg.pl/obhud/images/preview.png)

## Usage
````
obltk --volume {up} | {down} | {toggle}
obltk --brightness {up} | {down}
obltk --battery {low} | {full}
obltk --ac {connected} | {disconnected}
````
You can either assign commands to keys with [obkey](https://code.google.com/archive/p/obkey)

![obkey](http://nwg.pl/obhud/images/obkey1.png)

or just paste [this XML](https://gist.github.com/nwg-piotr/d357206b3779362797e9c43879f38615) 
into the `<keyboard></keyboard>` section of your `rc.xml` file.

To make use of the battery-related commands, enter them in the 
Tint2 preferences:

![tint2](http://nwg.pl/obhud/images/tint2.png)

## Commands description

`obltk --volume up`

Increases volume with the `amixer set Master 10%+` command, displays
graphical notification:

![volume](http://nwg.pl/obhud/images/volume.png)

`obltk --volume down`

Decreases volume with the `amixer set Master 10%-` command, displays
graphical notification.

`obltk --volume toggle`

Decreases volume with the `amixer set Master toggle` command, displays
graphical notification.

## Installation
Since the script is just the first stage of development a more
complex solution, packaging it seems to make no sense at the moment.
You'll have to copy files manually, and also take care of 
dependencies.

1. Create a folder in the location you want and place the `obltk.py` 
and `commands.py` files in it.
2. Create a launcher script, entering the location you selected:
````
#!/bin/sh
exec python /PathTo/YourFolder/obltk.py "$@"
````
and save as `/usr/bin/obltk`. Make the file executable.

## Dependencies (Arch Linux)
Make sure you have the following packages installed:
- `python` *(3.6, not python2)*
- `alsa-utils`
- `xorg-xbacklight`
- `libnotify`
- `notify-osd`