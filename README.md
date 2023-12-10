# Encryption and Decryption of Big Files with Python  

---

This repository contains tools for encrypting and decrypting **any** file using a **hybrid encryption** method, making
use of symmetric *AES 256* and asymmetric *RSA* encryption.  

This repository is an extension of the [Encryption and Decryption with Python][link1] project, portions of the code
from this project were used here. The implementations of the other technics were done by the owner of this repository.  

This project contains the **tools** and a **skill showcase**:

### Tool's functionality, click here: [Tools][link2]  

### Project's showcase, click here: [Showcase][link3]  

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

Concluding the process of encryption, the program will encrypt the AES key and iv and serialize those. First, the
program generates the **RSA keys**. The **private key** is generated using a *public exponent* of 65537 and a *key size*
of 2048. The **public key** is generated as an instance of the previously created private key.  

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
[link2]: 
[link3]: 
