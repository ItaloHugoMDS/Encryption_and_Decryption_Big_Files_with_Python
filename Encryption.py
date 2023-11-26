from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pd
from Encrypt_File import *
from Generate_Keys import *
import secrets
import pickle
import sys

aes_key = {
    "key": secrets.token_bytes(32),    # Key used for AES256 256 bits (32 bytes).
    "iv": secrets.token_bytes(16)   # Block size for AES 128 bits (16 bytes). The initialization vector needs to be the
# same size as the block size. The standard block size for AES is 128 bits.
}

data_to_be_encrypted = reading_file("Screenshot_2023-11-26_13_31_44.png")

padding_obj = pd.PKCS7(128).padder()    # The padding PKCS7 algorythm requires that the same block size as the
# encryption algorythm, in this case AES, which has a block size of 128 bits (16 bytes). The "encryptor" method
# generates the encryption object.

message = padding_obj.update(data_to_be_encrypted) + padding_obj.finalize()    # Padding the message so the
# data-to-be-encrypted will be a multiple of the block size (128 bits - 16 bytes for AES).

cipher_obj = Cipher(

    algorithm=algorithms.AES256(key=aes_key["key"]),    # The algorithm that will be used for encrypting the message
    # (AES256).
    mode=modes.CBC(initialization_vector=aes_key["iv"])    # The mode which the algorythm is going to be executed. The
    # CBC requires an initialization vector, which for security reasons shouldn't be the same when encrypting anything.

).encryptor()   # The "encryptor" method generates the encryption object.

encrypted_data = cipher_obj.update(message) + cipher_obj.finalize()    # Executing the encryption process.

writing_files("Screenshot_2023-11-26_13_31_44_(encrypted).png", encrypted_data)

private_key = generate_private_key()
public_key = generate_public_key(private_key)

private_pem = generate_private_pem("123", private_key)
public_pem = generate_public_pem(public_key)

serialization_pem("Private", private_pem)
serialization_pem("Public", public_pem)

with open("aes_keys.json", "wb") as aes_key_file:

    data_bytes = pickle.dumps(aes_key)
    print(f"Original Data 'Object': {data_bytes}")
    encrypted_aes_key = encrypt_data(public_key, data_bytes)
    print(f"Encrypted Data 'Object': {encrypted_aes_key}\n\n")
    aes_key_file.write(encrypted_aes_key)

print(f"Original Key: {aes_key['key'].hex()}")
print(f"Original IV: {aes_key['iv'].hex()}\n\n")

#def main():
#
#    if len(sys.argv) < 3 or len(sys.argv) > 6:
#        print(f"Usage: python3 Encryption.py [File_To_Be_Encrypted] [Private_Key_Password]\n")
#
#
#if __name__ == "__main__":
#    main()
