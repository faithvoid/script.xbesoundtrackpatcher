import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("Patch .XBE Soundtrack", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\patcher.py)"),
        ("(from E:\TDATA\FFFE000 to F:\TDATA\FFFE000)", ""),
        ("View ST.DB", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\viewer.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"XBE Audio Patcher", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
