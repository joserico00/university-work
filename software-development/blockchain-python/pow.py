import hashlib
import time

max_nonce = 2 ** 32  # 4 billion dont want this to take too long

def proof_of_work(data, target_bits):
    target = '0' * target_bits

    for nonce in range(max_nonce):
        data_nonce = f"{data}{nonce}".encode() 
        hash_result = hashlib.sha256(data_nonce).hexdigest()

        if hash_result[:target_bits] == target:
            print(f"Success with nonce {nonce}")
            print(f"Hash is {hash_result}")
            return (hash_result, nonce)

    print("Failed after {max_nonce} (MAX_NONCE) tries")
    return nonce

if __name__ == '__main__':
    data = "Pizza"
    difficulty_bits = 10  # cambia dificultad
    print(f"Mining the block containing \"{data}\"")
    start_time = time.time()
    new_hash, nonce = proof_of_work(data, difficulty_bits)
    elapsed_time = time.time() - start_time
    print(f"Mined a new block with nonce {nonce} in {elapsed_time} seconds")
