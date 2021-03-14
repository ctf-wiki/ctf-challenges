## 1. Create Key

You can use [http://monitor.jungletestnet.io/#createKey](http://monitor.jungletestnet.io/#createKey)



## 2. Create Account

You can use [http://monitor.jungletestnet.io/#account](http://monitor.jungletestnet.io/#account)

## 3. Import to wallet

```shell
# create wallet
cleos wallet create -n deploy11 --to-console
# import private key
cleos wallet import -n deploy11
```

## 4. Faucet

You can use [http://monitor.jungletestnet.io/#faucet](http://monitor.jungletestnet.io/#faucet)

## 5. Buy RAM

```shell
cleos system buyram de1ctf111eos de1ctf111eos '50 EOS'
```



## 6. Compile contract

```shell
cd easyeos
eosio-cpp -o easyeos.wasm easyeos.cpp
```




## 7. Deploy contract

```shell
cleos set contract de1ctf111eos . -p de1ctf111eos@active
```

## 8. Listen at the back end, send flag if someone win

```shell
cd backend
nodejs src/listen.js
```

