import xbmc
import xbmcgui
import os

# Define the exact byte sequences for hex patterns (ASCII encoded paths). Hex patterns are as follows:
# OLD_PATH = \Device\Harddisk1\Partition1\TDATA\FFFE0000\MUSIC\ST.DB
# NEW PATH = \Device\Harddisk0\Partition1\TDATA\FFFE0000\MUSIC\ST.DB

OLD_PATH = b"\x5C\x44\x65\x76\x69\x63\x65\x5C\x48\x61\x72\x64\x64\x69\x73\x6B\x31\x5C\x50\x61\x72\x74\x69\x74\x69\x6F\x6E\x31\x5C\x54\x44\x41\x54\x41\x5C\x46\x46\x46\x45\x30\x30\x30\x30\x5C"
NEW_PATH = b"\x5C\x44\x65\x76\x69\x63\x65\x5C\x48\x61\x72\x64\x64\x69\x73\x6B\x30\x5C\x50\x61\x72\x74\x69\x74\x69\x6F\x6E\x31\x5C\x54\x44\x41\x54\x41\x5C\x46\x46\x46\x45\x30\x30\x30\x30\x5C"


class XBEAudioPatcher:
    def __init__(self):
        self.xbe_file_path = None
        self.save_directory = None
        self.save_filename = None

    def browse_for_file(self):
        # Prompt the user to select an .xbe file
        self.xbe_file_path = xbmcgui.Dialog().browse(1, 'Select .xbe file', 'files', '.xbe')
        if not self.xbe_file_path:
            xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "No file selected.")
            return False
        return True

    def choose_save_location_and_name(self):
        # Prompt user to select a folder for saving the new .xbe file
        self.save_directory = xbmcgui.Dialog().browse(0, 'Select Folder to Save .xbe', 'files')
        if not self.save_directory:
            xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "No save location selected.")
            return False

        # Prompt user for the filename using xbmc.Keyboard
        keyboard = xbmc.Keyboard('', 'Enter filename (without .xbe extension)')
        keyboard.doModal()
        if keyboard.isConfirmed():
            self.save_filename = keyboard.getText()
            if not self.save_filename:
                xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "No filename entered.")
                return False
        else:
            xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "Filename input canceled.")
            return False

        # Combine directory and filename to create full path
        self.save_file_path = os.path.join(self.save_directory, self.save_filename + ".xbe")
        return True

    def replace_hex(self):
        # Ensure an input file is selected
        if not self.xbe_file_path:
            xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "Please select an .xbe file first.")
            return

        try:
            with open(self.xbe_file_path, 'rb') as xbe_file:
                xbe_data = xbe_file.read()

                # Check if OLD_PATH exists in xbe_data
                if OLD_PATH not in xbe_data:
                    xbmcgui.Dialog().ok("Pattern Not Found! (H:\)", "Are you sure this .XBE is patched?")
                    return

                # Perform replacement
                xbe_data = xbe_data.replace(OLD_PATH, NEW_PATH)

                # Write modified data to new file
                with open(self.save_file_path, 'wb') as new_xbe_file:
                    new_xbe_file.write(xbe_data)

                xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "File saved successfully!")

        except Exception as e:
            xbmcgui.Dialog().ok("XBE Soundtrack Patcher", "Error: " + str(e))

    def run(self):
        # Step 1: Ask user to browse for the input file
        if not self.browse_for_file():
            return
        
        # Step 2: Ask user for save location and filename
        if not self.choose_save_location_and_name():
            return
        
        # Step 3: Perform hex replacement and save the modified file
        self.replace_hex()

# Main execution
if __name__ == '__main__':
    editor = XBEAudioPatcher()
    editor.run()
