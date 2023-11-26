from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys


def reading_file(filename):    # Opening file to be encrypted and loading its contents into memory.
    """Opening file and reading its contents into memory."""

    with open(filename, "rb") as file:
        data = file.read()

    file.close()

    return data


def writing_files(filename, content):   # Writing encrypted file.
    """Writing the encrypted file."""

    with open(filename, "wb") as file:
        file.write(content)

    file.close()


def loading_pem_file(filename):    # Loading the Public PEM file into memory.
    """Deserializing the Public PEM file."""

    with open(filename, "rb") as public_pem_file:
        public_key = serialization.load_pem_public_key(public_pem_file.read())

    return public_key


def encrypt_data(public_key, data):    # Encrypting the data.
    """Function to encrypt data."""

    encrypted_data = public_key.encrypt(
        plaintext=data,

        # Padding is a way, used in encryption, to extend the cipher text, so it will match the block size of the hash.
        padding=padding.OAEP(  # OAEP (Optimal Asymmetric Encryption Padding) is recommended for RSA encryption.

            # MFG (Mask Generation Function) will create a mask with the same size of the inputted data.
            mgf=padding.MGF1(algorithm=hashes.SHA256()),

            # SHA256 is a hashing algorithm used to create hashes. In this case, a hash is used to authenticate the
            # message, making sure the data is unaltered, therefore, it's reliable.
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_data


def main():

    # The tool requires 3 arguments to process the encryption. But the 4th argument is optional, and it's related to the
    # output file name.
    if len(sys.argv) < 3 or len(sys.argv) > 4:  # Making sure the correct number of arguments was entered.
        print(f"Usage: python3 Encrypt_File.py [File_Name] [Public_Key.pem]\n")
        print(f"OPTIONAL: python3 Encrypt_File.py [File_Name] [Public_Key.pem] [Encrypted_File_Name]\n\n"
              f"ATTENTION!!!\nBy default, the original file will be OVERWRITTEN by the encrypted file")
        exit(1)

    data_tobe_encrypted = reading_file(sys.argv[1])    # Loading the file's content.
    public_key = loading_pem_file(sys.argv[2])  # Loading the public key.
    encrypted_data = encrypt_data(public_key, data_tobe_encrypted)  # Encrypting the file's content.

    if len(sys.argv) == 4:  # If a name for the new output file as provided:

        filename = sys.argv[1].split(".")   # Getting the file's extension.
        file_new_name = f"{sys.argv[3]}.{filename[1]}"  # Adding the new file's name with the extension.

        writing_files(file_new_name, encrypted_data)    # Writing the new encrypted file.

    else:   # If a name for the new output file wasn't provided.

        writing_files(sys.argv[1], encrypted_data)  # Using the name of the original file to write the encrypted file.
        # This will overwrite the original file's content with the new encrypted content.


if __name__ == "__main__":

    main()
