from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import sys


def generate_private_key():    # Generating Private Key.
    """Function to generate a Private Key object."""

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)    # Generating RSA private key.

    return private_key


def generate_public_key(private_key):   # Generating Public Key.
    """Function to generate a Public Key object."""

    public_key = private_key.public_key()   # Generating an RSA public key. A public key needs to be generated based on
    # a private key instance.

    return public_key


def generate_private_pem(password, private_key):    # Generating the private key's PEM object to be serialized.
    """Function to generate a PEM object for Private Key."""

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(f"{password}", "utf-8"))
    )

    return private_pem


def generate_public_pem(public_key):    # Generating the public key's PEM object to be serialized.
    """Function to generate a PEM object for Public Key."""

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_pem


def serialization_pem(filename, pem_key):   # Serializing PEM objects.
    """Function to serialize PEM objects."""

    with open(f"{filename}.pem", "wb") as pem_file:
        pem_file.write(pem_key)

    pem_file.close()


def main():

    if len(sys.argv) != 4:  # Making sure the correct number of arguments was used.
        print("Usage: python3 Generate_Keys.py [Name_of_Private_PEM] [Name_of_Public_PEM] [Private_Key_Password]")
        exit(1)

    private_key = generate_private_key()    # Private key object.
    public_key = generate_public_key(private_key)   # Public key object.

    private_pem = generate_private_pem(sys.argv[3], private_key)    # Private PEM object.
    public_pem = generate_public_pem(public_key)    # Public PEM object.

    serialization_pem(sys.argv[1], private_pem)    # Serializing the Private PEM object.
    serialization_pem(sys.argv[2], public_pem)  # Serializing the Public PEM object.


if __name__ == "__main__":
    main()
