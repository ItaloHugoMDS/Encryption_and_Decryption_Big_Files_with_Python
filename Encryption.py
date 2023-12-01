from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pd
from Encrypt_File import *
from Generate_Keys import *
import secrets
import pickle
import sys

aes_key = {    # AES Key.
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

writing_files("Screenshot_2023-11-26_13_31_44_(encrypted).png", encrypted_data)    # Writing the encrypted data
# into a file using the original extension.

private_key = generate_private_key()    # Generating the Private Key object.
public_key = generate_public_key(private_key)   # Generating the Public Key object.

private_pem = generate_private_pem("123", private_key)  # Generating the Private PEM object.
public_pem = generate_public_pem(public_key)    # Generating the Public PEM object.

serialization_pem("Private", private_pem)   # Serializing the Private PEM object.
serialization_pem("Public", public_pem)    # Serializing the Private PEM object.

with open("aes_keys.json", "wb") as aes_key_file:   # Serializing the AES Key.

    data_bytes = pickle.dumps(aes_key)  # Generating a byte object of the AES Key dictionary.
    print(f"Original Data 'Object': {data_bytes.hex()}\n")
    encrypted_aes_key = encrypt_data(public_key, data_bytes)    # Encrypting the AES Key OBJECT. The data is not
    # encrypted but the Python object is.
    print(f"Encrypted Data 'Object': {encrypted_aes_key.hex()}\n\n")
    aes_key_file.write(encrypted_aes_key)   # Writing the encrypted object into a file, serializing the AES Key.

print(f"Original Key: {aes_key['key'].hex()}")
print(f"Original IV: {aes_key['iv'].hex()}\n\n")


def generate_aes_keys():
    """Generating the AES Key and the AES Initiation Vector"""

    aes_key = {  # AES Key.
        "key": secrets.token_bytes(32),  # Key used for AES256 256 bits (32 bytes).
        "iv": secrets.token_bytes(16)
        # Block size for AES 128 bits (16 bytes). The initialization vector needs to be the
        # same size as the block size. The standard block size for AES is 128 bits.
    }

    return aes_key


def padding_data(data_to_be_padded):
    """Padding the data to fit the AES block size"""
    padding_obj = pd.PKCS7(128).padder()  # The padding PKCS7 algorythm requires that the same block size as the
    # encryption algorythm, in this case AES, which has a block size of 128 bits (16 bytes). The "encryptor" method
    # generates the encryption object.

    padded_data = padding_obj.update(data_to_be_padded) + padding_obj.finalize()  # Padding the message so the
    # data-to-be-encrypted will be a multiple of the block size (128 bits - 16 bytes for AES).

    return padded_data


def encrypt_data(data_to_be_encrypted, aes_key, aes_iv):
    """Encrypting the data using AES256 and CBC mode"""
    cipher_obj = Cipher(

        algorithm=algorithms.AES256(key=aes_key),  # The algorithm that will be used for encrypting the message
        # (AES256).
        mode=modes.CBC(initialization_vector=aes_iv)  # The mode which the algorythm is going to be executed. The
        # CBC requires an initialization vector, which for security reasons shouldn't be the same when encrypting
        # anything.

    ).encryptor()  # The "encryptor" method generates the encryption object.

    encrypted_data = cipher_obj.update(data_to_be_encrypted) + cipher_obj.finalize()  # Executing the encryption
    # process.

    return encrypted_data


def generating_rsa_key(private_key_password):
    """Generating and Serializing the RSA Keys to encrypt the AES Key"""
    private_key = generate_private_key()  # Generating the Private Key object.
    public_key = generate_public_key(private_key)  # Generating the Public Key object.

    private_pem = generate_private_pem(private_key_password, private_key)  # Generating the Private PEM object.
    public_pem = generate_public_pem(public_key)  # Generating the Public PEM object.

    serialization_pem("Private", private_pem)  # Serializing the Private PEM object.
    serialization_pem("Public", public_pem)  # Serializing the Private PEM object.

    return private_key, public_key


def serializing_aes_key(filename, rsa_public_key):
    """Encrypting and Serializing the AES Key using RSA encryption"""
    with open("aes_keys.json", "wb") as aes_key_file:  # Serializing the AES Key.

        data_bytes = pickle.dumps(aes_key)  # Generating a byte object of the AES Key dictionary.
        encrypted_aes_key = encrypt_data(public_key, data_bytes)  # Encrypting the AES Key OBJECT. The data is not
        # encrypted but the Python object is.
        aes_key_file.write(encrypted_aes_key)  # Writing the encrypted object into a file, serializing the AES Key.


def main():

    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print(f"Usage: python3 Encryption.py [File_To_Be_Encrypted] [Private_Key_Password]\n\n")
        print(f"OPTIONAL - Usage: python3 Encryption.py [File_To_Be_Encrypted] [RSA_Private_Key_Password] "
              f"[Encrypted_File_Name] [Private_Key_Name] [Public_Key_Name] [AES_Key_File_Name]\n\n")
        print(f"The default values: \n\n"
              f"\t\t[Private_Key_Name] = Private.PEM\n\n"
              f"\t\t[Public_Key_Name] = Public.PEM\n\n"
              f"\t\t[AES_Key_File_Name] = AES_Key.json (Format is not optional)\n\n"
              f"\t\t[Encrypted_File_Name] = Original-file-name.original-extension\n\n"
              f"\t\tATTENTION: If a name for the output file is not provided, the original file will be OVERWRITTEN "
              f"with the encrypted data.")

    aes_key = generate_aes_keys()
    private_key, public_key = generating_rsa_key(sys.argv[2])

    data_to_be_encrypted = reading_file("Screenshot_2023-11-26_13_31_44.png")


if __name__ == "__main__":
    main()
