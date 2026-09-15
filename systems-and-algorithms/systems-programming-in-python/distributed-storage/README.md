# Distributed Storage System

A simplified distributed file system in the style of HDFS / GFS. Files are split into blocks stored across multiple storage nodes, while a central metadata server tracks where every block lives.

## Architecture

```
            ┌────────────────────┐
            │  metadata_server   │  SQLite: files, nodes, block locations
            └─────────▲──────────┘
       register /     │     put / get / list
       block info     │
   ┌──────────────────┼──────────────────┐
   │                  │                  │
┌──┴───────────┐ ┌────┴─────────┐ ┌──────┴───────┐
│ storage_node │ │ storage_node │ │  transfer /  │
│  (blocks)    │ │  (blocks)    │ │  list_files  │
└──────────────┘ └──────────────┘ └──────────────┘
```

| File | Role |
|------|------|
| `metadata_server.py` | Handles `reg`, `put`, `get`, `dblks` (block registration) and `list` commands |
| `storage_node.py` | Registers with the metadata server; stores and returns blocks by UUID |
| `transfer.py` | Copies a file **into** the system (split into blocks across nodes) or **out of** it (reassembled from blocks) |
| `list_files.py` | Lists stored files and sizes |
| `metadata_db.py` | SQLite access layer |
| `packet.py` | JSON message format shared by all components |
| `create_db.py` | Creates an empty metadata database |

## Usage

> Written for **Python 2.7** (`SocketServer`, `print` statements).

```bash
python create_db.py
python metadata_server.py 8000
python storage_node.py localhost 9001 /tmp/node1 8000
python storage_node.py localhost 9002 /tmp/node2 8000

python transfer.py myfile.txt localhost:8000:/remote/myfile.txt     # upload
python list_files.py localhost:8000
python transfer.py localhost:8000:/remote/myfile.txt copy.txt       # download
```

Built on a provided starter framework (message format and database layer); the servers' request handling, block distribution and file transfer logic were implemented by me.
