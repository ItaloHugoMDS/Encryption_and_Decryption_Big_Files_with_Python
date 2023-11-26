from Decrypt_File import *
import secrets
import pickle

key = secrets.token_bytes(32)    # Key used for AES256 256 bits (32 bytes).
iv = secrets.token_bytes(16)   # Block size for AES 128 bits (16 bytes). The initialization vector needs to be the
# same size as the block size. The standard block size for AES is 128 bits.

aes_key = {'key': key, 'iv': iv}

private_key = loading_pem_file("Private.pem", "123")

with open("aes_keys.json", "rb") as file:

    data = file.read()
    data_bytes = decrypt_data(private_key, data)
    print(f"Original Data 'Object': {data_bytes}")
    print(f"Encrypted Data 'Object': {data}\n\n")
    decrypted_data = pickle.loads(data_bytes)


print(f"Key: {decrypted_data['key'].hex()}")
print(f"IV: {decrypted_data['iv'].hex()}\n\n")
