## XBE Soundtrack Patcher for XBMC
A utility that modifies the hex of .XBE files to read soundtrack files from "F:\TDATA\FFFE000" instead of "E:\TDATA\FFFE000". Includes ST.DB viewer to view contents of each individual ST.DB file. 

## How to use:
- Move "E:\TDATA\FFFE0000" to "F:\TDATA\FFFE0000"
- Run the script
- Select the game .xbe you'd like to modify (ideally you have the game extracted)
- Select the folder you'd like to save the modified .xbe in and what name you'd like to save it under (to avoid replacing default.xbe by default).
- ???
- Profit.

## Bugs:
- You tell me.

## Why?
The F:\ partition on most modded Xboxes tends to be much larger than the default E partition, so this is a great way to maximize how many songs you can have at once on your Xbox, or keep different soundtracks seperate!

## TODO:
- Ask the user to set a custom directory to load soundtrack files from (as long as it's the same amount of characters, any custom directory should be okay!).
- Implement script to automatically move ST.DB files from E to F.
- Implement dual-HDD support for Cerbios users.
- Add write support to ST.DB viewer.

## Credits:
- Sifaw99 on OGXbox for the original documentation of what hex values had to be modified!
- root670 & kickerofbottoms - ST.DB research (the ST.DB viewer script uses a lot of pystdb code!)
