import csv
import matplotlib.pyplot as plt

def read_csv(file_path):
    data_list = []
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Convert dbuff and var to integers
            dbuff, var = map(int, row[0].split('/'))
            
            # Extract values from the rest of the row
            values = [int(value) for value in row[1:]]
            
            # Create a list with [dbuff, var, values]
            entry = [dbuff, var, values]
            
            # Add the entry to the data_list
            data_list.append(entry)
    
    return data_list

def unique_sizes(data_list):
    unique_dbuff = set(entry[0] for entry in data_list)
    unique_var = set(entry[1] for entry in data_list)
    return len(unique_dbuff), len(unique_var)

# Example usage:
file_path = "results.csv"
result_list = read_csv(file_path)

# Sort result_list based on dbuff and var
result_list = sorted(result_list, key=lambda x: (x[0], x[1]))

# Find the unique sizes for dbuff and var
num_cols, num_rows = unique_sizes(result_list)

# Create a dynamic grid for subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(4 * num_cols, 4 * num_rows), constrained_layout=True)

# Flatten the axs array for easier indexing
axs_flat = axs.flatten()

# Plot each entry in a subplot
for i, entry in enumerate(result_list):
    dbuff, var, values = entry
    x_values = range(1, len(values) + 1)
    axs_flat[i].plot(x_values, values, marker='o', label=f'dbuff={dbuff}, var={var}')
    axs_flat[i].set_title(f'dbuff={dbuff}, var={var}')
    axs_flat[i].set_xlabel('X-axis')
    axs_flat[i].set_ylabel('Y-axis')
    axs_flat[i].legend().set_visible(False)

# Hide empty subplots if any
for i in range(len(result_list), len(axs_flat)):
    axs_flat[i].axis('off')

# Adjust layout and save the figure to a PNG file
plt.tight_layout()
plt.savefig("plot_of_plots.png", bbox_inches='tight')
