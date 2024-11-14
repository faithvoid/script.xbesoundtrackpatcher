import xbmc
import xbmcgui
import shutil
import os

# Function to ask the user if they want to copy the folder
def ask_user():
    # Create a dialog box to ask the user for confirmation
    dialog = xbmcgui.Dialog()
    result = dialog.yesno('Copy Soundtrack Folder', 
                          'Would you like to copy your soundtrack folder to F:\?',
                          '', '', 'Yes', 'No')
    return result  # Returns 1 for 'Yes' and 0 for 'No'

# Function to copy the folder
def copy_folder():
    source_path = "E:\\TDATA\\fffe0000"
    destination_path = "F:\\TDATA\\fffe0000"
    
    if not os.path.exists(source_path):
        xbmcgui.Dialog().ok("Error", "Soundtrack folder does not exist!")
        return

    # Make sure the destination directory exists
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    # Attempt to copy the folder
    try:
        # shutil.copytree will copy the entire directory tree
        shutil.copytree(source_path, destination_path)
        xbmcgui.Dialog().ok("Success", "The soundtrack folder was successfully copied to F:\!")
    except Exception as e:
        xbmcgui.Dialog().ok("Error", "Failed to copy the soundtrack folder: " + str(e))

# Main function to control the flow of the script
def main():
    # Ask the user if they want to copy the folder
    user_choice = ask_user()

    if user_choice == 0:  # User selected 'Yes'
        copy_folder()
    else:
        xbmcgui.Dialog().ok("Cancelled", "You chose not to copy the soundtrack folder.")

# Run the script
main()
