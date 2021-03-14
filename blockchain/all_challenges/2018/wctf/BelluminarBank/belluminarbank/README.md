# Credits

The task was based on different challenges and bugs. See more like this:
https://github.com/sigp/solidity-security-blog#storage
https://blog.positive.com/phdays-8-etherhack-contest-writeup-794523f01248
https://capturetheether.com/
https://ethernaut.zeppelin.solutions/

# Info

Teams should hack contract BelluminarBank only knowing its address.
Note that each team is provided with separate copy of private blockchain with separate RPC port exposed (8001-80XX). Teams should not be able to access blockchain other than their's.
If you cannot implement such network rules, we can update VM and deploy nginx reverse-proxy with unique passwords for each team.

To solve this task, teams need to reverse engineer the bytecode, and use the following attacks:
1) Integer overflow to bypass deposit term limitations;
2) Storage overflow to overwrite the bank owner;
3) Storage access to disclose private attribute;
4) Deploy suicidal contract to force-send eth to target contract (to fix balance differencies).

They also need to know how to work with web3, how to find contract bytecode, etc.

0daysober solved the task a bit differently during the last step (as 0daysober did), you don't necessarily need Unexpected ether attack.
You can just craft a proper balance if you play with withdraw() and invest() calls. 

This is possible due to a huge bug leading to an unintended solution: the withdraw() function does not change the balances array.
But you still need to exploit integer overflow beforehand.

# Deployment information

(For the CTF) VM is given 4 CPU cores and 10GB of RAM. This is because of possible high memory usage when a lot of private blockchains are deployed.
VM also may be duplicated. It was tested and worked well with 9 blockchains.
Ubuntu credentials: belluminar ; this-wctf2018-pwd123

Flag is located in deploy.js on the following line: data: web3.toHex('flag{this is flag}').
To deploy task for 9 teams, run:
```
# bash run.sh 9
```

This will open RPC interfaces on ports 8001-8009, each of them should be accessible by one team only!

Full exploit can be found in exploit.js.
Example run:

```bash
root@kali:~/blockchain# geth attach --preload exploit.js http://localhost:8001/
Found contract:  0x8630b28e30890060bc32a48d077d9873ec7499c4
Start balance:  31337
null 0x9597b22aad0f7da66b52295eb4ec305f733308301b513815b737d4bea63ab094
Welcome to the Geth JavaScript console!

instance: Geth/BelluminarChain1/v1.8.10-stable-eae63c51/linux-amd64/go1.10
coinbase: 0x2ed93eaa607a536effbef67a7818760304f2ee12
at block: 8 (Sun, 03 Jun 2018 09:27:19 CDT)
 modules: eth:1.0 net:1.0 personal:1.0 rpc:1.0 web3:1.0

> null 0xa31bdea53d2c7170fffced9e0ad433cd28096a3748b0fcaa79943e7bc79b4c7a
Interim balance:  31337
Donor contract mined! address: undefined transactionHash: 0xe5ce04a02bd909fa17ceb6a203c8b585ae738b7c3176eabd951db0e401465cd7
Got secret:  0x00313373133731337313373133731337
null 0x4b4900975afcb2f9fe66ac9532b84ee1d458685c32804e6d38457fe960e60a42
Not yet solved, waiting...
Not yet solved, waiting...
Not yet solved, waiting...
Not yet solved, waiting...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
> Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Solved! Balance=0. Searching for flag...
Found flag:  flag{this is flag}
Solved! Balance=0. Searching for flag...
Found flag:  flag{this is flag}
```

# Description for teams

Belluminar Bank is very small and special. It works as follows:
- Anyone can invest any amount of money and should specify deposit term (deposit will be locked before that);
- Deposit term must be at least 1 year greater than deposit term of previous client;
- An account number is assigned to each deposit;
- Account 0 contains 31337 wei, locked for many years by the bank owner (contract creator);
- The bank owner can confiscate your deposit 1 year after the deposit term (if you don't withdraw).


Your goal is to hack this bank and empty its balance. If you succeed, the bot will send you the flag in transaction data.
Your eth address: 0x72d45c0dc7EfdAfd00467086B65B2fe078788c44
Unlock password: 123qwe
Contract address: 0x8630b28e30890060bc32a48d077d9873ec7499c4

Just in case, here's genesis.json:
{
  "config": {
        "chainId": 31338,
        "homesteadBlock": 0
    },

  "coinbase"   : "0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2",
  "difficulty" : "0x1",
  "extraData"  : "",
  "gasLimit"   : "0xffffff",
  "mixhash"    : "0x0000000000000000000000000000000000000000000000000000000000000000",
  "parentHash" : "0x0000000000000000000000000000000000000000000000000000000000000000",
  "alloc"      : {
    "0x72d45c0dc7EfdAfd00467086B65B2fe078788c44": {"balance": "10000000000000000000"},
    "0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2": {"balance": "10000000000000000000"}
  }
}
