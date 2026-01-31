#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

char buf2[100];

int main(void){
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);
    
    unsigned long page_start = (unsigned long)buf2 & ~(getpagesize() - 1);
    if(mprotect((void*)page_start, getpagesize(), PROT_READ | PROT_WRITE | PROT_EXEC) < 0){
        perror("mprotect failed");
        return 1;
    }

    char buf[100];
    printf("No system for you this time !!!\n");
    printf("buf2 address: %p\n", buf2); 
    gets(buf);
    strncpy(buf2, buf, 100);
    printf("bye bye ~");
    return 0;
}