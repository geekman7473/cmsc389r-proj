#include <stdio.h>
#include <stdlib.h>

#include "common.h"

void dlog(char *msg) {
#if DEBUG
    printf("%s\n", msg);
#endif
}

void die(char *msg) {
    fprintf(stderr, "%s\n", msg);
    exit(-1);
}

void memdump(unsigned char *ptr, size_t n) {
    size_t i;
    for (i = 0; i < n; i++) {
        printf("%2hhx ", ptr[i]);
        if (i && i % 16 == 0) {
            printf("\n");
        }
    }
    printf("\n");
}

char* itoa(int val, int base){
	
	static char buf[32] = {0};
	
	int i = 30;
	
	for(; val && i ; --i, val /= base)
	
		buf[i] = "0123456789abcdef"[val % base];
	
	return &buf[i+1];
	
}