from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pd
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import pickle
import sys


def decrypt_data(private_key, data):    # Decrypting the file's content
    """Function to decrypting data."""

    decrypted_data = private_key.decrypt(
        ciphertext=data,
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data


def deserialize_aes_key(aes_private_key, aes_keys_file="AES_Keys"):
    """Deserializing the AES Key and AES Initiation Vector"""
    with open(f"{aes_keys_file}.json", "rb") as file:  # Deserializing the AES Key:

        data = file.read()  # Loading encrypted AES Key into memory.
        data_bytes = decrypt_data(aes_private_key, data)  # Decrypting the AES Key with RSA Key.
        decrypted_key = pickle.loads(data_bytes)  # Deserializing the AES Key into memory.

    file.close()

    return decrypted_key


def decrypting_data(data_to_be_decrypted, aes_key, aes_iv):
    """Decrypting the data"""
    cipher = Cipher(  # Creating the cipher object.
        algorithm=algorithms.AES256(key=aes_key),  # Using the decrypted AES Key.
        mode=modes.CBC(initialization_vector=aes_iv)  # Using the decrypted Initialization Vector.
    )

    decryptor = cipher.decryptor()  # Creating the decryption object.

    decrypted_data = decryptor.update(data_to_be_decrypted) + decryptor.finalize()  # Decrypting the message, which it's
    # still padded.

    return decrypted_data


def unpadding_data(data_to_be_unpadded):
    """Unpadding the data"""
    unpadder = pd.PKCS7(128).unpadder()  # Generating the unpadding object.

    unpadded_data = unpadder.update(data_to_be_unpadded) + unpadder.finalize()  # Unpadding the message, generating the
    # full decrypted data.

    return unpadded_data


def writing_file(filename, content):    # Writing the decrypted data into a file.
    """Writing the decrypted content"""

    with open(filename, "wb") as file:
        file.write(content)

    file.close()


def reading_file(filename):    # Opening the encrypted file and loading its contents into memory.
    """Opening file and reading its contents into memory."""

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    file.close()

    return encrypted_data


def loading_pem_file(filename, password):   # Loading the Private Key into memory.
    """Deserializing Private PEM file."""

    with open(f"{filename}.pem", "rb") as private_pem_file:
        private_key = serialization.load_pem_private_key(
            data=private_pem_file.read(),
            password=bytes(f"{password}", "utf-8")
        )

    private_pem_file.close()

    return private_key


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 7:  # Ensuring the correct number of arguments was passed.
        print(f"Usage: python3 decryption.py [File_To_Be_Decrypted] [RSA_Private_Key_Password]\n\n")
        print(f"OPTIONAL - Usage: python3 decryption.py [File_To_Be_Decrypted] [RSA_Private_Key_Password] "
              f"[Decrypted_File_Name] [RSA_Private_PEM_File_Name] [AES_Key_File]\n\n")
        print(f"The default values for the OPTIONALS: \n\n"
              f"\t\t[RSA_Private_PEM_File_Name] = Private.pem (If not specified, the program assumes the default name)\n\n"
              f"\t\t[AES_Key_File] = AES_Keys.json (If not specified, the program assumes the default name)\n\n"
              f"\t\t[Decrypted_File_Name] = Original-encrypted-file-name.original-extension\n\n"
              f"\t\tATTENTION: If a name for the DECRYPTED output file is not provided, the original file will be "
              f"OVERWRITTEN with the decrypted data.")
        exit(1)

    encrypted_data = reading_file(filename=sys.argv[1])  # Loading encrypted data into memory.

    if len(sys.argv) >= 5:  # Verifying if a new name for the RSA Private Key file WAS provided:
        private_key = loading_pem_file(filename=sys.argv[4], password=sys.argv[2])  # Deserializing the private key and
        # loading into memory. Using the name for the Private Key provided as an argument.

    else:   # If a new name for the RSA Private Key file WASN'T provided, using the default name for the file:
        private_key = loading_pem_file(filename="Private", password=sys.argv[2])  # Deserializing the private key
        # and loading into memory. Using the default name for the Private Key.

    if len(sys.argv) >= 6:  # Verifying if a different name was provided for the AES Keys file:
        aes_keys = deserialize_aes_key(aes_private_key=private_key, aes_keys_file=sys.argv[5])   # Deserializing the
        # AES Key using the new name for the AES Keys file.

    else:   # If a different name for the AES Keys file is not provided, using the default name for the AES Keys file:
        aes_keys = deserialize_aes_key(aes_private_key=private_key)    # Deserializing the AES Keys using the default
        # name for the AES Keys file.

    decrypted_data = decrypting_data(   # Decrypting the data.
        data_to_be_decrypted=encrypted_data,
        aes_key=aes_keys["key"],
        aes_iv=aes_keys["iv"]
    )

    unpadded_data = unpadding_data(data_to_be_unpadded=decrypted_data)  # Unpadding the data.

    if len(sys.argv) >= 4:  # Verifying if a name for the decrypted output file WAS provided:
        _, extension = sys.argv[1].split(".")   # Extracting the file extension.
        new_filename = f"{sys.argv[3]}.{extension}"   # Generating the new file name.

        writing_file(filename=new_filename, content=unpadded_data)  # Writing the decrypted data into the new file.

    else:   # If a name for the output file WASN'T provided, using the original encrypted file new to write the
        # decrypted data.
        writing_file(filename=sys.argv[1], content=unpadded_data)  # Writing the decrypted data into the original file.
        # OVERWRITING the contents of the encrypted file.


if __name__ == '__main__':
    main()
