#!/bin/bash

DATA="Scheduler,Time (s)"

for p in n b i
do
    COMMANDS=""
    FLAGS="-p$p -j4"
    COMMAND="./work $FLAGS > /dev/null"
    for i in $(seq 1 10)
    do
        COMMANDS="$COMMANDS $COMMAND;"
    done
    /usr/bin/time --format="%e" --output=data-"$p".txt sh -c "$COMMANDS"
    t=`cat data-"$p".txt`
    t=`echo "$t/10" | bc -l`
    LINE="$p,$t"
    DATA=$DATA$'\n'$LINE
done

# rm -f temp.txt
echo "$DATA"
