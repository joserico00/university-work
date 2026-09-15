# Shortest Job First Scheduler

A distributed producer–consumer simulation. Client devices generate compute jobs of random length and send them over UDP to a central compute server, which queues them and runs the shortest job first.

## How it works

- **`client_device.py`**: each device sends a job (`device id` + `job duration`), then waits for the server's acknowledgement before sending the next one.
- **`compute_server.py`** runs two threads that share a job queue:
  - **Producer**: receives jobs from the socket, adds them to the queue, sorts by job length, and acknowledges the device
  - **Consumer**: takes the shortest job and "executes" it by sleeping for its duration
- Access to the shared queue is coordinated with locks and semaphores to avoid race conditions. At the end, the server reports total compute time per device.

## Usage

```bash
# terminal 1
python3 compute_server.py <port>

# terminal 2+ (one per device)
python3 client_device.py <device id> localhost <port>
```
