// logger.js
var Web3 = require('web3');
web3 = new Web3('http://127.0.0.1:8545')

function getBlock(number) {

	web3.eth.getBlock(number, (err, block) => {
	  if (block != null) {
		  	//console.log("====== BLOCK # "+number+" ========");
		  	//console.log(block)
		    block.transactions.forEach(tx => {
		  		//console.log("====== BLOCK # "+number+" TX # "+tx+" ========");
				//console.log(tx)
		      	web3.eth.getTransaction(tx).then((err, _tx) => {
		      		console.log("====== BLOCK # "+number+" | TX #  "+tx+" ========");
					console.log(err);
		      	});
		      	web3.eth.getTransactionReceipt(tx).then((err, _tx) => {
		      		console.log("====== BLOCK # "+number+" | Receipt # "+tx+" ========");
					console.log(err);
		      	});
	    })
	  }
	  getBlock(number + 1)
	});

}

getBlock(0);
