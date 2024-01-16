# -*- coding: utf-8 -*-
"""
This script is used for loading and preprocessing data files for analysis.
It features functions for selecting files, mapping them to dataset names, cleaning the data, and performing initial data checks.
"""
import os
import tkinter as tk
from tkinter import filedialog

import hddm



# Initialization
root = tk.Tk()
root.wm_attributes("-topmost", 1)  # Set the window to be always on top
root.withdraw()  # Hide the root window

# Prompt user to select a folder
directory = filedialog.askdirectory(title='Select Data Folder')

# Datasets mapping
# data_files = {
#     'Full Data Set':'Avg.csv',
#     'Baseline_SPL': 'Both_S1_SPL_Avg.csv', #baseline data, both groups should perform similar
#     'Baseline_SHAM': 'Both_S1_SHAM_Avg.csv', 
#     'Baseline_VMPFC': 'Both_S1_VMPFC_Avg.csv',
#     'Gut_SHAM_WS': 'Prbtc_S1S2_SHAM_Avg.csv', #gut sham data, should show GBA effect overtime
#     'Gut_SHAM_BS': 'Both_S2_SHAM_Avg.csv',
#     'Gut_SPL_WS': 'Prbtc_S1S2_SPL_Avg.csv', #gut spl data, should not interfere with GBA effect
#     'Gut_SPL_BS': 'Both_S2_SPL_Avg.csv',
#     'TMS_preGut': 'Both_S1_SHAMvVMPFC_Avg.csv', #tms_preGut data, should show effect of cTBS on MGT
#     'TMS_postGut': 'Prbtc_S2_SHAMvVMPFC_Avg.csv',#tms_postGut data, should reveal if cTBS successfully killed the GBA effect or not
#     # # Add more key-value pairs as needed
# }

data_files = {
    'Raw Data Set' : 'Raw.csv'
    # 'Average Data Set' : 'Avg.csv',
    # 'Session 1 Data': 'S1_BothGroups_Raw.csv',
    # 'Session 2 Data': 'S2_BothGroups_Raw.csv'
    }

reverse_data_files = {filename: name for name, filename in data_files.items()}

datasets = {}
data_types = {
    "PARTICIPANT": 'str',
    "REP": 'category',
    "SESSIONCOMPLETE": 'category',
    "CONDITION": 'category',
    "GROUP": 'category',
    "CONCLUDED": 'str',
    "CLUSTERS": 'category'
}


for data_name in data_files:
    data_filename = filedialog.askopenfilename(title='Select Data Files')
    base_filename = os.path.basename(data_filename)

    if base_filename in reverse_data_files:
        dataset_name = reverse_data_files[base_filename]
        data = hddm.load_csv(data_filename, dtype=data_types)
        datasets[dataset_name] = data
    else:
        print(f"File '{base_filename}' does not match any dataset name in the mapping.")

# Data cleaning and pre-processing
def filter_data(column_name, values, dataframes):
    for key, df in dataframes.items():
        mask = df[column_name].isin(values)
        dataframes[key] = df.loc[~mask].copy()
        
def remove_columns(columns_to_remove, dataframes):
    """Remove specified columns from given dataframes."""
    for key, df in dataframes.items():
        for col in columns_to_remove:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)
        dataframes[key] = df

filter_data('CONCLUDED', ['DROPOUT'], datasets) #remove all subjects registered as dropouts
filter_data('PARTICIPANT', ['PT0015', 'PT0034', 'PT0053', 'PT0057', 'PT0060', 'PT0062'], datasets) # these subjects removed because of either not fully completing placebo/probiotic protcol or substantial data recording issues

columns_to_remove = ['REP','SESSIONCOMPLETE','NrOfPink','TokenLoc','BettingValuePink',
                     'BettingValueBlue','TRIALCODE','TrialOnset','ResponseTime',
                     'ValidTrial','ProbPink','ProbBlue','TRIAL HANDLE','EVPINK',
                     'EVBLUE','EVDIFF','EV.PICKED','VARPINK','VARBLUE','VARDIFF',
                     'VARPICKED'] #not needed, saves filespace
remove_columns(columns_to_remove, datasets)


column_replacements = {
    'PARTICIPANT': 'subj_idx',
    'NetRT': 'rt',
    'HEVC': 'response'
}

for key, df in datasets.items():
    df.dropna(inplace=True)
    for old_col, new_col in column_replacements.items():
        df.columns = [col.replace(old_col, new_col) for col in df.columns]
    datasets[key] = df



# Variable assignments (if required)

raw_dataset = datasets['Raw Data Set']
# avg_dataset = datasets['Average Data Set']
# session1_data = datasets['Session 1 Data']
# session2_data = datasets['Session 2 Data']
# baseline_sham = datasets['Baseline_SHAM']
# baseline_spl = datasets['Baseline_SPL']
# baseline_vmpfc = datasets['Baseline_VMPFC']
# gut_sham_ws = datasets['Gut_SHAM_WS']
# gut_sham_bs = datasets['Gut_SHAM_BS']
# gut_spl_bs = datasets['Gut_SPL_BS']
# gut_spl_ws = datasets['Gut_SPL_WS']
# tms_pregut = datasets['TMS_preGut']
# tms_postgut = datasets['TMS_postGut']

# Data check
def print_data_info(data_name, dataframe):
    print(f'Info for {data_name} data')
    print(dataframe.head(5))
    print(dataframe.tail(5))


print_data_info('Raw Data Set', raw_dataset)
# print_data_info('Average Data Set', avg_dataset)
# print_data_info('Session 1 Data',session1_data)
# print_data_info('Session 2 Data', session2_data)
# print_data_info('Both Groups S1 - SHAM', baseline_sham)
# print_data_info('Both Groups S1 - SPL', baseline_spl)
# print_data_info('Both Groups S1 - VMPFC', baseline_vmpfc)
# print_data_info('Probiotic S1S2 - SHAM', gut_sham_ws)
# print_data_info('Both Groups S2 - SHAM', gut_sham_bs)
# print_data_info('Probiotic S1S2 - SPL', gut_spl_bs)
# print_data_info('Both Groups S2 - SPL', gut_spl_ws)
# print_data_info('Both Groups S1 - SHAM v VMPFC', tms_pregut)
# print_data_info('Probiotic S2 - SHAM v VMPFC', tms_postgut)


