"""
This script compiles empirical and simulated (downsampled) data into CSV files for further analysis, 
specifically for use with an empsim_scatterplotter module to create model recovery scatterplots.
"""


import pandas as pd
import os
import re

def process_empirical_file(file_path):
    # Read and keep specific columns
    df = pd.read_csv(file_path, delimiter='\s+',
                     usecols=['#subj_idx', 'SESSION', 'GROUP', 'RESPONSE', 'TIME'])

    # Rename columns
    df.rename(columns={'#subj_idx': 'subject', 'SESSION': 'session', 
                       'GROUP': 'group', 'RESPONSE': 'response', 'TIME': 'RT'}, inplace=True)

    # Transform subject and group values
    df['subject'] = df['subject'].apply(lambda x: x.lstrip('PT00').zfill(2))
    df['group'] = df['group'].str.lower()
    df['group'] = df['group'].replace({'probiotics': 'probiotic'})
    # Add type column
    df['type'] = 'E'

    return df

def process_simulated_file(file_path):
    # Extract subject, session, and group from filename
    filename = os.path.basename(file_path)
    subject = re.search('pt_(\d+)', filename).group(1)[-2:]
    session = re.search('s(\d)', filename).group(1)
    group = filename.split('_')[0].lower()

    # Read file with no headers
    df = pd.read_csv(file_path, header=None, names=['response', 'RT'], delimiter='\s+')

    # Add extracted information
    df['subject'] = subject
    df['session'] = session
    df['group'] = group
    df['type'] = 'S'

    return df

def process_empirical_data(empirical_folders):
    empirical_data = []
    for folder in empirical_folders:
        for file in os.listdir(folder):
            if file.endswith('.txt'):
                file_path = os.path.join(folder, file)
                df = process_empirical_file(file_path)
                empirical_data.append(df)
    return pd.concat(empirical_data, ignore_index=True)

def process_simulated_data(simulated_folder):
    simulated_data = []
    for file in os.listdir(simulated_folder):
        if file.endswith('_sim.dat'):
            file_path = os.path.join(simulated_folder, file)
            df = process_simulated_file(file_path)
            simulated_data.append(df)
    simulated_df = pd.concat(simulated_data, ignore_index=True)

    # Downsample the simulated dataframe
    empirical_count = len(empirical_data)
    downsampled_simulated = simulated_df.iloc[::(len(simulated_df) // empirical_count), :].copy()
    downsampled_simulated = downsampled_simulated.iloc[:empirical_count, :]

    return downsampled_simulated

def reorder_columns(df):
    desired_order = ['subject', 'session', 'group', 'type', 'response', 'RT']
    return df[desired_order]

def save_data_to_csv(data, output_path):
    data.to_csv(output_path, index=False)

# Define paths to the data
simulated_folder = r'C:\Users\Darren\Desktop\CODE\FASTDM\models\for compiler code\sim_b0'
empirical_folders = [
    r'C:\Users\Darren\Desktop\CODE\FASTDM\models\for compiler code\emp_b0\placebo_s1',
    r'C:\Users\Darren\Desktop\CODE\FASTDM\models\for compiler code\emp_b0\placebo_s2',
    r'C:\Users\Darren\Desktop\CODE\FASTDM\models\for compiler code\emp_b0\probiotic_s1',
    r'C:\Users\Darren\Desktop\CODE\FASTDM\models\for compiler code\emp_b0\probiotic_s2'
]

# Process empirical and simulated data
empirical_data = process_empirical_data(empirical_folders)
simulated_data = process_simulated_data(simulated_folder)

# Ensure column order matches
empirical_data = reorder_columns(empirical_data)
simulated_data = reorder_columns(simulated_data)

# Save the data to CSV files
empirical_output_path = r'C:\Users\Darren\Desktop\CODE\FASTDM\empirical_data.csv'
simulated_output_path = r'C:\Users\Darren\Desktop\CODE\FASTDM\simulated_data.csv'

save_data_to_csv(empirical_data, empirical_output_path)
save_data_to_csv(simulated_data, simulated_output_path)

# Print out the shapes of the data
print(f"The shape of the empirical data is: {empirical_data.shape}")
print(f"The empirical data is saved to: {empirical_output_path}")
print(f"The shape of the simulated data is: {simulated_data.shape}")
print(f"The simulated data is saved to: {simulated_output_path}")
