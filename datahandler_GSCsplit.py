"""
This script is designed to handle and manipulate datasets, specifically for splitting a raw dataset by group > session > condition > participant.
"""


import pandas as pd
from pathlib import Path

class DatasetHandler:
    def __init__(self, file_path, columns_to_keep):
        self.file_path = file_path
        self.columns_to_keep = columns_to_keep
        self.dataset = None
    
    def load_csv_dataset(self):
        try:
            self.dataset = pd.read_csv(self.file_path)
            print(f"Dataset loaded successfully from {self.file_path}")
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist.")
        except pd.errors.EmptyDataError:
            print(f"The file {self.file_path} is empty.")
        except pd.errors.ParserError:
            print(f"The file {self.file_path} does not appear to be a valid CSV file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def filter_columns(self):
        if self.dataset is not None:
            try:
                self.dataset = self.dataset[self.columns_to_keep]
                print("Columns filtered successfully.")
            except KeyError as e:
                print(f"One or more columns not found in the dataset: {e}")

    def replace_spaces_in_clusters(self):
        if self.dataset is not None:
            self.dataset['CLUSTERS'] = self.dataset['CLUSTERS'].str.replace(' ', '_', regex=False)
            print("Replaced spaces with underscores in 'CLUSTERS' column.")

    def save_as_txt(self, dataframe, file_path):
        with open(file_path, 'w') as f:
            f.write('#' + '\t'.join(dataframe.columns) + '\n')
            dataframe.to_csv(f, sep='\t', index=False, header=False)

    def split_by_group_session_condition_and_save(self, subj_column, group_column, session_column, condition_column, base_output_dir):
        if self.dataset is not None:
            base_output_path = Path(base_output_dir)
            base_output_path.mkdir(exist_ok=True)
            for group_name, group_df in self.dataset.groupby(group_column):
                group_path = base_output_path / group_name.lower()
                group_path.mkdir(exist_ok=True)
                
                for session_name, session_df in group_df.groupby(session_column):
                    session_path = group_path / f'session {session_name}'
                    session_path.mkdir(exist_ok=True)

                    for condition_name, condition_df in session_df.groupby(condition_column):
                        condition_path = session_path / condition_name.lower()
                        condition_path.mkdir(exist_ok=True)
                    
                        for subj_name, subj_df in condition_df.groupby(subj_column):
                            subj_number = subj_name.strip('PT')
                            filename = condition_path / f'pt_{subj_number}.txt' # change suffic (.txt, .csv, .dat) to save different file type
                            self.save_as_txt(subj_df, filename)
                            print(f"Saved {subj_column} {subj_name} dataset to {filename}")
        else:
            print("No dataset to split. Please ensure the dataset is loaded and filtered correctly.")

# Usage
file_path = r"C:\Users\Darren\Desktop\CODE\FASTDM\raw_corrected.csv"  # Replace with your CSV file path
columns_to_keep = ['subj_idx', 'SESSION', 'CONDITION', 'GROUP', 'CLUSTERS', 'RISK', 'HEV', 'RESPONSE', 'TIME']

handler = DatasetHandler(file_path, columns_to_keep)
handler.load_csv_dataset()
handler.filter_columns()
handler.replace_spaces_in_clusters()
handler.split_by_group_session_condition_and_save('subj_idx', 'GROUP', 'SESSION', 'CONDITION', 'datasets') #first 4 are column handles, last is name of parent folder
