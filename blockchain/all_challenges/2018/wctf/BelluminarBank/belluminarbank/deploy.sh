#!/bin/bash

ps aux | grep -i geth | awk '{print $2}' | xargs kill -9

export WORK=$HOME/blockchain
genesis=$(cat <<EOF
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
EOF
)
echo $genesis > genesis.json

export NUM=$1
rm -rf $WORK/chain$NUM

geth --datadir "$WORK/chain$NUM" init genesis.json
geth --verbosity 5 --identity "BelluminarChain$NUM"  --rpc --rpcaddr "0.0.0.0" --rpcport "$((8000 + $NUM))" --rpccorsdomain "*" --datadir "$WORK/chain$NUM" --port "$((30000 + $NUM))" --nodiscover --rpcapi "db,eth,net,personal,web3" --networkid 31338 --mine --minerthreads 1 --etherbase 0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2 --nat "any" console
