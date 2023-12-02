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

encrypted_data = reading_file("Screenshot_2023-11-26_13_31_44.png")    # Loading encrypted data into memory.

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

writing_file("Screenshot_2023-11-26_13_31_44.png", decrypted_message)   # Writing the decrypted data
# into the original file.


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 7:  # Ensuring the correct number of arguments was passed.
        print(f"Usage: python3 Decryption.py [File_To_Be_Decrypted] [Private_Key_Password]\n\n")
        print(f"OPTIONAL - Usage: python3 Decryption.py [File_To_Be_Decrypted] [Private_Key_Password] "
              f"[Decrypted_File_Name] [Private_PEM_File] [AES_Key_File]\n\n")
        print(f"The default values: \n\n"
              f"\t\t[Private_PEM_File] = Private.PEM (If not specified, the program assumes the default name)\n\n"
              f"\t\t[AES_Key_File] = AES_Keys.json (If not specified, the program assumes the default name)\n\n"
              f"\t\t[Decrypted_File_Name] = Original-encrypted-file-name.original-extension\n\n"
              f"\t\tATTENTION: If a name for the output file is not provided, the original file will be OVERWRITTEN "
              f"with the decrypted data.")
        exit(1)


if __name__ == '__main__':
    main()
