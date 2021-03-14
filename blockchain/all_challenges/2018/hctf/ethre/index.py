#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import sha3
from ethereum.utils import privtoaddr, encode_hex
from hashlib import sha256
from web3 import Web3
import signal
import time
import logging.handlers

signal.alarm(0x60)
my_ipc = Web3.IPCProvider("/home/ubuntu/.ethereum/geth.ipc")
assert my_ipc.isConnected()
w3py = Web3(my_ipc)
salt = b""

LOG_FILE = "hctf2018.log"
addr = os.environ["SOCAT_PEERADDR"]
handler = logging.handlers.RotatingFileHandler(LOG_FILE)
fmt = '%(asctime)s - %(levelname)s - %(message)s' + " - %s"%addr
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('hctf2018')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def banner():
    baner = """
_    _  _____ _______ ______ ___   ___  __  ___
| |  | |/ ____|__   __|  ____|__ \ / _ \/_ |/ _ \
| |__| | |       | |  | |__     ) | | | || | (_) |
|  __  | |       | |  |  __|   / /| | | || |> _ <
| |  | | |____   | |  | |     / /_| |_| || | (_) |
|_|  |_|\_____|  |_|  |_|    |____|\___/ |_|\___/

welcom to HCTF 2018 to play a ethereum reverse challengeself.
"""
    print(baner)

def PoW():
    random = bytes.hex(os.urandom(3))
    info = "sha256(X + %s).hexdigest()[:6] == '000000'"%random
    print(info)
    X = input("Please enter X: ").strip()
    news = X + random
    if sha256(news.encode()).hexdigest()[:6] == "000000":
        return True
    else:
        return False

def help_info():
    networdid = 111
    info = """
->  first, you need connect my private ethereum blockchain, networkid is %d
->  second, use sha3.keccak_256(your token) as your ethereum private key, and you can calculate your ethereum account address
->  third, if your account balance > 0, you can get flag1
->  use getflag2 to exec Smart contract getflag function and if you pass the function, I will give you flag2
->  finally, flag is: hctf{flag1+flag2}
    """%networdid
    print(info)

def init_file():
    with open("/home/ubuntu/geth/gene.json") as f:
        initf = f.read()
    print(initf)
    publickey = "e4bef62d1c7854093d5ceea236bd9c438c7d12a1ff86c0cf57c43a8cecda5f7a2ceef9c1397e695fee3f128b2c6dca2a756ca569877e7b2c2f1f4cde5636d8a7"
    print("enode://" + publickey)

def getflag1():
    token = input("Please enter your team token: ").strip()
    flag = sha256(token.encode() + salt).hexdigest()
    private_key = sha3.keccak_256(token.encode()).digest()
    public_key = "0x" + encode_hex(privtoaddr(private_key))
    try:
        value = w3py.eth.getBalance(Web3.toChecksumAddress(public_key))
    except:
        value = 0
    if value > 0:
        print(flag[:32])
        msg = "%s get flag1: %s"%(repr(token), flag[:32])
        logger.debug(msg)
    else:
        print("Failed")

def getflag2():
    token = input("Please enter your team token: ").strip()
    flag = sha256(token.encode() + salt).hexdigest()
    private_key = sha3.keccak_256(token.encode()).digest()
    public_key = "0x" + encode_hex(privtoaddr(private_key))
    contract = "0xc3dac37d5d3000a7fa70b574167fed36a8330a35"
    value = w3py.eth.getStorageAt(Web3.toChecksumAddress(contract), Web3.toChecksumAddress(public_key))
    value = int.from_bytes(bytes(value), "big")
    public_key_int = int(public_key[2:], 16)
    if (value + public_key_int)%(2**256) < value:
        print(flag[32:])
        msg = "%s get flag2: %s"%(repr(token), flag[32:])
        logger.debug(msg)
    else:
        print("Failed")

def hint():
    create_hint = "You can use this constract to find other two contract(Only Admin can call this constract)"
    user_hint = "You can call this constract, and set some value in storage"
    admin_hint = "Only admin can call this constract and sha3(getflag(uint256))[:8] == 'dddc5bbf'"
    hint_dict = {
        "0x628187b11ef814fe75dc9d33c813961b71153afc": create_hint,
        "0xc3dac37d5d3000a7fa70b574167fed36a8330a35": user_hint,
        "0x15ec709c5d749345a3bcfc36a5b6bb695aba51e4": admin_hint
    }
    help_info = "getflag2 hint: you enter token, and I will calculate your private key. The private key will be passed as a parameter to the constract's getflag function."
    print(help_info)
    help2 = "And I will help you to check constract address. (Three times)"
    print(help2)
    for _ in range(3):
        address = input("Please constract address(format: 0x12345): ").strip()
        if address in hint_dict:
            print(hint_dict[address])
        else:
            print("error address!")

def menu():
    men = """
A. help
B. get init file
C. getflag1
D. getflag2
E. getflag2_hint
"""
    print(men)
    choice = input("Please enter Your chioce:")
    return choice.strip()

def main():
    banner()
    if not PoW():
        print("Bye!")
        return
    c = menu().upper()
    if c == "A":
        help_info()
    elif c == "B":
        init_file()
    elif c == "C":
        getflag1()
    elif c == "D":
        getflag2()
    elif c == "E":
        hint()
    print("Bye!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(str(e))
