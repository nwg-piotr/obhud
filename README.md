# Openbox HUD

This script is intended to simplify assigning 
laptop-specific keys and events to actions and display ~~slightly gnomish~~
graphical messages in [Openbox](http://openbox.org) window manager. 
This way one can, for instance, change volume level or screen brightness,
or switch primary / secondary display and see a graphical confirmation 
by just binding a key to a single command. 
Furthermore - assigning a command in [Tint2](https://gitlab.com/o9000/tint2) 
preferences allows to see alerts concerning the AC and
battery state, and also suspend on critical battery level.

### New in 0.1.8 version

**Timer/Stopwatch added**. Please run `obhud --autoconfig tint2` to add the executor.

### New in 0.1.7 version

**Sound added** to the battery low notification. Launch `obhuh --autoconfig tint2` or just
replace `obhud --battery low` with `obhud --battery LOW` in Tint2 / Battery alert, to hear 
sound before the notification and suspending the system.

![preview](http://nwg.pl/obhud/images/preview1.png)

## Installation

Arch Linux: search the [obhud](https://aur.archlinux.org/packages/obhud) 
package in AUR.

## Quick start

Type `obhud` in terminal to access the menu, which allows to add 
default keybindings to `rc.xml` and commands to `tint2rc` file 
automatically. You'll also find syntax of each command here.

Alternatively you can use the `obhud --autoconfig all` command.

![Terminal](http://nwg.pl/obhud/images/terminal.png)

**CAUTION:** 
*I did my best to test the script and make sure it's safe. However, the `--autoconfig`
options make changes to essential system configuration files. Making backups of
`~/.config/openbox/rc.xml` and `~/.config/tint2/tint2rc` files is recommended.*

For more info [check Wiki](https://github.com/nwg-piotr/obhud/wiki/Openbox-HUD-Wiki).

## Credits
I used icons from [numix-gtk-theme](https://www.archlinux.org/packages/community/any/numix-gtk-theme)
by [Numix Project](http://numixproject.org) as the base of the icon set. Thanks!

