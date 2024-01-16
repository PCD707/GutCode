"""
The purpose of this script is to compare empirical and simulated data. 
It plots scatterplots to visualize the correspondence between these two datasets.
It's important to note that the simulated data must be downsampled to match the empirical data's size.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data files
empirical_data_path = r'C:\Users\Darren\Desktop\CODE\FASTDM\empirical_data.csv'
simulated_data_path = r'C:\Users\Darren\Desktop\CODE\FASTDM\simulated_data.csv'

empirical_data = pd.read_csv(empirical_data_path)
simulated_data = pd.read_csv(simulated_data_path)

# Rename 'Session' and 'Group' columns
empirical_data.rename(columns={'session': 'Session', 'group': 'Group'}, inplace=True)
simulated_data.rename(columns={'session': 'Session', 'group': 'Group'}, inplace=True)

# Function to calculate the percentage of correct responses
def calculate_percent_correct(data):
    percent_correct = data.groupby(['subject', 'Group', 'Session'])['response'].apply(lambda x: (x.sum() / len(x)) * 100)
    return percent_correct.reset_index()

# Function to plot scatter plot on a given axes
def plot_scatter(ax, data, x_col, y_col, x_label, y_label):
    sns.scatterplot(data=data, x=x_col, y=y_col, hue='Session', style='Group', s=150, ax=ax)
    ax.plot([0, 100], [0, 100], linestyle='--', color='gray')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(title='Group/Session', loc='center left')

# Calculate the RT quantiles for both datasets
quantiles_empirical = empirical_data['RT'].quantile([0.25, 0.5, 0.75])
quantiles_simulated = simulated_data['RT'].quantile([0.25, 0.5, 0.75])

# Calculate the percent correct for both datasets
empirical_percent_correct = calculate_percent_correct(empirical_data)
simulated_percent_correct = calculate_percent_correct(simulated_data)
merged_data = pd.merge(empirical_percent_correct, simulated_percent_correct, 
                       on=['subject', 'Group', 'Session'], suffixes=('_empirical', '_simulated'))

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# Overall percent correct scatterplot
plot_scatter(axs[0, 0], merged_data, 'response_empirical', 'response_simulated', 'Empirical Data (% Correct)', 'Simulated Data (% Correct)')

# Scatterplots for each quantile
for i, q in enumerate([0.25, 0.5, 0.75]):
    quantile_start_empirical = quantiles_empirical[q-0.25] if q > 0.25 else empirical_data['RT'].min()
    quantile_end_empirical = quantiles_empirical[q]
    quantile_start_simulated = quantiles_simulated[q-0.25] if q > 0.25 else simulated_data['RT'].min()
    quantile_end_simulated = quantiles_simulated[q]

    empirical_q_percent_correct = calculate_percent_correct_in_quantile(empirical_data, quantile_start_empirical, quantile_end_empirical)
    simulated_q_percent_correct = calculate_percent_correct_in_quantile(simulated_data, quantile_start_simulated, quantile_end_simulated)
    merged_q_data = pd.merge(empirical_q_percent_correct, simulated_q_percent_correct, 
                             on=['subject', 'Group', 'Session'], suffixes=('_empirical', '_simulated'))
    
    ax_index = (i + 1) // 2, (i + 1) % 2
    x_label = f'Empirical Data (% Correct) - {int(q*100)}% Quantile'
    y_label = f'Simulated Data (% Correct) - {int(q*100)}% Quantile'
    plot_scatter(axs[ax_index], merged_q_data, 'response_empirical', 'response_simulated', x_label, y_label)

plt.tight_layout()
plt.show()
