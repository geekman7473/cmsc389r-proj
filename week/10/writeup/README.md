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

The key to this challenge is the small keyspace for the "key" found by taking the MD5 hash of the password from command line argument. Since there are only ~65k possible values for the key, there will likewise only be 65k possible values for the "key hash." Assuming that MD5 outputs are roughly equally likely to one another, we should have a 1/65k chance of any given password matching the hash. Repeating this process a few thousand times should get us a match quickly.

The algorithm is thus:
1) Choose a random printable string
2) Takes it's MD5 hash
3) Zero out all but it's high 2 bytes
4) Take the hash of the resulting 16 bytes
5) Compare this to the "key hash" in the file
6) If they don't match, goto #1, else goto #7
7) The random string is a "valid" password. Write it to stdout and exit.

CMSC389R-{k3y5p4c3_2_sm411}

### Part 3 (10 Pts)

In my opinion security through obscurity has little value with regards to internet connected computer systems. Though having the source code available can make the reverse engineering process easier, strong cryptographic methods are mathematically secure, even if you know the exact implementation. For example, if ledger.c had used SHA512 for it's hashing algorithm, and hadn't truncated the hashes output, it would have been computationally intractable to break the encryption. With that said, there is a place for obscurity. For example, in air-gapped systems for government use, there is value in hiding details of your security protocols and procedures from possible nation-state actors, who may be more motivated and capable, than your typical black hats.