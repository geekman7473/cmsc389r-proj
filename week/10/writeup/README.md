# Writeup 10 - Crypto I

Name: Justin Becker
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker


## Assignment details

### Part 1 (45 Pts)
1. What is the structure of the ledger file format? Include exact byte offsets when static.
0-15: Key Hash
16-31: Ciphertext Hash
32-47: IV
48 - EOF: Cipher Text

2. What specific cryptographic implementations are used by the program? I.e. not "hashing", but a specific algorithm. Why might this pose a risk?

AES128 and MD5 are used in ledger.c, both of which are known to be weak against modern computers.

3. What information, if any, are you able to derive from [ledger.bin](ledger.bin) without decrypting it at all?

The value of the key, the ciphertext hash, and the IV.

4. How does the application ensure Confidentiality? How is the encryption key derived?

The application ensures Confidentiality by encrypting it's data using AES128. The encryption key is derived by taking the MD5 hash of the password, and then zeroing out all but the two high bytes.

5. How does the application ensure Integrity? Is this flawed in any way?

The application checks that the ciphertext hash from the ledger matches the hash of the contents of the file. This should be a decent enough solution, however it is possible that the ciphertext hash could be corrupted, instead of the ciphertext itself, leaving you with a perfectly intact message.

6. How does the application ensure Authenticity? Is this flawed in any way?

Authenticity is ensured by taking the hash of the inputted password, taking it's hash, taking the first two bytes of the hash, and then hashing it again, and then comparing *that* value with the hash stored in the file. If they match, you're golden. The issue here, is that there's a small keyspace for the 1st hash (due to only take the two high bytes) so you can readily generate hash collisions for the final hash function.

7. How is the initialization vector generated and subsequently stored? Are there any issues with this implementation?

IV is generated using a secure random byte generation function and then is stored in the file unencrypted. I am not certain of this, but I believe that this information should not be left in the clear and could be used for an attack on AES encryption.

### Part 2 (45 Pts)

### Part 3 (10 Pts)

