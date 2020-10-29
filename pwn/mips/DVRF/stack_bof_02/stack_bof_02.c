#include <string.h>
#include <stdio.h>
#include <stdlib.h>

//Simple BoF by b1ack0wl for E1550
//Shellcode is Required


int main(int argc, char **argv[]){
char buf[500] ="\0";

if (argc < 2){
printf("Usage: stack_bof_01 <argument>\r\n-By b1ack0wl\r\n");
exit(1);
} 


printf("Welcome to the Second BoF exercise! You'll need Shellcode for this! ;)\r\n\r\n"); 
strcpy(buf, argv[1]);

printf("You entered %s \r\n", buf);
printf("Try Again\r\n");

return 0;
}
