import csv
import matplotlib.pyplot as plt
import numpy as np

# values that can/should be changed
file_path = "LunarLander-v2-seed11-batch64.csv"
png_path = "plot_of_plots.png"

def read_csv(file_path):
    keys = []   # each variation of dbuff/var is a key
    #bins = [[] for _ in range(100)]   # not to be confused with data binning, just a list to collect 100 data points across all of the same dbuff/var rows in a 2d grid
    data_list = []
    first_row = True
    max_bound = -np.inf
    min_bound = np.inf
    
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        total_rows = sum(1 for _ in csv_reader)  # Count total rows
        
        # Reset reader to the beginning
        csvfile.seek(0)
        
        for row_num, row in enumerate(csv_reader, start=1):
            # Convert dbuff and var to floats
            dbuff, var = map(float, row[0].split('/'))
            
            key = (dbuff, var)
            if key not in keys:
                if not first_row:
                    dbuff2, var2 = keys[-1]
                    keys.append(key)
                    
                    averages = [np.mean(inner_list) for inner_list in bins]
                    errors = [np.std(inner_list, ddof=1) / np.sqrt(len(inner_list)) for inner_list in bins]

                    entry = [dbuff2, var2, averages, errors]
                    data_list.append(entry)
                else:
                    first_row = False
                    keys.append(key)
                bins = [[] for _ in range(100)]
            
            # Extract values from the rest of the row
            values = [float(value) for value in row[1:]]
            bin_num = 0
            for val in values:
                #find max and min bounds of the data, for graphs
                if max_bound < val:
                    max_bound = val
                if min_bound > val:
                    min_bound = val
                # Sort bins into list
                bins[bin_num].append(val)
                bin_num += 1
            
            # Check if the current row is the last row
            is_last_row = row_num == total_rows
            if is_last_row:
                averages = [np.mean(inner_list) for inner_list in bins]
                errors = [np.std(inner_list, ddof=1) / np.sqrt(len(inner_list)) for inner_list in bins]

                entry = [dbuff, var, averages, errors]
                data_list.append(entry)

    return data_list, max_bound, min_bound

def unique_sizes(data_list):
    unique_dbuff = set(entry[0] for entry in data_list)
    unique_var = set(entry[1] for entry in data_list)
    return len(unique_dbuff), len(unique_var)

# Example usage:
result_list, max_bound, min_bound = read_csv(file_path)
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
axs_flat = axs.flatten()

# Plot each entry in a subplot
for i, entry in enumerate(result_list):
    # code for how each plot will be constructed
    dbuff, var, values, errors = entry
    x_values = range(1, len(values) + 1)
    axs_flat[i].plot(x_values, values, marker='o', label=f'dbuff={dbuff}, var={var}')   # can change colour by adding (color='gray') to this line
    axs_flat[i].fill_between(x_values, np.array(values) - np.array(errors), np.array(values) + np.array(errors), alpha=0.6, color='gray', label=None)
    axs_flat[i].set_title(f'dbuff={dbuff}, var={var}')
    axs_flat[i].set_xlabel(f'Time-Steps/Frames (100)')
    axs_flat[i].set_ylabel('Rewards')
    axs_flat[i].legend().set_visible(False)
    axs_flat[i].set_ylim([min_bound, max_bound])

# Hide empty subplots if any
for i in range(len(result_list), len(axs_flat)):
    axs_flat[i].axis('off')

# Adjust layout and save the figure to a PNG file
plt.tight_layout()
plt.savefig(png_path, bbox_inches='tight')
