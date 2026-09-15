# Memory Paging Simulator

Simulates how an operating system handles virtual memory when physical memory is full. Each program reads a sequence of page accesses, keeps a fixed number of frames in memory, and reports page faults and hits.

| Algorithm | How it chooses a page to evict |
|-----------|--------------------------------|
| **FIFO** (`fifo.py`) | The page that has been in memory the longest |
| **Optimal** (`optimal.py`) | The page that won't be needed for the longest time in the future (theoretical best case) |
| **WSClock** (`wsclock.py`) | Circular scan combining the *clock* algorithm with the *working set* model: skips recently referenced pages and pages used within the last `tau` time units |

## Input format

A text file with space-separated accesses, `R:<page>` for reads and `W:<page>` for writes:

```
W:4 R:1 R:6 W:1 R:2 R:5 R:4 W:6 R:3 R:1
```

## Usage

```bash
python3 fifo.py <frames> example_sequence.txt
python3 optimal.py <frames> example_sequence.txt
python3 wsclock.py <frames> <tau> example_sequence.txt
```

Example: with 3 frames on `example_sequence.txt`, Optimal produces 13 page faults, while FIFO and WSClock both produce 19, showing how far practical algorithms are from the theoretical best.
