#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>        // threading
#include <sys/types.h>      // pid
#include <unistd.h>         // pid
#include <linux/sched.h>    // schduling policies

#define LENGTH 524288
#define NUM_WORKERS 4

typedef struct work_load {
    int nworkers;
    int data_length;
    long *data;
} WorkLoad;

WorkLoad *wl;

void *work(void *data);
void run_workers();
void print_schduler(pid_t pid);
void initialize_grandi(WorkLoad *wl, int start, int stop);
long calculate_sum(WorkLoad *wl, int start, int stop);

int main(int argc, char *argv[]) {

    // Get and print pid
    pid_t pid = getpid();
    printf("pid: %d\n", pid);

    // Set scheduler
    struct sched_param param;
    param.sched_priority = 0;
    //int policy = SCHED_BATCH;
    //int policy = SCHED_IDLE;

    // if (sched_setscheduler(pid, policy, &param) != 0) {
    //     perror("Set scheduler");
    // }

    // Check and print scheduler
    print_schduler(pid);


    // Allocate memory for work load
    wl = malloc(sizeof(WorkLoad));
    // Initialize work load
    wl->nworkers = NUM_WORKERS;
    wl->data_length = LENGTH;
    long data[LENGTH];
    wl->data = data;

    run_workers();

    printf("Done\n");
}

/**
 * work - a silly attempt to calculate the limit of Grandi's series
 * @param  index index to start at
 * @return       nothing
 */
void *work(void *index) {
    printf("Working...\n");
    int start = *(int *)index;
    int stop = start + wl->data_length / wl->nworkers;
    initialize_grandi(wl, start, stop);

    long sum = 0;
    int times = 10000;
    //int times = 1;
    for (int k = 0; k < times; k++) {
        sum = sum + calculate_sum(wl, start, stop);
        if (k == times/2) {
            printf("Half way there...\n");
        }
    }

    long *sump = malloc(sizeof(long));
    if (!sump) {
        perror("malloc");
    }
    *sump = sum;
    return (void *)sump;
}

/**
 * run_workers - start work threads and wait for them to finish
 */
void run_workers() {
    int num = wl->nworkers;
    long total_sum = 0;
    void *tmp_sum = 0;

    // create threads
    pthread_t threads[num];
    int startindex[num];
    int len = LENGTH;
    int i;
    for (i = 0; i < num-1; i++) {
        startindex[i] = i * len / num;
        if (pthread_create(&threads[i], NULL, work, (void *)&startindex[i]) != 0) {
            perror("Could not create thread");
        }
    }
    startindex[i] = i * len / num;
    tmp_sum = work((void *)&startindex[i]);

    total_sum += *(long *)tmp_sum;
    free(tmp_sum);

    // Join the threads
    for (int i = 0; i < num-1; i++) {
        pthread_join(threads[i], &tmp_sum);
        total_sum += *(long *)tmp_sum;
        free(tmp_sum);
    }

    printf("Sum is %d\n", total_sum);
}

/**
 * print_schduler - print the current scheduler
 * @param  pid  the pid of the process
 */
void print_schduler(pid_t pid) {
    int schedlr = sched_getscheduler(pid);

    char *schedlr_name;
    switch (schedlr) {
        case SCHED_NORMAL:
            schedlr_name = "Normal/Other";
            break;
        case SCHED_BATCH:
            schedlr_name = "Batch";
            break;
        case SCHED_IDLE:
            schedlr_name = "Idle";
            break;
        case SCHED_FIFO:
            schedlr_name = "FIFO";
            break;
        case SCHED_RR:
            schedlr_name = "RR";
            break;
        case SCHED_DEADLINE:
            schedlr_name = "Deadline";
            break;
        default:
            schedlr_name = "Unknown";
    }
    printf("Scheduler: %s\n", schedlr_name);
}

void initialize_grandi(WorkLoad *wl, int start, int stop) {
    for (int i = start; i < stop; i++) {
        if (i % 2 == 0) {
            wl->data[i] = 1;
        } else {
            wl->data[i] = -1;
        }
    }
}


long calculate_sum(WorkLoad *wl, int start, int stop) {
    long sum = 0;

    for (int i = start; i < stop; i++) {
        sum = sum + wl->data[i];
    }
    return sum;
}
