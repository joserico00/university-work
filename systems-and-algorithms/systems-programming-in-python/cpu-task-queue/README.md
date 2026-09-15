# CPU Task Queue

A client–server simulation where clients send CPU jobs over UDP to a server that buffers them in a shared queue protected by a mutex and semaphore. Once the buffer is full, the server processes the jobs and displays the computation time per client ID.

## Usage

```bash
# terminal 1
python3 task_server.py <port>

# terminal 2+ (one per client)
python3 task_client.py <client id> localhost <port>
```

The port must match between the server and its clients.
