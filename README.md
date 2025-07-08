## Objective

This part of the assignment focuses on implementing a multithreaded **producer-consumer pipeline** using the pthread library and analyzing its performance using the `perf` tool.

## Program Overview

### File: `pipeline.c`

- **Functionality**:
  - `N` producer threads each generate 100 random integers and write them to a dedicated buffer.
  - `N` consumer threads each consume 100 integers from their assigned buffer.
- **Design**:
  - Each producer-consumer pair shares a unique buffer.
  - Uses `pthread_mutex_t` and `pthread_cond_t` for synchronization.
  - Prevents race conditions and avoids busy-waiting.
- **Output**:
  - Execution time (in seconds)
  - Throughput (items processed per second)
  - Results are also saved in `performance_results.txt` for analysis

## Compilation Instructions

```bash
gcc pipeline.c -o pipeline -lpthread
```

## Run Instructions

```bash
./pipeline <num_threads>
```

Example:
```bash
./pipeline 4
```

- This launches 4 producer and 4 consumer threads with 4 shared buffers.

---

## Performance Profiling using `perf`

Use the following command to profile the program execution:

```bash
perf stat -e context-switches,cache-references,cache-misses,cpu-migrations ./pipeline 4
```

### Recommended Thread Counts
- Run tests for: `2`, `4`, `8`, `16`, `50`, `100` threads
- Save results for analysis and plotting scalability graphs

---

## Key Performance Metrics

- `context-switches` – Measures overhead of switching between threads
- `cache-references` and `cache-misses` – Evaluate cache efficiency
- `cpu-migrations` – Tracks how often threads move across CPU cores
- Execution time and throughput printed by the program

---

## Learning Outcome

- Understand and implement the producer-consumer paradigm
- Gain hands-on experience with thread synchronization primitives
- Analyze context switches, cache behavior, and system throughput
- Explore scalability and performance trends with increasing concurrency

