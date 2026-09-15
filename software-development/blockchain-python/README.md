# Blockchain in Python

A minimal proof-of-work blockchain that runs as a Flask HTTP node, plus a standalone SHA-256 nonce-search demo and study notes on blockchain cryptography. The node supports pending transactions, mining with a block reward, returning the chain, registering peer nodes, and resolving conflicts by adopting the longest valid chain.

**Credit:** `blockchain.py` closely follows the structure of the well-known Flask tutorial [*Learn Blockchains by Building One*](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46) by Daniel van Flymen.

## Contents

| File | Description |
|---|---|
| [`blockchain.py`](#blockchainpy) | `Blockchain` class (blocks, SHA-256 hashing, proof of work, chain validation, consensus) and a Flask REST API for one node |
| [`pow.py`](#powpy) | Standalone proof-of-work demo: search for a nonce whose SHA-256 hash starts with a given number of zeros |
| [`blockchain-cryptology-notes.txt`](#blockchain-cryptology-notestxt) | Study notes on hash functions, digital signatures, transactions and consensus mechanisms |

---

## `blockchain.py`

### Block structure

The chain is a Python list of dictionaries, kept in memory. Every block has five fields:

```json
{
  "index": 2,
  "timestamp": 1789443850.649058,
  "transactions": [
    {"sender": "addr-A", "recipient": "addr-B", "amount": 5}
  ],
  "proof": 22653,
  "previous_hash": "981f9205b56ee32675cfd94bea4a17339ccf2153637b55eb027dbc6f6416dd6d"
}
```

| Field | Meaning |
|---|---|
| `index` | Position in the chain, starting at 1 (`len(self.chain) + 1`) |
| `timestamp` | `time.time()` when the block was created (float, in seconds) |
| `transactions` | Pending transactions collected since the previous block |
| `proof` | The number found by proof of work |
| `previous_hash` | SHA-256 hash of the previous block |

The constructor creates a **genesis block** with `previous_hash='1'`, `proof=100` and no transactions.

### Key class members

| Member | What it does |
|---|---|
| `new_transaction(sender, recipient, amount)` | Appends `{sender, recipient, amount}` to `current_transactions` and returns the index of the block that will contain it (`last_block['index'] + 1`) |
| `new_block(proof, previous_hash)` | Builds a block from the pending transactions, clears the pending list, appends the block and returns it |
| `last_block` (property) | `self.chain[-1]` |
| `hash(block)` (static) | `json.dumps(block, sort_keys=True)` encoded to bytes, then `hashlib.sha256(...).hexdigest()`. Sorting the keys means the same block always serializes, and therefore hashes, the same way. |
| `proof_of_work(last_block)` | Tries `proof = 0, 1, 2, …` until `valid_proof` succeeds |
| `valid_proof(last_proof, proof, last_hash)` (static) | Returns `True` if `sha256(f"{last_proof}{proof}{last_hash}")` starts with `"0000"` |
| `valid_chain(chain)` | Checks each block's link and proof against the previous block |
| `register_node(address)` | Adds a peer's `host:port` to the `nodes` set |
| `resolve_conflicts()` | Consensus: replaces the local chain with the longest valid chain found on any peer |

### Hashing and proof of work

1. `proof_of_work` reads the last block's `proof` and computes `last_hash = hash(last_block)`.
2. It increments a candidate `proof` from 0. For each candidate it hashes the string made of the previous proof, the candidate and the previous block's hash, joined together.
3. The first candidate whose hex digest begins with `0000` is accepted. Four hex zeros equal 16 zero bits, so a proof takes about 2¹⁶ = 65,536 hash attempts on average (a local test found `22653` in 0.02 s). The difficulty is fixed in the code.

Because `last_hash` is part of the puzzle, each proof is tied to the entire chain before it. The puzzle does **not** include the new block's own transactions or timestamp. Those are protected only once a later block stores this block's hash in `previous_hash`.

### Chain validation

`valid_chain(chain)` walks the chain from the second block onward. For each block it checks two things:

1. `block['previous_hash']` equals `hash(previous_block)`, so the links are intact.
2. `valid_proof(previous_block['proof'], block['proof'], hash(previous_block))`, so the proof of work is correct.

If any check fails, it returns `False`. It also prints each pair of blocks as debug output. The genesis block itself is not checked, and transactions are not validated: there are no signatures, balances or amount checks. In a local test, changing the genesis block's `proof` made the rest of the chain fail validation.

### Mining and consensus

- **Mining (`GET /mine`):**
  1. Run `proof_of_work` on the last block.
  2. Add a reward transaction with `sender="0"`, `recipient=node_identifier` and `amount=1`. `node_identifier` is a `uuid4` hex string generated when the node starts.
  3. Create the block with `previous_hash = hash(last_block)`.
- **Consensus (`GET /nodes/resolve`):** for each registered peer, send `GET http://{node}/chain`. If the response is `200`, the peer's `length` is greater than the current best, and `valid_chain` accepts the peer's chain, keep it as the candidate. If a candidate was found, replace the local chain with it. This is the longest-valid-chain rule.

### HTTP endpoints

The Flask app defines exactly these routes:

| Method | Path | Request body | Success response |
|---|---|---|---|
| `GET` | `/mine` | none | `200` `{"message": "New Block Forged", "index", "transactions", "proof", "previous_hash"}` |
| `POST` | `/transactions/new` | `{"sender": str, "recipient": str, "amount": number}` | `201` `{"message": "Transaction will be added to Block N"}`; `400 Missing values` if a field is absent |
| `GET` | `/chain` | none | `200` `{"chain": [...], "length": N}` |
| `POST` | `/nodes/register` | `{"nodes": ["http://127.0.0.1:5001", ...]}` | `201` `{"message": "New nodes have been added", "total_nodes": [...]}`; `400` if `nodes` is missing |
| `GET` | `/nodes/resolve` | none | `200` `{"message": "Our chain was replaced", "new_chain": [...]}` or `{"message": "Our chain is authoritative", "chain": [...]}` |

**Command line:** `-p/--port` (default `5000`). The server listens on `0.0.0.0`, which means every network interface, so other machines on the network can reach it.

### Limitations and known issues

- The chain and pending transactions live in memory only and are lost when the process stops.
- No digital signatures, wallets or balance checks. Any client can post a transaction for any sender with any amount.
- **Register peers with a full URL** such as `http://127.0.0.1:5000`. On Python 3.9+, `urlparse("192.168.0.5:5000")` treats the host as the URL scheme, so the "URL without scheme" branch stores only `"5000"`. This was checked on Python 3.9.
- `resolve_conflicts()` calls `requests.get` with no timeout and no exception handling. If a registered peer is unreachable, `/nodes/resolve` fails with an HTTP 500 error.
- `/transactions/new` and `/nodes/register` expect a JSON body with `Content-Type: application/json`. Missing or non-JSON bodies are not handled cleanly.
- The difficulty (four leading hex zeros) is hard-coded in `valid_proof`.

---

## `pow.py`

A standalone demonstration of the brute-force nonce search behind proof-of-work mining.

### How it works

`proof_of_work(data, target_bits)`:
1. Builds the target prefix `'0' * target_bits`.
2. For `nonce` from 0 up to `max_nonce = 2**32`, hashes `f"{data}{nonce}"` with SHA-256.
3. If the hex digest starts with the target prefix, prints the nonce and hash and returns `(hash_result, nonce)`.
4. If the loop finishes without a match, prints a failure message and returns `nonce`.

The main block mines the string `"Pizza"` and prints the nonce and the elapsed time from `time.time()`.

### Difficulty

Despite the parameter name `target_bits`, the comparison counts **hex characters**, and each one is 4 bits. Difficulty `d` therefore needs `4·d` leading zero bits, or about 16ᵈ attempts on average. Time and memory grow as O(16ᵈ) hashes and O(1) space. Measured locally with `data = "Pizza"`:

| `target_bits` | Nonce found | Hash prefix | Time |
|---|---|---|---|
| 1 | 11 | `0024e4d1b63d…` | < 0.01 s |
| 2 | 11 | `0024e4d1b63d…` | < 0.01 s |
| 3 | 7,738 | `0008b361fe25…` | 0.03 s |
| 4 | 17,703 | `0000112bdea1…` | 0.10 s |
| 5 | 2,869,934 | `000009c5d7b0…` | 6.2 s |

For a given input the nonces are always the same. Timings depend on the machine (about 460,000 hashes per second in CPython here).

### Known issues

- The main block sets `difficulty_bits = 10`, which is 40 bits and about 1.1 × 10¹² expected attempts. That is far more than `max_nonce` (about 4.3 × 10⁹), so a run will almost certainly try all 2³² nonces (hours of CPU time) and fail.
- On failure the function returns a bare `nonce` instead of a tuple, so `new_hash, nonce = proof_of_work(...)` raises `TypeError`.
- The failure message is missing its `f` prefix, so it prints the literal text `{max_nonce}`.

## `blockchain-cryptology-notes.txt`

The author's notes, written as a slide outline (some headings repeat or have no body text). They cover:

- **What a blockchain is:** a data structure that records transactions across many computers so that changing one record means changing every block after it. Listed properties: decentralized, immutable, transparent, secure, smart contracts, consensus mechanisms.
- **Hash functions:** map input of any size to a fixed-size digest, and a small change in the input produces a completely different output. Storing each block's hash in the next block links the chain and makes tampering detectable. SHA-256 is used in Bitcoin for addresses, proof of work and transaction verification.
- **Digital signatures:** provide authentication, non-repudiation and integrity. The sender hashes the message and signs it with a private key; the recipient verifies it with the sender's public key.
- **Cryptocurrency transactions:** a sender address, recipient address, amount and signature, broadcast to the network and confirmed by miners.
- **Consensus mechanisms:** agreement on transactions that prevents fraud and double spending. **Proof of Work** is secure but energy-hungry and tends toward centralization. **Proof of Stake** chooses validators by staked holdings; it uses less energy but risks centralization among large holders.

How the notes relate to the code: `blockchain.py` implements hash chaining, SHA-256 proof of work and longest-chain consensus. It does not implement digital signatures or proof of stake.

---

## Requirements

- Python 3.6+ (the code uses f-strings)
- `flask` and `requests` for `blockchain.py`
- `pow.py` uses only the standard library

```bash
pip install flask requests
```

## Usage

### Run a single node

```bash
python3 blockchain.py            # listens on 0.0.0.0:5000
```

```bash
# Queue a transaction
curl -X POST http://localhost:5000/transactions/new \
     -H "Content-Type: application/json" \
     -d '{"sender": "addr-A", "recipient": "addr-B", "amount": 5}'

# Mine a block (includes the queued transaction plus the mining reward)
curl http://localhost:5000/mine

# View the chain
curl http://localhost:5000/chain
```

### Try consensus with two nodes

```bash
python3 blockchain.py -p 5000
python3 blockchain.py -p 5001      # in a second terminal

curl http://localhost:5000/mine    # make node 5000's chain longer
curl http://localhost:5000/mine

curl -X POST http://localhost:5001/nodes/register \
     -H "Content-Type: application/json" \
     -d '{"nodes": ["http://127.0.0.1:5000"]}'

curl http://localhost:5001/nodes/resolve   # "Our chain was replaced"
```

### Proof-of-work demo

Running `python3 pow.py` as written uses difficulty 10 (see known issues). To see results in seconds, call the function with a lower difficulty:

```bash
python3 -c "from pow import proof_of_work; print(proof_of_work('Pizza', 4))"
# Success with nonce 17703
# Hash is 0000112bdea1...
```

## Author

Jose E. Rodriguez Rios
