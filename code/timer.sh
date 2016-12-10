#!/bin/bash

# A timer script to measure the differences between schedulers/policies
#
# Author: Lennart Jern (ens16ljn@cs.umu.se)

# For the polices n(ormal) b(atch) and i(dle)
for p in n b i
do
    # Running with 4 threads/jobs
    FLAGS="-p$p -j4"
    COMMAND="./work $FLAGS > /dev/null"
    DATA="Scheduler,Time (s)"
    # Time the command 10 times
    for i in $(seq 1 10)
    do
        /usr/bin/time --format="%e" --output=data-"$p".txt sh -c "$COMMAND"
        t=`cat data-"$p".txt`
        LINE="$p,$t"
        DATA=$DATA$'\n'$LINE
    done
    # Store data for each policy
    echo "$DATA" > "data-$p.txt"
    # A little progress report
    echo "$COMMAND done."
done
