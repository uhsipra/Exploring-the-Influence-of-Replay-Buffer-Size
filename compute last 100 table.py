import csv
import matplotlib.pyplot as plt
import numpy as np
import glob

# values that can/should be changed
file_path = "./good data lunar/*.csv"
png_path = "plot_of_plots.png"

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
        values = []
        for inner_list in data[f"{dbuff}/{var}"]:
            values.extend(inner_list[-10:])

        entry = [dbuff, var, values]
        data_list.append(entry)

    return data_list, max_bound, min_bound

# Example usage:
result_list, max_bound, min_bound = read_csv(file_path)
min_bound = -250

baseline = {}
baseline_error = {}
perf_diff = {}
perf_diff_error = {}


for i, entry in enumerate(result_list):
    dbuff, var, values = entry
    if var == 0:
        baseline[dbuff] = sum(values)/len(values)
        baseline_error[dbuff] = 1.96*(np.std(values)/ np.sqrt(len(values)))
    else:
        if dbuff not in perf_diff:
            perf_diff[dbuff] = {var:sum(values)/len(values)}
            perf_diff_error[dbuff] = {var:1.96*(np.std(values)/ np.sqrt(len(values)))}
        else:
            perf_diff[dbuff][var] = sum(values)/len(values)
            perf_diff_error[dbuff][var] = 1.96*(np.std(values)/ np.sqrt(len(values)))

# process data and output perfromance difference
for b in perf_diff:
    print(f"RB {b}: \n  Baseline perf: {baseline[b]:.1f} - Baseline error: {baseline_error[b]:.1f}")
    for v in perf_diff[b]:
        print(f"  V:{v} - perf: {perf_diff[b][v]:.1f} - perf error: {perf_diff_error[b][v]:.1f} - perf diff: {100*(perf_diff[b][v] - baseline[b])/baseline[b]:.1f} - diff error: {100*(perf_diff_error[b][v] + baseline_error[b])/baseline[b]:.1f}")
