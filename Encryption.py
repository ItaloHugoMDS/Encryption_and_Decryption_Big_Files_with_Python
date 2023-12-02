from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pd
from Encrypt_File import *
from Generate_Keys import *
import secrets
import pickle
import sys

#aes_key = {    # AES Key.
#    "key": secrets.token_bytes(32),    # Key used for AES256 256 bits (32 bytes).
#    "iv": secrets.token_bytes(16)   # Block size for AES 128 bits (16 bytes). The initialization vector needs to be the
#    # same size as the block size. The standard block size for AES is 128 bits.
#}
#
#data_to_be_encrypted = reading_file("Screenshot_2023-11-26_13_31_44.png")
#
#padding_obj = pd.PKCS7(128).padder()    # The padding PKCS7 algorythm requires that the same block size as the
## encryption algorythm, in this case AES, which has a block size of 128 bits (16 bytes). The "encryptor" method
## generates the encryption object.
#
#message = padding_obj.update(data_to_be_encrypted) + padding_obj.finalize()    # Padding the message so the
## data-to-be-encrypted will be a multiple of the block size (128 bits - 16 bytes for AES).
#
#cipher_obj = Cipher(
#
#    algorithm=algorithms.AES256(key=aes_key["key"]),    # The algorithm that will be used for encrypting the message
#    # (AES256).
#    mode=modes.CBC(initialization_vector=aes_key["iv"])    # The mode which the algorythm is going to be executed. The
#    # CBC requires an initialization vector, which for security reasons shouldn't be the same when encrypting anything.
#
#).encryptor()   # The "encryptor" method generates the encryption object.
#
#encrypted_data = cipher_obj.update(message) + cipher_obj.finalize()    # Executing the encryption process.
#
#writing_files("Screenshot_2023-11-26_13_31_44_(encrypted).png", encrypted_data)    # Writing the encrypted data
## into a file using the original extension.
#
#private_key = generate_private_key()    # Generating the Private Key object.
#public_key = generate_public_key(private_key)   # Generating the Public Key object.
#
#private_pem = generate_private_pem("123", private_key)  # Generating the Private PEM object.
#public_pem = generate_public_pem(public_key)    # Generating the Public PEM object.
#
#serialization_pem("Private", private_pem)   # Serializing the Private PEM object.
#serialization_pem("Public", public_pem)    # Serializing the Private PEM object.
#
#with open("aes_keys.json", "wb") as aes_key_file:   # Serializing the AES Key.
#
#    data_bytes = pickle.dumps(aes_key)  # Generating a byte object of the AES Key dictionary.
#    print(f"Original Data 'Object': {data_bytes.hex()}\n")
#    encrypted_aes_key = encrypt_data(public_key, data_bytes)    # Encrypting the AES Key OBJECT. The data is not
#    # encrypted but the Python object is.
#    print(f"Encrypted Data 'Object': {encrypted_aes_key.hex()}\n\n")
#    aes_key_file.write(encrypted_aes_key)   # Writing the encrypted object into a file, serializing the AES Key.
#
#print(f"Original Key: {aes_key['key'].hex()}")
#print(f"Original IV: {aes_key['iv'].hex()}\n\n")


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


def encrypting_data(data_to_be_encrypted, aes_key, aes_iv):
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


def generating_rsa_key(private_key_password, private_key_name="Private", public_key_name="Public"):
    """Generating and Serializing the RSA Keys to encrypt the AES Key"""

    private_key = generate_private_key()  # Generating the Private Key object.
    public_key = generate_public_key(private_key)  # Generating the Public Key object.

    private_pem = generate_private_pem(private_key_password, private_key)  # Generating the Private PEM object.
    public_pem = generate_public_pem(public_key)  # Generating the Public PEM object.

    serialization_pem(private_key_name, private_pem)  # Serializing the Private PEM object.
    serialization_pem(public_key_name, public_pem)  # Serializing the Private PEM object.

    return private_key, public_key


def serializing_aes_key(rsa_public_key, aes_key_object, filename="AES_Keys"):
    """Encrypting and Serializing the AES Key using RSA encryption"""

    with open(f"{filename}.json", "wb") as aes_key_file:  # Serializing the AES Key.

        data_bytes = pickle.dumps(aes_key_object)  # Generating a byte object of the AES Key dictionary.
        encrypted_aes_key = encrypt_data(rsa_public_key, data_bytes)  # Encrypting the AES Key OBJECT. The data is not
        # encrypted but the Python object is.
        aes_key_file.write(encrypted_aes_key)  # Writing the encrypted object into a file, serializing the AES Key.


def main():

    if len(sys.argv) < 3 or len(sys.argv) > 7:  # Ensuring the correct number of arguments was passed.
        print(f"Usage: python3 Encryption.py [File_To_Be_Encrypted] [Private_Key_Password]\n\n")
        print(f"OPTIONAL - Usage: python3 Encryption.py [File_To_Be_Encrypted] [RSA_Private_Key_Password] "
              f"[Encrypted_File_Name] [Private_Key_Name] [Public_Key_Name] [AES_Key_File_Name]\n\n")
        print(f"The default values: \n\n"
              f"\t\t[Private_Key_Name] = Private.PEM (Format is not optional)\n\n"
              f"\t\t[Public_Key_Name] = Public.PEM (Format is not optional)\n\n"
              f"\t\t[AES_Key_File_Name] = AES_Keys.json (Format is not optional)\n\n"
              f"\t\t[Encrypted_File_Name] = Original-file-name.original-extension\n\n"
              f"\t\tATTENTION: If a name for the output file is not provided, the original file will be OVERWRITTEN "
              f"with the encrypted data.")
        exit(1)

    data_to_be_encrypted = reading_file(filename=sys.argv[1])   # Loading the file to be encrypted into program memory.

    aes_keys = generate_aes_keys()  # Generating the AES Key and AES Initialization Vector (AES IV).

    padded_data = padding_data(data_to_be_padded=data_to_be_encrypted)  # Padding the data-to-be-encrypted so it will
    # fit the block size for AES.
    encrypted_data = encrypting_data(data_to_be_encrypted=padded_data, aes_key=aes_keys["key"], aes_iv=aes_keys["iv"])
    # Encrypted padded data using AES256.

    if len(sys.argv) >= 6:    # Checking if the name for the Private and Public key WERE provided:
        _, public_key = generating_rsa_key(
            private_key_password=sys.argv[2],
            private_key_name=sys.argv[4],
            public_key_name=sys.argv[5]
        )

    else:   # If the name for the Private and Public key WEREN'T provided, using the default values:
        _, public_key = generating_rsa_key(private_key_password=sys.argv[2])

    if len(sys.argv) >= 4:    # Checking if a name for the encrypted output file WAS provided:
        filename = sys.argv[1].split(".")
        new_filename = f"{sys.argv[3]}.{filename[1]}"

        writing_files(filename=new_filename, content=encrypted_data)

    else:   # If the name for the encrypted output files WASN'T provided, using the original file name:
        writing_files(filename=sys.argv[1], content=encrypted_data)

    if len(sys.argv) == 7:    # Checking if the name for the AES Key file WAS provided:
        serializing_aes_key(filename=sys.argv[6], rsa_public_key=public_key, aes_key_object=aes_keys)

    else:   # If the name for the AES Key WASN'T provided, using the default name:
        serializing_aes_key(rsa_public_key=public_key, aes_key_object=aes_keys)


if __name__ == "__main__":
    main()
