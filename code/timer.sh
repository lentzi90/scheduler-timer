#!/bin/bash

# A timer script to measure the differences between schedulers/policies
#
# Author: Lennart Jern (ens16ljn@cs.umu.se)

for THREADS in $(seq 1 10)
do
    DATA="Normal,Batch,Idle,FIFO,Round Robin"
    echo "Running with $THREADS threads"
    # Time the commands 10 times
    for i in $(seq 1 10)
    do
        LINE=""
        # For the polices n(ormal) b(atch) and i(dle)
        for POLICY in n b i f r
        do
            # Set policy and number of threads
            FLAGS="-p$POLICY -j$THREADS"
            COMMAND="./work $FLAGS > /dev/null"
            # Run the command and store the time
            t="$(sh -c "TIMEFORMAT='%5R'; time $COMMAND" 2>&1)"
            # Build the line
            if [ "$POLICY" = "n" ]; then
                LINE="$t"
            else
                LINE="$LINE,$t"
            fi
        done
        DATA=$DATA$'\n'$LINE
        # A little progress report
        echo "Run $i done."
    done

    # Write data to a file
    echo "$DATA" > "data$THREADS.csv"

done
