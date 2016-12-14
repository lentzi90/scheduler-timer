"""
stats.py

Process the data produced by timer.sh by calculating the
medians, max values and min values for each scheduler and thread count

Author: Lennart Jern (ens16ljn@cs.umu.se)
"""

import pandas as pd
import re
import matplotlib.pyplot as plt

def total_stats():
    # The data file names are of the form data<thread count>.csv
    base = "../data/data"
    thread_base = "../data/threads"
    ext = ".csv"
    header = ("Normal", "Batch", "Idle", "FIFO", "Round Robin")
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

    # Calculate ranges
    rng = mx-mn
    thr_rng = mx-mn

    # Write everything to files
    data_frames = [med, mx, mn, thread_med, thread_mx, thread_mn, rng, thr_rng]
    base = "../data/"
    names = ["medians", "max", "min", "thread_medians", "thread_max", "thread_min", "range", "thread_range"]
    for frm, name in zip(data_frames, names):
        frm.to_csv(base+name + ext, index_label="Threads", float_format="%.5f")

    # Plot
    # ax2 = thr_df["FIFO"].plot.hist(bins=20)
    # fig2 = ax2.get_figure()
    # fig2.savefig('hist.pdf')

    # ax = thr_df.plot.box()
    # fig = ax.get_figure()
    # fig.savefig('box.pdf')

    # ax = thr_df[["Normal", "Idle", "FIFO"]].plot.kde()
    ax = thr_df[["Batch", "Round Robin"]].plot.kde()

    fig = ax.get_figure()
    fig.savefig('test.pdf')



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
