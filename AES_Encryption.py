from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import secrets

with open("", "rb") as file:
    data = file.read()

# Encryption:
key = secrets.token_bytes(32)  # Key used for AES256 256 bits (32 bytes).

iv = secrets.token_bytes(16)    # Block size for AES 128 bits (16 bytes).

byted_message = bytes("Hello there, this is a test message", 'utf-8')

padder = padding.PKCS7(128).padder()    # Padding the message for 128 bits, default block size for AES.

message = padder.update(byted_message) + padder.finalize()

algorithm = algorithms.AES256(key)
mode = modes.CBC(iv)

cipher = Cipher(
    algorithm=algorithms.AES256(key=key),   # The algorithm used for the encryption (AES256)
    mode=modes.CBC(initialization_vector=iv)
)
encryptor = cipher.encryptor()

cipher_text = encryptor.update(message) + encryptor.finalize()

with open(, "wb") as file:
    file.write(cipher_text)

print(f"Original Message: {byted_message.decode()}")
print(f"Secret Key: {key.hex()}")
print(f"Initialization Vector: {iv.hex()}")
print(f"Padded Original Message: {message.hex()}")
print(f"Encrypted Message: {cipher_text.hex()}")



# Decrypting:

decryptor = cipher.decryptor()

padded_message = decryptor.update(cipher_text) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()

decrypted_message = unpadder.update(padded_message) + unpadder.finalize()

print(f"Padded Decrypted Message: {padded_message.hex()}")
print(f"Decrypted Message: {decrypted_message.decode()}")
