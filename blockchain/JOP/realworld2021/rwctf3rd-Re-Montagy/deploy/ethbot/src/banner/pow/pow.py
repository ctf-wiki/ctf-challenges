import hashlib
import random
from conf.base import pow_difficult
import sys
import string

def generatepow(difficulty):
	prefix = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
	msg = "sha256(" + prefix + "+?).binary.endswith('" + "0" * difficulty + "')"
	return prefix, msg


def pow(prefix, difficulty, answer):
	hashresult = hashlib.sha256((prefix + answer).encode()).digest()
	bits = bin(int(hashlib.sha256((prefix + answer).encode()).hexdigest(), 16))[2:]
	if bits.endswith("0" * difficulty):
		return True
	else:
		return False



if __name__ == "__main__":
	prefix,msg=generatepow(pow_difficult)
	print("[+]",msg)
	answer=input("[-] ?=")

	if not pow(prefix,pow_difficult,answer):
		print("[+]wrong proof")
		sys.exit(0)
	print("[+] passed")