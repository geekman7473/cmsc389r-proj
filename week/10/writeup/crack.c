#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <openssl/rand.h>

#include "crypto.h"
#include "common.h"

#define LEDGER_FILE "ledger.bin"
#define PERMISSIONS (S_IRUSR | S_IWUSR)

void rand_str(char *dest, size_t length);

int main(int argc, char **argv) {
    struct stat st;
    struct cipher_params params;
    unsigned char *key;
    unsigned char *key_hash;

    if (stat(LEDGER_FILE, &st) == 0) {
        unsigned char fd_key_hash[16], generated_key_hash[16], password_char[17];
        unsigned char *key, *key_hash;
        int ctext_len = st.st_size - 48, ptext_len, i;
        int fd;
        fd = open(LEDGER_FILE, O_RDONLY, PERMISSIONS);

        read(fd, fd_key_hash, 16);
        memset(&password_char, 0, 17);

        do {
            rand_str(password_char, 16);
            key = md5_hash(password_char, 16);
            memset(key+2, 0, 14);
            key_hash = md5_hash(key,2);
        } while (memcmp(fd_key_hash, key_hash, 16) != 0);

        printf("%s", password_char);

    } else {
        die("Ledger doesn't exist!");
    }
}

// Credit to https://stackoverflow.com/questions/15767691/whats-the-c-library-function-to-generate-random-string
void rand_str(char *dest, size_t length) {
    char charset[] = "0123456789"
                     "abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    while (length-- > 0) {
        size_t index = (double) rand() / RAND_MAX * (sizeof charset - 1);
        *dest++ = charset[index];
    }
    *dest = '\0';
}