from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pd
from Decrypt_File import *
import pickle
import sys

private_key = loading_pem_file("Private.pem", "123")    # Deserializing the private key and loading
# into memory.

with open("aes_keys.json", "rb") as file:   # Deserializing the AES Key:

    data = file.read()  # Loading encrypted AES Key into memory.
    data_bytes = decrypt_data(private_key, data)    # Decrypting the AES Key with RSA Key.
    print(f"Original Data 'Object': {data_bytes.hex()}\n")
    print(f"Encrypted Data 'Object': {data.hex()}\n\n")
    decrypted_key = pickle.loads(data_bytes)    # Deserializing the AES Key into memory.


print(f"Decrypted Key: {decrypted_key['key'].hex()}")
print(f"Decrypted IV: {decrypted_key['iv'].hex()}\n\n")

encrypted_data = reading_file("Screenshot_2023-11-26_13_31_44_(encrypted).png")    # Loading encrypted data into memory.

cipher = Cipher(    # Creating the cipher object.
    algorithm=algorithms.AES256(key=decrypted_key["key"]),  # Using the decrypted AES Key.
    mode=modes.CBC(initialization_vector=decrypted_key["iv"])   # Using the decrypted Initialization Vector.
)

decryptor = cipher.decryptor()  # Creating the decryption object.

padded_message = decryptor.update(encrypted_data) + decryptor.finalize()    # Decrypting the message, which it's still
# padded.

unpadder = pd.PKCS7(128).unpadder()    # Generating the unpadding object.

decrypted_message = unpadder.update(padded_message) + unpadder.finalize()   # Unpadding the message, generating the full
# decrypted data.

writing_file("Screenshot_2023-11-26_13_31_44_(decrypted).png", decrypted_message)   # Writing the decrypted data
# into the original file.
