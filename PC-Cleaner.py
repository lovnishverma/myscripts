import os
import shutil
import ctypes

temp = os.environ['TEMP']
dirs = [temp, "C:\\Windows\\Temp", "C:\\Windows\\Prefetch", "C:\\$Recycle.Bin"]

for d in dirs:
    try:
        shutil.rmtree(d, ignore_errors=True)
        print(f"Cleaned: {d}")
    except Exception as e:
        print(f"Failed: {d} -> {e}")

ctypes.windll.user32.MessageBoxW(0, "PC cleanup done!", "Cleaner", 1)
# This script cleans up temporary files and directories on a Windows system.
# It removes files from the TEMP directory, Windows Temp, Prefetch, and Recycle Bin.
# It uses the shutil module to remove directories and their contents, and ctypes to show a message box.
# Note: This script requires administrative privileges to delete certain directories.
# It is important to be cautious when running scripts that delete files, as they can lead to data loss if not used properly.
# The script is designed to be run on Windows systems and may not work as intended on other operating systems.
# The script uses the os module to access environment variables and the shutil module to remove directories.
# The script also uses the ctypes module to create a message box to inform the user when the cleanup is complete.
# The script is a simple utility for cleaning up temporary files and directories on a Windows system.
# It is important to ensure that the script is run with the necessary permissions to avoid errors when trying to delete certain directories.
# The script is intended for use by users who want to free up space on their system by removing temporary files.
# The script is a simple and effective way to clean up temporary files and directories on a Windows system.
# The script is designed to be easy to use and does not require any special knowledge or skills to run.
# The script is a useful tool for anyone who wants to keep their system clean and free of unnecessary files.
