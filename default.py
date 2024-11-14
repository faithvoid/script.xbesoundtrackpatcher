import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("Patch .XBE Soundtrack (E:\ to F:\)", "RunScript(Q:\\scripts\\XBEAudioPatcher\\patcher.py)"),
        ("Unpatch .XBE Soundtrack Location (F:\ to E:\)", "RunScript(Q:\\scripts\\XBEAudioPatcher\\unpatcher.py)"),
        ("View ST.DB", "RunScript(Q:\\scripts\\XBEAudioPatcher\\viewer.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"XBE Soundtrack Patcher", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
