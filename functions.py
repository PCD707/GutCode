# -*- coding: utf-8 -*-
"""
Script for pre-processing functions. Handles tasks such as checking for missing values, analyzing response distributions, and generating various plots.
"""

import os
import copy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog



def check_missing_values(dataset):
    for key, df in dataset.items():
        missing_values = df.isna().sum()

        if missing_values.sum() > 0:
            print(f"Missing values found in dataset -'{key}':")
            print(missing_values[missing_values > 0])
        else:
            print(f"No missing values found in dataset -'{key}'.")


def print_column_length(dataset, column_name):
    for key, df in dataset.items():
        column_length = len(df[column_name])
        print(f"Length of column '{column_name}' in dataset -'{key}': {column_length}")


def count_response_values(datasets):
    value_counts = {}

    for key, data in datasets.items():
        counts = data['response'].value_counts()
        value_counts[key] = {
            '0': counts.get(0, 0),
            '0.25': counts.get(0.25, 0),
            '0.5': counts.get(0.5, 0),
            '0.75': counts.get(0.75, 0),
            '1': counts.get(1, 0)
        }

    return value_counts

def remove_z_outliers(dataset, threshold=3):
    z_dataset = copy.deepcopy(dataset)
    
    for key, df in dataset.items():
       
        # Filter based on z-scores
        z_scores = (df['rt'] - df['rt'].mean()) / df['rt'].std()
        z_filtered_data = df[abs(z_scores) <= threshold]
        
        # Further filter based on 'rt' value
        value_filtered_data = z_filtered_data[z_filtered_data['rt'] > 0.1] #filter out trials 100ms and below
        

        # Update the z_dataset with the final filtered data
        z_dataset[key] = value_filtered_data

    return z_dataset

def plot_group_rt(dataset, corr_dataset):
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()

    folder_path = filedialog.askdirectory(title='Select Folder to Save Group RT Histograms')
    plot_histograms_side_by_side(dataset, corr_dataset, folder_path)


def plot_histograms_side_by_side(dataset, corr_dataset, folder_path):
    columns = ['rt']
    for key in dataset:
        if key in corr_dataset:  # Ensures that the same key exists in both datasets
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns

            for i, current_dataset in enumerate([dataset, corr_dataset]):
                df = current_dataset[key]
                correct_choices = df[df['response'] == 1]
                incorrect_choices = df[df['response'] == 0]

                axes[i].hist(correct_choices['rt'], bins='auto', alpha=0.5, label='Correct Choice')
                axes[i].hist(incorrect_choices['rt'], bins='auto', alpha=0.5, label='Incorrect Choice')
                axes[i].set_xlabel('Response Time (s)')
                axes[i].set_ylabel('Frequency')
                axes[i].legend()
                axes[i].spines['top'].set_visible(False)
                axes[i].spines['right'].set_visible(False)
                #axes[i].set_title(f"{'Uncorrected' if i == 0 else 'Corrected'} - {key}")

            plt.tight_layout()

            figure_path = f"{folder_path}/{key}_GroupRTs_Comparison.png"
            
            # Ensure directory exists
            dir_to_create = os.path.dirname(figure_path)
            if not os.path.exists(dir_to_create):
                os.makedirs(dir_to_create)
            
            plt.savefig(figure_path)
            print(f"Successfully saved figure to: {figure_path}")

            plt.show()



def plot_subject_rt(dataset, corr_dataset):
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()

    folder_path = filedialog.askdirectory(title='Select Folder to Save Subject RTs Histograms')
    plot_histogram_for_subject(dataset, folder_path, '- with Outliers')
    plot_histogram_for_subject(corr_dataset, folder_path, '- Corrected')

# this version generates 1 plot for 0 on negative x and 1 on positive x
def plot_histogram_for_subject(datasets, folder_path, suffix):
    for key, data in datasets.items():
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, xlabel='Incorrect vs Correct Choice Response Times (s)', ylabel='Frequency', title=f"Histogram of Response Times {suffix}")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        
        for i, subj_idx in data.groupby('subj_idx'):
            rt_correct = subj_idx[subj_idx['response'] == 1]['rt']
            rt_incorrect = -subj_idx[subj_idx['response'] == 0]['rt']
            
            rt_correct.hist(bins=30, histtype='step', ax=ax)
            rt_incorrect.hist(bins=30, histtype='step', ax=ax)

        plt.grid(None)

        figure_path = f"{folder_path}/{key}_subjectRTs_{suffix}.pdf"

        # Ensure directory exists
        dir_to_create = os.path.dirname(figure_path)
        if not os.path.exists(dir_to_create):
            os.makedirs(dir_to_create)

        plt.savefig(figure_path)
        print(f"Successfully saved figure to: {figure_path}")

        plt.show()


def plot_boxplots(dataset, corr_dataset):
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()

    folder_path = filedialog.askdirectory(title='Select Folder to Save Boxplots')
    plot_boxplots_for_datset(dataset, folder_path, '- with Outliers')
    plot_boxplots_for_datset(corr_dataset, folder_path, '- Corrected')


def plot_boxplots_for_datset(dataset, folder_path, suffix):
    for key, df in dataset.items():
        fig, ax = plt.subplots(figsize=(8, 6))
        data = [df[df['response'] == i]['rt'] for i in [0, 1]]

        ax.boxplot(data, labels=['Incorrect Choice', 'Correct Choice'])
        ax.set_ylabel('Response Time (s)')
        ax.set_title(f'Boxplot of Response Times {suffix}')

        plt.tight_layout()

        figure_path = f"{folder_path}/{key}_Boxplot{suffix}.pdf"
        
        # Ensure directory exists
        dir_to_create = os.path.dirname(figure_path)
        if not os.path.exists(dir_to_create):
            os.makedirs(dir_to_create)
        
        plt.savefig(figure_path)
        print(f"Successfully saved figure to: {figure_path}")

        plt.show()

def plot_violinplots(dataset, corr_dataset):
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()

    folder_path = filedialog.askdirectory(title='Select Folder to Save Violinplots')
    plot_violinplots_for_dataset(dataset, folder_path, '- with Outliers')
    plot_violinplots_for_dataset(corr_dataset, folder_path, '- Corrected')


def plot_violinplots_for_dataset(dataset, folder_path, suffix):
    for key, df in dataset.items():
        fig, ax = plt.subplots(figsize=(8, 6))
        data = [df[df['response'] == i]['rt'] for i in [0, 1]]

        ax.violinplot(data, showmedians=True)
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Incorrect Choices', 'Correct Choices'])
        ax.set_ylabel('Response Time (s)')
        ax.set_title(f'Violinplot of Response Times {suffix}')

        plt.tight_layout()

        figure_path = f"{folder_path}/{key}_Violinplot{suffix}.pdf"
        
        # Ensure directory exists
        dir_to_create = os.path.dirname(figure_path)
        if not os.path.exists(dir_to_create):
            os.makedirs(dir_to_create)
        
        plt.savefig(figure_path)
        print(f"Successfully saved figure to: {figure_path}")

        plt.show()

