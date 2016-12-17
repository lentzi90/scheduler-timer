"""
stats.py

Process the data produced by timer.sh by calculating the
medians, max values and min values for each scheduler and thread count.
Also collects the data about individual thread times, and produces similar
statistics for them.
Lastly, produces a set of plots describing the data.

Author: Lennart Jern (ens16ljn@cs.umu.se)
"""

import pandas as pd
import re
import matplotlib.pyplot as plt

def total_stats():
    """
    Read the data from files and calculate statistical values and make plots.
    """
    # The data file names are of the form data<thread count>.csv
    base = "../data/data"
    thread_base = "../data/threads"
    ext = ".csv"
    header = ("Normal", "Batch", "Idle", "FIFO", "RR")
    # Data frames to store the results in
    med = pd.DataFrame(columns=header)          # Medians (total runtime)
    mx = pd.DataFrame(columns=header)           # Max (total runtime)
    mn = pd.DataFrame(columns=header)           # Min (total runtime)
    thread_med = pd.DataFrame(columns=header)   # Medians (threads)
    thread_mx = pd.DataFrame(columns=header)    # Max (threads)
    thread_mn = pd.DataFrame(columns=header)    # Min (threads)

    # For each number of threads
    for i in range(1,11):
        # Build the file name
        f = base + str(i) + ext             # Total run times
        thr_f = thread_base + str(i) + ext  # Thread times
        # Read the time data
        df = pd.read_csv(f)
        thr_df = pd.read_csv(thr_f)

        # Calculate some statistical properties
        med.loc[i] = df.median()
        mx.loc[i] = df.max()
        mn.loc[i] = df.min()
        thread_med.loc[i] = thr_df.median()
        thread_mx.loc[i] = thr_df.max()
        thread_mn.loc[i] = thr_df.min()

        # Plot and save some nice figures
        # Density curves for thread count 2, 4, 6 and 8
        if (i == 2 or i == 4 or i == 6 or i == 8):
            ax = thr_df.plot.kde()
            ax.set_xlabel("Time (s)")
            fig = ax.get_figure()
            fig.savefig("density"+str(i)+".pdf")

        # Box plots for all thread counts
        ax = thr_df.plot.box(figsize=(4.5,3))
        ax.set_ylabel("Time (s)")
        fig = ax.get_figure()
        fig.savefig("box"+str(i)+".pdf")


    # Calculate ranges
    rng = mx-mn
    thr_rng = mx-mn

    # Write everything to files
    data_frames = [med, mx, mn, thread_med, thread_mx, thread_mn, rng, thr_rng]
    base = "../data/"
    names = ["medians", "max", "min", "thread_medians", "thread_max",
             "thread_min", "range", "thread_range"]
    for frm, name in zip(data_frames, names):
        frm.to_csv(base+name + ext, index_label="Threads", float_format="%.5f")


def collect_thread_times(file_name):
    """Read thread times from a file."""
    f = open(file_name)
    times = []
    # Regular expression to find floats
    time = re.compile("(\d+\.\d+)")

    for line in f:
        match = time.match(line)

        if (match):
            t = float(match.group(1))
            times.append(t)

    return times


def thread_stats():
    """Collect timing information about all threads and store in csv files"""
    threads = [i for i in range(1, 11)]
    schedulers = ["n", "b", "i", "f", "r"]
    base = "../data/threads"
    ext = ".log"
    header=("Normal", "Batch", "Idle", "FIFO", "RR")

    # Collect all times for one thread count in one file
    for t in threads:
        times = {key: [] for key in schedulers}
        for s in schedulers:
            f = get_file_name(t, s)
            times[s] = collect_thread_times(f)
        # Write to file
        df = pd.DataFrame(times)
        df.to_csv(get_csv_name(t), index=False, header=header)


def get_file_name(threads, scheduler):
    """Get the file name for the data regarding <scheduler> and <threads>"""
    base = "../data/threads"
    ext = ".log"
    return base + str(threads) + scheduler + ext

def get_csv_name(threads):
    """For a specific number of threads: Get name of file to write data to"""
    base = "../data/threads"
    ext = ".csv"
    return base + str(threads) + ext

# Collect thread timings
thread_stats()
# Get statistics and plots
total_stats()
