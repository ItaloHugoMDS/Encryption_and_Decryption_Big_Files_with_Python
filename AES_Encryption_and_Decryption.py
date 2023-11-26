from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
import secrets

with open("Screenshot_2023-11-26_13_31_44.png", "rb") as file:
    data = file.read()

aes_key = {
    "key": secrets.token_bytes(32),
    "iv": secrets.token_bytes(16)
}

# Encryption:
key = secrets.token_bytes(32)  # Key used for AES256 256 bits (32 bytes).

iv = secrets.token_bytes(16)    # Block size for AES 128 bits (16 bytes).

byted_message = bytes("Hello there, this is a test message", 'utf-8')

padder = padding.PKCS7(128).padder()    # Padding the message for 128 bits, default block size for AES.

message = padder.update(data) + padder.finalize()

cipher = Cipher(
    algorithm=algorithms.AES256(key=aes_key["key"]),   # The algorithm used for the encryption (AES256)
    mode=modes.CBC(initialization_vector=aes_key["iv"])
)
encryptor = cipher.encryptor()

cipher_text = encryptor.update(message) + encryptor.finalize()

with open("Screenshot_2023-11-26_13_31_44_(encrypted).png", "wb") as file:
    file.write(cipher_text)

#print(f"Original Message: {byted_message.decode()}")
print(f"Secret Key: {aes_key['key'].hex()}")
print(f"Initialization Vector: {aes_key['iv'].hex()}")
print(f"Padded Original Message: {message.hex()}")
print(f"Encrypted Message: {cipher_text.hex()}")

# Decrypting:

with open("Screenshot_2023-11-26_13_31_44_(encrypted).png", "rb") as file:
    encrypted_data = file.read()

decryptor = cipher.decryptor()

padded_message = decryptor.update(encrypted_data) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()

decrypted_message = unpadder.update(padded_message) + unpadder.finalize()

print(f"Padded Decrypted Message: {padded_message.hex()}")
#print(f"Decrypted Message: {decrypted_message}")

with open("Screenshot_2023-11-26_13_31_44_(decrypted).png", "wb") as file:
    file.write(decrypted_message)
