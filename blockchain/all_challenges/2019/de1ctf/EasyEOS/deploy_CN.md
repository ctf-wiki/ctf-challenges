## 1. 创建Key

可以使用[http://monitor.jungletestnet.io/#createKey](http://monitor.jungletestnet.io/#createKey)



## 2. 创建账号

可以使用[http://monitor.jungletestnet.io/#account](http://monitor.jungletestnet.io/#account)

## 3. 导入钱包

```shell
创建钱包
cleos wallet create -n deploy11 --to-console
导入私钥
cleos wallet import -n deploy11
```

## 4. 水龙头充钱

可以使用[http://monitor.jungletestnet.io/#faucet](http://monitor.jungletestnet.io/#faucet)

## 5. 买内存

```shell
cleos system buyram de1ctf111eos de1ctf111eos '50 EOS'
```



## 6. 编译合约

```shell
cd easyeos
eosio-cpp -o easyeos.wasm easyeos.cpp
```




## 7. 部署合约

```shell
cleos set contract de1ctf111eos . -p de1ctf111eos@active
```

## 8. 后端监听，发送flag

```shell
cd backend
nodejs src/listen.js
```

