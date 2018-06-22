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

## Quick start

**CAUTION:** 
*I did my best to test the script and make sure it's safe. However, the `--autoconfig`
options make changes to essential system configuration files. Making backups of
`~/.config/openbox/rc.xml` and `~/.config/tint2/tin2rc` files is recommended.*

If you have [Tint2](https://gitlab.com/o9000/tint2) installed, just enter one command in terminal:
````
obhud --autoconfig all
````
This will add all the necessary keybindings in `~/home/config/openbox/rc.xml`
and configure Tint2 AC- and battery-related commands in `~/home/config/tint2/tint2rc`.

Otherwise, you can only make keybindings in the `rc.xml` file with
````
obhud -autoconfig keys
````

For more info [check Wiki](https://github.com/nwg-piotr/obhud/wiki).

## Credits
I used icons from [numix-gtk-theme](https://www.archlinux.org/packages/community/any/numix-gtk-theme)
by [Numix Project](http://numixproject.org) as the base of the icon set. Thanks!

