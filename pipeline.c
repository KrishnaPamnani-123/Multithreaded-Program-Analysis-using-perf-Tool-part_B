#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/time.h>

#define BUFFER_SIZE 100
#define ITEMS_PER_THREAD 100

typedef struct {
    int buffer[BUFFER_SIZE];
    int count;
    pthread_mutex_t mutex;
    pthread_cond_t full, empty;
} SharedBuffer;

void *producer(void *arg) {
    SharedBuffer *buf = (SharedBuffer *)arg;
    for (int i = 0; i < ITEMS_PER_THREAD; i++) {
        int data = rand() % 100;

        pthread_mutex_lock(&buf->mutex);
        while (buf->count == BUFFER_SIZE)
            pthread_cond_wait(&buf->empty, &buf->mutex);

        buf->buffer[buf->count++] = data;
        pthread_cond_signal(&buf->full);
        pthread_mutex_unlock(&buf->mutex);
    }
    return NULL;
}

void *consumer(void *arg) {
    SharedBuffer *buf = (SharedBuffer *)arg;
    for (int i = 0; i < ITEMS_PER_THREAD; i++) {
        pthread_mutex_lock(&buf->mutex);
        while (buf->count == 0)
            pthread_cond_wait(&buf->full, &buf->mutex);

        int data = buf->buffer[--buf->count];
        pthread_cond_signal(&buf->empty);
        pthread_mutex_unlock(&buf->mutex);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <num_threads>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    pthread_t producers[N], consumers[N];
    SharedBuffer buffers[N];

    struct timeval start, end;
    gettimeofday(&start, NULL);

    for (int i = 0; i < N; i++) {
        buffers[i].count = 0;
        pthread_mutex_init(&buffers[i].mutex, NULL);
        pthread_cond_init(&buffers[i].full, NULL);
        pthread_cond_init(&buffers[i].empty, NULL);
    }

    for (int i = 0; i < N; i++) {
        pthread_create(&producers[i], NULL, producer, &buffers[i]);
        pthread_create(&consumers[i], NULL, consumer, &buffers[i]);
    }

    for (int i = 0; i < N; i++) {
        pthread_join(producers[i], NULL);
        pthread_join(consumers[i], NULL);
    }

    gettimeofday(&end, NULL);

    for (int i = 0; i < N; i++) {
        pthread_mutex_destroy(&buffers[i].mutex);
        pthread_cond_destroy(&buffers[i].full);
        pthread_cond_destroy(&buffers[i].empty);
    }

    double execution_time = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1e6;
    int total_items_processed = N * ITEMS_PER_THREAD;
    double throughput = total_items_processed / execution_time;

    printf("Execution Time: %.6f seconds\n", execution_time);
    printf("Throughput: %.2f items/sec\n", throughput);

    // Store results in a text file
    FILE *file = fopen("performance_results.txt", "a");
    if (file) {
        fprintf(file, "%d %f %f\n", N, execution_time, throughput);
        fclose(file);
    } else {
        printf("Error opening file!\n");
    }

    return 0;
}
