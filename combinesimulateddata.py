"""
This script is for combining multiple .dat files (simulation outputs) from selected folders into a single file for easier management and analysis.
"""


import os
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog

def combine_dat_files(folders, output_file_path):
    with open(output_file_path, 'wb') as outfile:  # Open the output file once
        for folder in folders:
            for dat_file in Path(folder).rglob('*.dat'):
                with open(dat_file, 'rb') as infile:  # Open each input file
                    shutil.copyfileobj(infile, outfile)  # Efficiently copy the contents

# Set up the root tkinter window
root = tk.Tk()
root.attributes('-topmost', True)
root.withdraw()

# Function to select folders repeatedly
def select_folders():
    folders = []
    while True:
        folder = filedialog.askdirectory(title="Select a folder containing .dat files, Cancel to stop")
        if folder:
            folders.append(folder)
        else:
            break
    return folders

selected_folders = select_folders()

if selected_folders:
    output_file_path = filedialog.asksaveasfilename(defaultextension=".dat", filetypes=[("DAT files", "*.dat")], title="Save combined file as")
    if output_file_path:
        combine_dat_files(selected_folders, output_file_path)
        print(f"All .dat files have been combined into {output_file_path}")
    else:
        print("No output file selected.")
else:
    print("No folders were selected.")

root.destroy()
