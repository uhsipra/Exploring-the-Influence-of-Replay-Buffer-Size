import csv
import matplotlib.pyplot as plt
import numpy as np
import glob

# values that can/should be changed
file_path = "./good data lunar/*.csv"
png_path = "plot_of_plots.png"
group_x = False
group_y = False

def read_csv(file_path):
    keys = []   # each variation of dbuff/var is a key
    #bins = [[] for _ in range(100)]   # not to be confused with data binning, just a list to collect 100 data points across all of the same dbuff/var rows in a 2d grid
    data_list = []
    data = {}
    entries = []
    max_bound = -np.inf
    min_bound = np.inf
    for f_in in glob.glob(file_path):
        with open(f_in, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)

            #process rows into dict
            for row in csv_reader:
                #get key in consistant format
                si = row[0].split('/')
                key = f"{int(si[0])}/{float(si[1])}"
                # Convert dbuff and var to floats
                if key not in data:
                    data[key] = [[] for _ in row[1:]]
                    entries.append([int(si[0]), float(si[1])])

                #Extract values from the rest of the row
                for i, val in enumerate(map(float, row[1:])):
                    #find max and min bounds of the data, for graphs
                    if max_bound < val:
                        max_bound = val
                    if min_bound > val:
                        min_bound = val
                    # Sort bins into list
                    data[key][i].append(val)

    #process stats
    for key in sorted(entries, key=lambda x: x[1]):
        dbuff, var = key
        averages = [np.mean(inner_list) for inner_list in data[f"{dbuff}/{var}"]]
        #use 95% confidence interval
        errors = [1.96*np.std(inner_list, ddof=1) / np.sqrt(len(inner_list)) for inner_list in data[f"{dbuff}/{var}"]]

        entry = [dbuff, var, averages, errors]
        data_list.append(entry)

    return data_list, max_bound, min_bound

def unique_sizes(data_list):
    unique_dbuff = set(entry[0] for entry in data_list)
    unique_var = set(entry[1] for entry in data_list)
    return len(unique_dbuff), len(unique_var)

# Example usage:
result_list, max_bound, min_bound = read_csv(file_path)
min_bound = -250

# Find the unique sizes for dbuff and var
data_num_cols, data_num_rows = unique_sizes(result_list)
if group_x:
    num_cols = 1
else:
    num_cols = data_num_cols
if group_y:
    num_rows = 1
else:
    num_rows = data_num_rows

# Create a dynamic grid for subplots
if group_x:
    fig, axs = plt.subplots(1, num_rows, figsize=(4 * num_rows, 4 * num_cols), constrained_layout=True)
else:
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4 * num_cols, 4 * num_rows), constrained_layout=True)

# Flatten the axs array for easier indexing
if type(axs) == np.ndarray:
    axs_flat = axs.flatten()
    # Plot each entry in a subplot
    for i, entry in enumerate(result_list):
        # code for how each plot will be constructed
        dbuff, var, values, errors = entry
        
        #deal with grouped entries
        plot_label = ""
        line_label = ""
        if group_x:
            i //= data_num_cols
            plot_label +="Replay Buffer: All - "
            line_label +=f"RB: {dbuff}"
        else:
            plot_label +=f"Replay Buffer: {dbuff} - "
        if group_y:
            i %= data_num_rows
            plot_label +="V: All"
            line_label +=f"V: {var}"
        else:
            plot_label +=f"V: {var}"


        x_values = range(1, len(values)*500 + 1, 500)
        axs_flat[i].plot(x_values, values, label=line_label)   # can change colour by adding (color='gray') to this line
        axs_flat[i].fill_between(x_values, np.array(values) - np.array(errors), np.array(values) + np.array(errors), alpha=0.4, label=None)
        axs_flat[i].set_title(plot_label)
        axs_flat[i].set_xlabel(f'Time-Steps')
        axs_flat[i].set_ylabel('Rewards')
        if group_x or group_y:
            axs_flat[i].legend().set_visible(True)
        axs_flat[i].set_ylim([min_bound, max_bound])
    # Hide empty subplots if any
    for i in range(len(result_list), len(axs_flat)):
        axs_flat[i].axis('off')
else:
    axs_flat = axs
    dbuff, var, values, errors = result_list[0]
    x_values = range(1, len(values)*500 + 1, 500)
    axs_flat.plot(x_values, values,label=f'dbuff={dbuff}, var={var}')   # can change colour by adding (color='gray') to this line
    axs_flat.fill_between(x_values, np.array(values) - np.array(errors), np.array(values) + np.array(errors), alpha=0.6, color='gray', label=None)
    axs_flat.set_title(f'dbuff={dbuff}, var={var}')
    axs_flat.set_xlabel(f'Time-Steps')
    axs_flat.set_ylabel('Rewards')
    axs_flat.legend().set_visible(False)
    axs_flat.set_ylim([min_bound, max_bound])

# Adjust layout and save the figure to a PNG file
plt.tight_layout()
plt.savefig(png_path, bbox_inches='tight', dpi=300)
