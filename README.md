# Encryption and Decryption of Big Files with Python  

---

This repository contains tools for encrypting and decrypting **any** file using a **hybrid encryption** method, making
use of symmetric *AES 256* and asymmetric *RSA* encryption.  

This repository is an extension of the [Encryption and Decryption with Python][link1] project, portions of the code
from this project were used here. The implementations of the other technics were done by the owner of this repository.  

This project contains the **tools** and a **skill showcase**:

### Tool's functionality, click here: [Tools][tools]  

### Project's showcase, click here: [Showcase][showcase]  

---

### How does it work?  

The project works by using two scripts, one for encrypting the file and the other for decrypting it.  

The process of encryption starts by loading the data-to-be-encrypted into the program memory. After loading the data
into memory, the symmetric and asymmetric keys are generated. For the symmetric encryption, a *key* is generated as a
random 256-bit value and another random 128-bit value is also generated to be used as the *initialization vector*,
necessary for the symmetric encryption.  

The **AES 256** object is then generated using the previously created *key* and *iv* (*initialization vector*), it uses
the **CBC** mode for the encryption. The **padding** object is also generated, it uses **PKCS7** as the padding method. 
After generating the keys and objects for the process, the data is first padded and then encrypted.  

Concluding the process of encryption, the program will encrypt the AES *key* and *iv* and serialize those. First, the
program generates the **RSA keys**. The **private key** is generated using a *public exponent* of 65537 and a *key size*
of 2048. The **public key** is generated as an instance of the previously created private key.  

After being generated, the RSA *public key* is used for encrypting the AES **keys** (**keys** is referencing to the AES
*key* and *iv*). When generating the AES *keys*, both the *key* and *iv* were created as a Python dictionary, which
contained the key and iv identifiers, with the same respective names, and the bytes used for the encryption process, as
the values associated with those identifiers. Therefore, the process of AES *keys* encryption doesn't happen by
encrypting the bytes used as the *key* and *iv*, but it encrypts the Python object which contains those bytes.  

The first step for AES *keys* encryption is to transform the Python object into a byte object. After the conversion, the
object is then encrypted using the RSA *private key* encryption, and the encrypted data is serialized as a *json* file.
The following steps are the serialization of the RSA *keys*, which are serialized using the **PEM** encoding, as a
traditional **OpenSSH** format and using the **AES-256-CBC** as the encryption algorithm for the *private key*.  

The decryption process is much simpler and follows just a few steps. The first one

---

## How to use  

Here will come an explanation on how to use the tools.  

---

## Showcase  

Here will come a showcase for the tools.  

---

## References  

Here will come a list of references.  

[link1]: https://github.com/ItaloHugoMDS/Encryption_and_Decryption_with_Python
[tools]: https://github.com/ItaloHugoMDS/Encryption_and_Decryption_Big_Files_with_Python?tab=readme-ov-file#how-to-use
[showcase]: https://github.com/ItaloHugoMDS/Encryption_and_Decryption_Big_Files_with_Python?tab=readme-ov-file#showcase
