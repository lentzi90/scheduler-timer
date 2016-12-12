"""
stats.py

Process the data produced by timer.sh by calculating the
medians, max values and min values for each scheduler and thread count

Author: Lennart Jern (ens16ljn@cs.umu.se)
"""

import pandas as pd

# The data file names are of the form data<thread count>.csv
name = "data"
ext = ".csv"
# Data frames to store the results in
medians = pd.DataFrame(columns=("Normal", "Batch", "Idle", "FIFO", "Round Robin"))
mx = pd.DataFrame(columns=("Normal", "Batch", "Idle", "FIFO", "Round Robin"))
mn = pd.DataFrame(columns=("Normal", "Batch", "Idle", "FIFO", "Round Robin"))

# For each number of threads
for i in range(1,11):
    # Build the file name
    f = name + str(i) + ext
    # Read the time data
    df = pd.read_csv(f)

    # Add data to results
    medians.loc[i] = df.median()
    mx.loc[i] = df.max()
    mn.loc[i] = df.min()

# Write everything to files
medians.to_csv("medians" + ext, index_label="Threads", float_format="%.3f")
mx.to_csv("max" + ext, index_label="Threads", float_format="%.3f")
mn.to_csv("min" + ext, index_label="Threads", float_format="%.3f")

spread = mx-mn
spread.to_csv("spread" + ext, index_label="Threads", float_format="%.3f")
