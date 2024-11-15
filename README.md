## XBE Soundtrack Patcher for XBMC
A utility that modifies the hex of .XBE files to read soundtrack files from "F:\TDATA\FFFE000" instead of "E:\TDATA\FFFE000". Includes ST.DB viewer to view contents of each individual ST.DB file. 

## Installation:
- Install script to "Q:\scripts\XBESoundtrackPatcher" (must be installed there as script paths are hardcoded!)

## How to use:
- Run the script
- Select "Copy ST.DB folder (E: to F:)" if you don't already have a soundtrack folder set up on your F:\ partition.
- Select "Patch .XBE Soundtrack (E:\ to F:\)"
- Select the game .xbe you'd like to modify (make sure you're using an extracted copy of the game you're patching, attach.xbe files will not work!)
- Select the folder you'd like to save the modified .xbe in and what name you'd like to save it under.
- ???
- Profit.

## Bugs:
- You tell me.

## Why?
The F:\ partition on most modded Xboxes tends to be much larger than the default E partition, so this is a great way to maximize how many songs you can have at once on your Xbox, or keep different soundtracks seperate with a little modification!

## TODO:
- Ask the user to set a custom directory to load soundtrack files from (as long as it's the same amount of characters, any custom directory should be okay!).
- Test Dual-HDD support (if you'd like to test this yourself, replace "patcher.py" with "patcherdualhdd.py". This will default to the first partition of your secondary HDD.). Requires a dashboard capable of reading from a secondary HDD, like LithiumX, for file management.
- Add write support to ST.DB viewer(?) (trying to figure it out is giving me a migraine so any help is appreciated)

## Credits:
- Sifaw99 on OGXbox for the original documentation of what hex values had to be modified!
- root670 & kickerofbottoms - ST.DB research (the ST.DB viewer script uses a lot of pystdb code!)
