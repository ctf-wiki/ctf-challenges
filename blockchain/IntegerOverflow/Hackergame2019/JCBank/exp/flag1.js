var Web3=require("web3");
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    web3 = new Web3(new Web3.providers.HttpProvider("https://kovan.infura.io/v3/b38f10b5036f4e6691fcc690461097d1"));
}

var address="0xE575c9abD35Fa94F1949f7d559056bB66FddEB51";
web3.eth.getStorageAt(address, 0, function(x,y){console.info(y)});
web3.eth.getStorageAt(address, 1, function(x,y){console.info(y)});
web3.eth.getStorageAt(address, 2, function(x,y){console.info(y)});
