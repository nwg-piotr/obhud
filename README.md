# Openbox HUD

This script is intended to simplify assigning 
laptop-specific keys and events to actions and display ~~slightly gnomish~~
graphical messages in [Openbox](http://openbox.org) window manager. 
This way one can, for instance, change volume level or screen brightness 
and see a graphical confirmation by just binding a key to a single 
command. Furthermore - assigning a command in [Tint2](https://gitlab.com/o9000/tint2) 
preferences allows to see alerts concerning the AC and
battery state, and also suspend on critical battery level.

**New in 0.1.4 version:**

Switching primary/secondary display added. Please run `obhud --autoconfig keys` or add keybindings manually.

![preview](http://nwg.pl/obhud/images/preview1.png)

## Installation

Arch Linux: search the [obhud](https://aur.archlinux.org/packages/obhud) 
package in AUR.

## Quick start

![Terminal](http://nwg.pl/obhud/images/terminal.png)

Type `obhud` in terminal to access the menu, which allows to add 
default keybindings to `rc.xml` and commands to `tint2rc` file 
automatically. You'll also find syntax of each command here.

**CAUTION:** 
*I did my best to test the script and make sure it's safe. However, the `--autoconfig`
options make changes to essential system configuration files. Making backups of
`~/.config/openbox/rc.xml` and `~/.config/tint2/tint2rc` files is recommended.*

For more info [check Wiki](https://github.com/nwg-piotr/obhud/wiki/Openbox-HUD-Wiki).

## Credits
I used icons from [numix-gtk-theme](https://www.archlinux.org/packages/community/any/numix-gtk-theme)
by [Numix Project](http://numixproject.org) as the base of the icon set. Thanks!

