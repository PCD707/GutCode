"""
This script is used to convert file types of simulation outputs (from fast-dm software used in R) to a more user-friendly format.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Set up the root tkinter window and hide it
root = tk.Tk()
root.wm_attributes("-topmost", 1)  # Set the window to be always on top
root.withdraw()

# Prompt the user to select the source_directory
source_directory = filedialog.askdirectory(title="Select the folder containing .lst files")
source_directory = Path(source_directory) if source_directory else None

# Proceed if the user selected a directory
if source_directory and source_directory.exists():
    # Iterate through all the .lst files in the directory
    for lst_file in source_directory.glob('*.lst'):
        txt_file_path = lst_file.with_suffix('.txt')  # Change the file extension to .txt
        
        # Read the contents of the .lst file
        with open(lst_file, 'r') as source:
            content = source.read()
        
        # Write the header followed by the original content to the .txt file
        with open(txt_file_path, 'w') as target:
            header = '# RESPONSE\tTIME\n'
            target.write(header + content)  # Prepend the header
            
        print(f'Converted {lst_file.name} to {txt_file_path.name}')

    print("All .lst files have been converted to .txt files with headers.")
else:
    print("No directory selected or the directory does not exist.")
