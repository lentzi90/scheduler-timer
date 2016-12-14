"""
stats.py

Process the data produced by timer.sh by calculating the
medians, max values and min values for each scheduler and thread count

Author: Lennart Jern (ens16ljn@cs.umu.se)
"""

import pandas as pd
import re

def total_stats():
    # The data file names are of the form data<thread count>.csv
    base = "../data/data"
    thread_base = "../data/threads"
    ext = ".csv"
    header = ("Normal", "Batch", "Idle", "FIFO", "Round Robin")
    # Data frames to store the results in
    med = pd.DataFrame(columns=header)
    mx = pd.DataFrame(columns=header)
    mn = pd.DataFrame(columns=header)
    thread_med = pd.DataFrame(columns=header)
    thread_mx = pd.DataFrame(columns=header)
    thread_mn = pd.DataFrame(columns=header)

    # For each number of threads
    for i in range(1,11):
        # Build the file name
        f = base + str(i) + ext
        thr_f = thread_base + str(i) + ext
        # Read the time data
        df = pd.read_csv(f)
        thr_df = pd.read_csv(thr_f)

        # Add data to results
        med.loc[i] = df.median()
        mx.loc[i] = df.max()
        mn.loc[i] = df.min()
        thread_med.loc[i] = thr_df.median()
        thread_mx.loc[i] = thr_df.max()
        thread_mn.loc[i] = thr_df.min()

    # Write everything to files
    med.to_csv("medians" + ext, index_label="Threads", float_format="%.3f")
    mx.to_csv("max" + ext, index_label="Threads", float_format="%.3f")
    mn.to_csv("min" + ext, index_label="Threads", float_format="%.3f")
    thread_med.to_csv("thread_medians" + ext, index_label="Threads", float_format="%.3f")
    thread_mx.to_csv("thread_max" + ext, index_label="Threads", float_format="%.3f")
    thread_mn.to_csv("thread_min" + ext, index_label="Threads", float_format="%.3f")

    # Caclulate range
    rng = mx-mn
    thr_rng = mx-mn
    rng.to_csv("range" + ext, index_label="Threads", float_format="%.3f")
    thr_rng.to_csv("thread_range" + ext, index_label="Threads", float_format="%.3f")



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
    header=("Normal", "Batch", "Idle", "FIFO", "Round Robin")
    # Files to write: thread{}.csv
    # csv_files = [base+str(i)+".csv" for i in threads]

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
    """Get name of file to write data about thread count <threads> to"""
    base = "../data/threads"
    ext = ".csv"
    return base + str(threads) + ext

thread_stats()
total_stats()
