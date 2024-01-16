# -*- coding: utf-8 -*-

"""
Main script for pre-processing. Calls upon load_data and functions modules.
This script automates the process of selecting a working directory, importing data, 
processing it (including outlier removal and missing value handling), and then visualizing 
the results. It also allows for exporting the processed data to CSV files.
"""

#############
## STARTUP ##
#############

# Import required libraries and modules
import os
import tkinter as tk
from tkinter import filedialog

# Set up a Tkinter root window to prompt the user to select a working directory
def select_working_directory():
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)  # Set the window to be always on top
    root.withdraw()  # Hide the root window
    # Prompt the user to select a folder
    cwd = filedialog.askdirectory(title='Select Working Directory')
    os.chdir(cwd)

select_working_directory()

# Import custom functions and data loading modules
import subdirectory.functions as fn
import subdirectory.load_data as load

# Uncomment the following lines if you need to reload the modules after making changes
# import importlib
# importlib.reload(fn)
# importlib.reload(load)

# Load and preprocess the data
dictionary = load.data_files
datasets = load.datasets

# Process the data: Remove outliers and handle missing values
corr_datasets = fn.remove_z_outliers(datasets)

# Filter out the 'SHAM' condition data
raw_data = datasets["Raw Data Set"]
raw_grouped = raw_data.groupby('CONDITION')

sham_data = raw_grouped.get_group('SHAM')

rawc = corr_datasets["Raw Data Set"]
rawc_grouped = rawc.groupby('CONDITION')

shamc_data = rawc_grouped.get_group('SHAM')

# Re-check and handle outliers and missing values
corr_datasets = fn.remove_z_outliers(datasets)
fn.check_missing_values(datasets)
fn.check_missing_values(corr_datasets)
fn.print_column_length(datasets, 'rt')
fn.print_column_length(corr_datasets, 'rt')
fn.count_response_values(corr_datasets)

# Perform data visualization
fn.plot_group_rt(datasets, corr_datasets)
fn.plot_subject_rt(datasets, corr_datasets)
fn.plot_boxplots(datasets, corr_datasets)
fn.plot_violinplots(datasets, corr_datasets)

# Use corrected dataframes in global namespace and also save as .csv to file
raw_corrected = corr_datasets['Raw Data Set']
raw_corrected.to_csv('raw_corrected.csv')

# Uncomment the following lines to save additional corrected datasets as CSV
# avg_corrected = corr_datasets['Average Data Set']
# avg_corrected.to_csv('avg_corrected.csv')

# session1_corrected = corr_datasets['Session 1 Data']
# session1_corrected.to_csv('session1_corrected_raw.csv')

# session2_corrected = corr_datasets['Session 2 Data']
# session2_corrected.to_csv('session2_corrected_raw.csv')
