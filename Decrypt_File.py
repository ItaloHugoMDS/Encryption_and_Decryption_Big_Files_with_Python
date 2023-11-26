from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys


def reading_file(filename):    # Opening the encrypted file and loading its contents into memory.
    """Opening file and reading its contents into memory."""

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    return encrypted_data


def writing_file(filename, content):    # Writing the decrypted data into a file.
    """Writing the decrypted content"""

    with open(filename, "wb") as file:
        file.write(content)


def loading_pem_file(filename, password):   # Loading the Private Key into memory.
    """Deserializing Private PEM file."""

    with open(filename, "rb") as private_pem_file:
        private_key = serialization.load_pem_private_key(
            data=private_pem_file.read(),
            password=bytes(f"{password}", "utf-8")
        )

    return private_key


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


def main():

    # The tool requires 4 arguments to process the decryption. But the 5th argument is optional, and it's related to the
    # output file name.
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(f"Usage: python3 Decrypt_File.py [File_To_Be_Decrypted] [Private_Key.pem] [Private_Key_Password]\n")
        print(f"OPTIONAL: python3 Decrypt_File.py [File_To_Be_Decrypted] [Private_Key.pem] [Private_Key_Password] "
              f"[Encrypted_File_Name]\n\n"
              f"ATTENTION!!!\nBy default, the original file will be OVERWRITTEN by the decrypted file")
        exit(1)

    data_tobe_decrypted = reading_file(sys.argv[1])    # Loading the encrypted data into memory.
    private_key = loading_pem_file(sys.argv[2], sys.argv[3])    # Loading Private Key into memory.
    decrypted_data = decrypt_data(private_key, data_tobe_decrypted)    # Decrypting the file's content.

    if len(sys.argv) == 5:  # If a name for the new output decrypted file was provided:

        filename = sys.argv[1].split(".")   # Getting the file's extension.
        file_new_name = f"{sys.argv[4]}.{filename[1]}"  # Creating the new name for the file using the original
        # extension.

        writing_file(file_new_name, decrypted_data)    # Writing the decrypted content into a file.

    else:   # If a name for the output file is not provided:

        writing_file(sys.argv[1], decrypted_data)   # Using the file's original name to create the output.


if __name__ == '__main__':

    main()
