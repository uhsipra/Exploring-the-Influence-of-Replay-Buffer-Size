import csv
import matplotlib.pyplot as plt
import numpy as np
import glob

# values that can/should be changed
file_path = "./good data/*.csv"
png_path = "plot_of_plots.png"

def read_csv(file_path):
    keys = []   # each variation of dbuff/var is a key
    #bins = [[] for _ in range(100)]   # not to be confused with data binning, just a list to collect 100 data points across all of the same dbuff/var rows in a 2d grid
    data_list = []
    data = {}
    first_row = True
    max_bound = -np.inf
    min_bound = np.inf
    for f_in in glob.glob(file_path):
        with open(f_in, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)

            #process rows into dict
            for row in csv_reader:
                # Convert dbuff and var to floats
                if row[0] not in data:
                    data[row[0]] = [[] for _ in row[1:]]

                #Extract values from the rest of the row
                for i, val in enumerate(map(float, row[1:])):
                    #find max and min bounds of the data, for graphs
                    if max_bound < val:
                        max_bound = val
                    if min_bound > val:
                        min_bound = val
                    # Sort bins into list
                    data[row[0]][i].append(val)

    #process stats
    for key in data:
        dbuff, var = map(float, key.split('/'))
        averages = [np.mean(inner_list) for inner_list in data[key]]
        #use 95% confidence interval
        errors = [1.96*np.std(inner_list, ddof=1) / np.sqrt(len(inner_list)) for inner_list in data[key]]

        entry = [dbuff, var, averages, errors]
        data_list.append(entry)

    return data_list, max_bound, min_bound

def unique_sizes(data_list):
    unique_dbuff = set(entry[0] for entry in data_list)
    unique_var = set(entry[1] for entry in data_list)
    return len(unique_dbuff), len(unique_var)

# Example usage:
result_list, max_bound, min_bound = read_csv(file_path)
#min_bound = 0
#for i in result_list:
#    print(i)
# IMPORTANT:
# If you want to swap increasing x-axis and y-axis (dbuff vs var), uncomment line below
# result_list = sorted(result_list, key=lambda x: (x[0], x[1]))

# Find the unique sizes for dbuff and var
num_cols, num_rows = unique_sizes(result_list)

# Create a dynamic grid for subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(4 * num_cols, 4 * num_rows), constrained_layout=True)

# Flatten the axs array for easier indexing
if type(axs) == np.ndarray:
    axs_flat = axs.flatten()
    # Plot each entry in a subplot
    for i, entry in enumerate(result_list):
        # code for how each plot will be constructed
        dbuff, var, values, errors = entry
        x_values = range(1, len(values)*200 + 1, 200)
        axs_flat[i].plot(x_values, values, marker='o', label=f'dbuff={dbuff}, var={var}')   # can change colour by adding (color='gray') to this line
        axs_flat[i].fill_between(x_values, np.array(values) - np.array(errors), np.array(values) + np.array(errors), alpha=0.6, color='gray', label=None)
        axs_flat[i].set_title(f'dbuff={dbuff}, var={var}')
        axs_flat[i].set_xlabel(f'Time-Steps')
        axs_flat[i].set_ylabel('Rewards')
        axs_flat[i].legend().set_visible(False)
        axs_flat[i].set_ylim([min_bound, max_bound])
    # Hide empty subplots if any
    for i in range(len(result_list), len(axs_flat)):
        axs_flat[i].axis('off')
else:
    axs_flat = axs
    dbuff, var, values, errors = result_list[0]
    x_values = range(1, len(values)*200 + 1, 200)
    axs_flat.plot(x_values, values, marker='o', label=f'dbuff={dbuff}, var={var}')   # can change colour by adding (color='gray') to this line
    axs_flat.fill_between(x_values, np.array(values) - np.array(errors), np.array(values) + np.array(errors), alpha=0.6, color='gray', label=None)
    axs_flat.set_title(f'dbuff={dbuff}, var={var}')
    axs_flat.set_xlabel(f'Time-Steps')
    axs_flat.set_ylabel('Rewards')
    axs_flat.legend().set_visible(False)
    axs_flat.set_ylim([min_bound, max_bound])

# Adjust layout and save the figure to a PNG file
plt.tight_layout()
plt.savefig(png_path, bbox_inches='tight')
