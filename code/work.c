#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>        // threading
#include <sys/types.h>      // pid
#include <unistd.h>         // pid
#include <linux/sched.h>    // schduling policies

#define NUM_WORKERS 4
#define LENGTH 2147483400

typedef struct work_load {
    int nworkers;
    long data_length;
} WorkLoad;

typedef struct work_packet {
    long index;
    long length;
    long result;
} Packet;

WorkLoad *get_work_load();
void *work(void *data);
int get_grandi(int index);
long calculate_sum(long index, long length);
void run_workers(WorkLoad *wl);
void print_schduler();
void set_scheduler(int policy);


int main(int argc, char *argv[]) {

    // Set scheduler
    // int policy = SCHED_BATCH;
    int policy = SCHED_IDLE;
    set_scheduler(policy);

    // Check and print scheduler
    print_schduler();

    WorkLoad *wl = get_work_load();

    printf("Starting workers...\n");
    run_workers(wl);

    free(wl);
    printf("Done\n");
}

WorkLoad *get_work_load() {
    WorkLoad *wl;
    // Allocate memory for work load
    wl = malloc(sizeof(WorkLoad));
    // Initialize work load
    wl->nworkers = NUM_WORKERS;
    // wl->data_length = 1073741824; // 2^30
    wl->data_length = LENGTH;
}

/**
 * work - a silly attempt to calculate the limit of Grandi's series
 * @param  index index to start at
 * @return       nothing
 */
void *work(void *packet) {
    printf("Working...\n");
    Packet *pkt = (Packet *)packet;

    long sum = 0;

    sum = sum + calculate_sum(pkt->index, pkt->length);
}

int get_grandi(int index) {
    if (index % 2 == 0) {
        return 1;
    } else {
        return -1;
    }
}


long calculate_sum(long index, long length) {
    long sum = 0;

    for (int i = index; i < index+length; i++) {
        sum = sum + get_grandi(i);
    }
    return sum;
}

/**
 * run_workers - start work threads and wait for them to finish
 */
void run_workers(WorkLoad *wl) {
    int num = wl->nworkers;
    long total_sum = 0;

    Packet *pkt[num];
    for (int i = 0; i < num; i++) {
        pkt[i] = malloc(sizeof(Packet));
        if (!pkt[i]) {
            perror("malloc");
        }
        pkt[i]->result = 0;
    }

    // create threads
    pthread_t threads[num];
    long len = wl->data_length;
    long p_len = len / num;
    int i;
    for (i = 0; i < num-1; i++) {
        pkt[i]->index = i * len / num;
        pkt[i]->length = p_len;
        if (pthread_create(&threads[i], NULL, work, (void *)pkt[i]) != 0) {
            perror("Could not create thread");
        }
    }
    pkt[i]->index = i * len / num;
    pkt[i]->length = p_len;
    work((void *)pkt[i]);

    total_sum += pkt[i]->result;
    free(pkt[i]);

    // Join the threads
    for (int i = 0; i < num-1; i++) {
        pthread_join(threads[i], NULL);
        total_sum += pkt[i]->result;
        free(pkt[i]);
    }

    printf("Sum is %d\n", total_sum);
}

/**
 * print_schduler - print the current scheduler
 * @param  pid  the pid of the process
 */
void print_schduler() {
    pid_t pid = getpid();
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

void set_scheduler(int policy) {
    struct sched_param param;
    pid_t pid = getpid();
    param.sched_priority = 0;

    if (sched_setscheduler(pid, policy, &param) != 0) {
        perror("Set scheduler");
    }
}
